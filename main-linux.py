#pyramid of imports
import os
import re
import time
import html
import json
import pickle
import argparse
import requests
import subprocess
from threading import Timer
from bs4 import BeautifulSoup
from selenium import webdriver
from colorama import init, Fore
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Initialize colorama
init()

# Load .env
load_dotenv()

def download_vtt(vtt_url, save_path):
    if vtt_url:
        ffmpeg_command = ['ffmpeg', '-v', 'quiet', '-i', vtt_url, save_path]
        try:
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + f" VTT downloaded,\n\tand saved to {save_path}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Error occurred during FFmpeg execution: {e}")
        except Exception as e:
            print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"An unexpected error occurred: {e}")

def convert_vtt_to_srt(vtt_file, srt_file):
    if os.path.exists(vtt_file):
        try:
            command = ['ffmpeg', '-v', 'quiet', '-i', vtt_file, srt_file]
            subprocess.run(command, check=True)
            print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + f"Captions Download successful!\n\t Saved as SRT: {srt_file}")
            os.remove(vtt_file)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Error during VTT conversion: {e}")
        except FileNotFoundError:
            print(Fore.RED + "\n[ERROR] " + Fore.RESET + "FFmpeg not found. Please install FFmpeg and ensure it's in your system's PATH.")
        except Exception as e:
            print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"An unexpected error occurred while converting VTT: {e}")

def sanitize(filename):
    sanitized_filename = re.sub(r'[\\/:*?"<>|\r\n]+', '_', filename)
    sanitized_filename = sanitized_filename.rstrip(' .')
    if len(sanitized_filename) > 255:
        sanitized_filename = sanitized_filename[:255]
    return sanitized_filename

def extract_ids_and_lecture_url(soup, account_id, headers, COURSE_URL):
    course_id = re.search(r'(?<=data-video-id=")\d+(?=")', str(soup))
    course_id = course_id.group(0) if course_id else None
    print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f"This Course's ID: {course_id}")

    lecture_id = re.search(r"\/([a-f0-9\-]{36})\/main\/", str(soup))
    lecture_id = lecture_id.group(1) if lecture_id else None
    print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f"This Lecture's ID: {lecture_id}")

    if course_id:
        threesv_url = f'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{course_id}'
        response = requests.get(threesv_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            data_str = str(data)
            duration = re.findall(r"'duration': (\d+)", data_str)[-1]
            lecture_url = re.search(r"'http://manifest.prod.boltdns.net/manifest/v1/hls.+?", data_str)
            caption_url = re.search(r"'http://house-fastly-signed-eu-west-1-prod.brightcovecdn.com/media/v1/text/vtt/clear/.+?", data_str)
            return lecture_id, course_id, lecture_url.group(0) if lecture_url else None, caption_url.group(0) if caption_url else None, duration
        else:
            print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Failed to get data: {response.status_code}")
    return lecture_id, course_id, None, None, None

def check_course_url(course_url):
    base_url_1 = "https://learn.365datascience.com/"
    base_url_2 = "https://learn.365financialanalyst.com/"
    if course_url.startswith(base_url_1) or course_url.startswith(base_url_2):
        course_url = course_url.rstrip('/') + '/'
        if '/courses/' in course_url and course_url.count('/') == 6:
            return (base_url_1 if course_url.startswith(base_url_1) else base_url_2, f"https://api.{base_url_1.split('//')[1]}")
        else:
            raise ValueError(f"{Fore.RED} \n[ERROR] {Fore.RESET} Invalid course URL.")
    else:
        raise ValueError(f"{Fore.RED} \n[ERROR] {Fore.RESET} Unsupported URL.")

def main():
    parser = argparse.ArgumentParser(description='Process a course URL.')
    parser.add_argument('-c', '--course', type=str, required=True, help='Course link')
    args = parser.parse_args()
    global COURSE_URL, base_url, base_api_url
    COURSE_URL = args.course
    try:
        base_url, base_api_url = check_course_url(args.course)
        print(f"{Fore.MAGENTA} \n[WELCOME] {Fore.RESET}Platform chosen: {base_url}")
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()

OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')
TEMP_PATH = os.getenv('CHROME_PROFILE_PATH')
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
TEMP_PATH = os.path.join(current_directory, TEMP_PATH)
os.makedirs(TEMP_PATH, exist_ok=True)
POLICY_KEY = os.getenv('POLICY_KEY')
DRIVER_PATH = os.getenv('WEBDRIVER_PATH')
service = Service(DRIVER_PATH)
options = Options()
options.add_argument('ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument(f"user-data-dir={TEMP_PATH}")
options.add_argument("--mute-audio")
options.add_argument('--headless=new')
options.add_argument("--log-level=3")
options.add_experimental_option(
    "prefs", {
        "profile.managed_default_content_settings.images": 2,
        "safebrowsing.enabled": True
    }
)
driver = webdriver.Chrome(service=service, options=options)
