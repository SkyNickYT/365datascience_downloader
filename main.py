# PYRAMID OF IMPORTS
import os
import re
import time
import html
import json
import pickle
import argparse
import html5lib
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
#Load .env
load_dotenv()
# Regex for valid Windows filenames (for validation)
windows_filename_regex = r'^(?!^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.[^\\/:*?"<>|\r\n]*)?$)(?!.*[\\/:*?"<>|\|]).{1,255}$'
# List of reserved device names that are invalid as filenames
reserved_device_names = [
    "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
]
def download_vtt(vtt_url, save_path):
	if vtt_url != None:
		ffmpeg_command = [
				'ffmpeg',
				'-v', 'quiet',
				'-i', vtt_url,
				save_path
			]
		try:
			# Execute the FFmpeg command
			subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + f" VTT downloaded,\n\tand saved to {save_path}")
		except subprocess.CalledProcessError as e:
			# Handle errors during FFmpeg execution
			print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Error occurred during FFmpeg execution: {e}")

		except Exception as e:
			# Handle other general exceptions
			print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"An unexpected error occurred: {e}")
def convert_vtt_to_srt(vtt_file, srt_file):
	if os.path.exists(vtt_file):
		try:
			# Run the FFmpeg command to convert VTT to SRT
			command = [
				'ffmpeg',
				'-v', 'quiet',
				'-i', vtt_file,  # Input VTT file
				srt_file	 # Output SRT file
			]
			# Execute the command
			subprocess.run(command, check=True)
			print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + f"Captions Download successful!\n\t Saved as SRT: {srt_file}")
			os.remove(vtt_file)
		except subprocess.CalledProcessError as e:
			print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Error during VTT conversion: {e}")
		except FileNotFoundError:
			print(Fore.RED + "\n[ERROR] " + Fore.RESET + "FFmpeg not found. Please install FFmpeg and ensure it's in your system's PATH.")
		except Exception as e:
			print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"An unexpected error occurred while converting VTT: {e}")
# Function to sanitize a string for use as a valid Windows filename
def sanitize(filename):
	# Step 1: Remove illegal characters (like \ / : * ? " < > |)
	sanitized_filename = re.sub(r'[\\/:*?"<>|\r\n]+', '_', filename)
	# Step 2: Replace reserved device names (e.g., COM1, CON, etc.) if found
	# Ensure the name is not just a reserved name or has the same name with extension
	if sanitized_filename.upper() in reserved_device_names:
		sanitized_filename = f"{sanitized_filename}_file"  # Add a suffix to make it valid
	# Step 3: Trim trailing spaces or periods
	sanitized_filename = sanitized_filename.rstrip(' .')
	# Step 4: Ensure the final filename length is within Windows' 255-character limit
	if len(sanitized_filename) > 255:
		sanitized_filename = sanitized_filename[:255]
	return sanitized_filename
def extract_ids_and_lecture_url(soup, account_id, headers, COURSE_URL):
	stripped_id = ""
	# Extracting the video ID
	crs_pattern = r'(?<=data-video-id=")\d+(?=")'
	course_id = re.search(crs_pattern, str(soup))
	if course_id:
		course_id = course_id.group(0)
		print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f"This Course's ID: {course_id}")
	else:
		course_id = None
		print(Fore.RED + "\n[ERROR] " + Fore.RESET + "Video ID not found.")

	# Extracting the lecture ID
	lecid_pattern = r"\/([a-f0-9\-]{36})\/main\/"
	lecture_id = re.search(lecid_pattern, str(soup))
	if lecture_id:
		lecture_id = lecture_id.group(1)
		print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f"This Lecture's ID: {lecture_id}")
	else:
		lecture_id = None
		print(Fore.RED + "\n[ERROR] " + Fore.RESET + "Lecture ID not found.")
	# Check if we have a valid video ID to proceed
	if course_id:
		# Construct the URL to get the video information from Brightcove
		threesv_url = f'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{course_id}'
		# Make the request to the API
		response = requests.get(threesv_url, headers=headers)
		if response.status_code == 200:
			print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + "Caught Something! What Is It?")
			data = response.json()
			# Convert data to string for easier handling of the manifest URL
			data = str(data)
			dur = re.findall(r"'duration': (\d+)", data)
			requested_duration = dur[-1]
			# Extracting the lecture video URL from the response data
			start_pt = data.find("'http://manifest.prod.boltdns.net/manifest/v1/hls")
			end_pt = data.find(",", start_pt)
			if start_pt != -1 and end_pt != -1:
				lec = data[start_pt:end_pt].split("'")[1::2]
				lecture_url = lec[0]
			else:
				print(Fore.RED + "\n[ERROR] " + Fore.RESET + "Lecture URL not found.")
			# Extracting the lecture caption URL from the response data
			start_pt = data.find("'http://house-fastly-signed-eu-west-1-prod.brightcovecdn.com/media/v1/text/vtt/clear/")
			end_pt = data.find(",", start_pt)
			if start_pt != -1 and end_pt != -1:
				lec = data[start_pt:end_pt].split("'")[1::2]
				caption_url = lec[0]
			else:
				print(Fore.RED + "\n[ERROR] " + Fore.RESET + "Caption URL not found.")
		else:
			print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Failed to get data: {response.status_code}")
	else:
		print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Video ID is required to fetch the lecture URL.")
	# Return both IDs and the lecture URL (if found)
	return lecture_id, course_id, lecture_url if 'lecture_url' in locals() else None, caption_url if 'caption_url' in locals() else None, requested_duration if 'requested_duration' in locals() else None
def duration_probe(file_path):
	try:
		# Build the ffprobe command
		command = [
			'ffprobe',
			'-i', file_path.replace(':',''),
			'-show_entries', 'format=duration',
			'-v', 'quiet',
			'-of', 'csv=p=0'
		]
		# Run the command using subprocess and capture the output
		result = subprocess.run(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
		# Output the result (duration in HH:MM:SS.xx format)
		duration = float(result.stdout)
		duration = str(duration)
		duration = duration.replace('.', '')
		duration = duration[0:6]
		duration = duration.ljust(6, '0')
		duration = int(duration)+1
		duration = str(duration)
		return duration

	except Exception as e:
		print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Could not retrieve the duration: {e}")
		return None
def is_duration_correct(existing_duration: str, expected_duration: str) -> bool:
	exidur = int(existing_duration)
	expdur = int(expected_duration)
	if(len(str(expdur))<7):
		rounded_exidur = exidur // 10
		if exidur % 10 >= 5:
			rounded_exidur += 1
	else:
		rounded_exidur = expdur+1
	if exidur >= expdur or rounded_exidur >= expdur:
		return True
	else:
		return False
def download_lecture_part(output_folder, lec_link, lec_title, expected_duration):
	if lec_link != None:
		if "vtt" in lec_link:
			output_path_vtt = os.path.join(output_folder, f"{lec_title}.vtt")
			output_path_srt = os.path.join(output_folder, f"{lec_title}.srt")
			if(os.path.exists(output_path_srt)):
				print(Fore.MAGENTA + "\n[SKIPPING] " + Fore.RESET + "Skipping Captions Download, they already exist for this lecture.")
				try:
					os.remove(output_path_vtt)
				except FileNotFoundError:
					pass
			else:
				print(Fore.YELLOW + "\n[FFMPEG] " + Fore.RESET + " Trying to Download Captions\n\t...")
				download_vtt(lec_link, output_path_vtt)
				time.sleep(3)
				convert_vtt_to_srt(output_path_vtt, output_path_srt)
	else:
		print(Fore.MAGENTA + "\n[INFO] " + Fore.RESET + "Captions will not be downloaded for this lecture, unavailable.")
	if lec_link != None:
		if "hls" in lec_link:
			output_path = os.path.join(output_folder, f"{lec_title}.mp4")
			# Construct the FFmpeg command as a list of arguments
			ffmpeg_command = [
				'ffmpeg',
				'-y',
				'-v', 'quiet', '-stats',
				'-i', lec_link,
				'-c', 'copy',
				'-bsf:a', 'aac_adtstoasc',
				output_path
			]
			# Check if the output file already exists
			if os.path.exists(output_path):
				existing_duration = duration_probe(output_path)
				if(is_duration_correct(existing_duration, expected_duration)):
					print(Fore.YELLOW + "\n[MOVING ON] " + Fore.RESET + f"Output file {output_path}\n\tjust downloaded or already exists, with correct duration.\n\t...")
				else:
					# Execute the FFmpeg command and wait for it to finish - fixing duration
					try:
						print(Fore.YELLOW + "\n[FFMPEG] " + Fore.RESET + f" Downloading Video for this lecture, alongside fixing duration to a correct one.\n\t...")
						process = subprocess.Popen(ffmpeg_command,
												   stdout=subprocess.PIPE,
												   stderr=subprocess.STDOUT,
												   universal_newlines=True)
						for line in iter(process.stdout.readline, b''):
							if line.rstrip() != "":
								print(">>>" + Fore.MAGENTA + line.rstrip().replace("size=", "") + Fore.RESET)
							else:
								break
						print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + f"Lecture Download completed successfully!" + Fore.MAGENTA + "\n\n[INFO] " + Fore.RESET +  f"Saved to {output_path} after fixing duration from {existing_duration} to {expected_duration}")
					except subprocess.CalledProcessError as e:
						print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Error during conversion, corrupted file maybe: {e}")
			else:
				# Execute the FFmpeg command and wait for it to finish
				try:
					print(Fore.YELLOW + "\n[FFMPEG] " + Fore.RESET + " Downloading Video for this lecture\n\t...")
					process = subprocess.Popen(ffmpeg_command,
											   stdout=subprocess.PIPE,
											   stderr=subprocess.STDOUT,
											   universal_newlines=True)
					for line in iter(process.stdout.readline, b''):
						if line.rstrip() != "":
							print(">>>" + Fore.MAGENTA + line.rstrip().replace("size=", "") + Fore.RESET)
						else:
							break
					print(Fore.GREEN + "\n[SUCCESS] " + Fore.RESET + f"Lecture Download completed successfully!" + Fore.MAGENTA + "\n\n[INFO] " + Fore.RESET +  f"Saved to {output_path}")
				except subprocess.CalledProcessError as e:
					print(Fore.RED + "\n[ERROR] " + Fore.RESET + f"Error during conversion: {e}")
# Function to validate the course URL
def check_course_url(course_url):
	base_url_1 = "https://learn.365datascience.com/"
	base_url_2 = "https://learn.365financialanalyst.com/"
	api_base_1 = "https://api.365datascience.com/"
	api_base_2 = "https://api.365financialanalyst.com/"
	# Check if the URL matches one of the base URLs
	if course_url.startswith(base_url_1) or course_url.startswith(base_url_2):
		unexpected_pattern = re.compile(r'/{2,}$')
		if(bool(unexpected_pattern.search(course_url))):
			course_url = re.sub(r'/+$', '', course_url)
		if not course_url.endswith('/'):
			course_url += '/'
		# Check if the URL contains the necessary sections
		if '/courses/' in course_url and course_url.count('/') == 6:
			return (base_url_1 if course_url.startswith(base_url_1) else base_url_2,
                    api_base_1 if course_url.startswith(base_url_1) else api_base_2)
		else:
			raise ValueError(
				f"{Fore.RED} \n[ERROR] {Fore.RESET} Provided URL must contain '/courses/' and end with course's first lecture.\n\t Are you missing that?"
				f"{Fore.RED} \n[ERROR] {Fore.RESET} Ensure you're providing the link to the first lecture."
			)
	else:
		raise ValueError("{Fore.RED} \n[ERROR] {Fore.RESET} Provided URL is not part of this tool's capability, only provide 365datascience and 365financialanalyst URLs.")
#MAIN
def main():
	global COURSE_URL
	global COURSE_SLUG
	global base_url
	global base_api_url
	global title_ignorer
	global cookie_file_name
	# Set up argument parsing
	parser = argparse.ArgumentParser(description='Process a course URL.')
	parser.add_argument('-c', '--course', type=str, required=True, help='Course link')
	parser.add_argument('-rc', '--remove-cookies', action='store_true', help='Deletes Cookies before processing on the link')
	# Parse the arguments
	args = parser.parse_args()
	COURSE_URL = args.course
	base_url = None
	try:
		base_url, base_api_url = check_course_url(args.course)
		course_slug_match = re.search(r"courses\/([^\/]+)\/", COURSE_URL)
		if "365data" in base_url:
			title_ignorer = " | 365 Data Science"
			cookie_file_name = "cookies_ds.pkl"
			COURSE_SLUG = course_slug_match.group(1)
		elif "365financial" in base_url:
			title_ignorer = " | 365 Financial Analyst"
			cookie_file_name = "cookies_fa.pkl"
			COURSE_SLUG = course_slug_match.group(1)
		else:
			print(f"{Fore.RED} \n[ERROR] {Fore.RESET}Uhhh not sure what happened here, please open an issue report on GitHub.")
			time.sleep(2)
			exit()
		# Check if the remove-cookies flag is present
		if args.remove_cookies:
			if(os.path.exists(cookie_file_name)):
				print(f"{Fore.YELLOW} \n[INFO] {Fore.RESET}Removing {cookie_file_name} before processing, make sure your creds are in .env file.")
				os.remove(cookie_file_name)
			else:
				print(f"{Fore.RED} \n[ERROR] {Fore.RESET}No Cookies to delete, you sure they ever existed?")
				time.sleep(2)
				exit()
		print(f"{Fore.MAGENTA} \n[WELCOME] {Fore.RESET}Platform chosen: {base_url}")
	except ValueError as e:
		print(e)
if __name__ == '__main__':
    main()
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')
TEMP_PATH = os.getenv('CHROME_PROFILE_PATH')
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
TEMP_PATH = os.path.join(current_directory,TEMP_PATH)
os.makedirs(TEMP_PATH, exist_ok=True)
# GIVE YOUR POLICY KEY HERE
POLICY_KEY = os.getenv('POLICY_KEY')
# MOSTLY SELENIUM
DRIVER_PATH = os.getenv('WEBDRIVER_PATH')
s =Service(DRIVER_PATH)
options = Options()
options.add_argument('ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument(fr"user-data-dir={TEMP_PATH}")
options.add_argument("--mute-audio")
options.add_argument('--headless=new')
options.add_argument("--log-level=3")
options.add_argument("--auto-open-devtools-for-tabs")
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
options.add_argument(f'user-agent={DesiredCapabilities.CHROME}')
# Set the custom download path in Chrome preferences
options.add_experimental_option(
	"prefs", {
	"profile.managed_default_content_settings.images": 2,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(service=s, options=options)
if(base_url != None and POLICY_KEY != None):
	# MOSTLY HEADERS
	headers = {
	    'Accept': f'application/json;pk={POLICY_KEY}',
	    'Accept-Language': 'en-US,en;q=0.9',
	    'Accept-Encoding': 'gzip, deflate, br, zstd',
	    'Origin': f'{base_url[:-1]}',
	    'Priority': 'u=1, i',
	    'Referer': f'{base_url}',
	    'Sec-CH-UA': '"Chromium";v="130", "Google Chrome";v="130", "Not_A_Brand";v="99"',
	    'Sec-CH-UA-Mobile': '?0',
	    'Sec-CH-UA-Platform': '"Windows"',
	    'Sec-Fetch-Dest': 'empty',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Site': 'cross-site',
	}
else:
	driver.close()
	exit()
driver.get(base_url)
print(Fore.BLUE + "\n[START] " + Fore.RESET +  "At Page Title: ",driver.title)
try:
    cookies = pickle.load(open(f"{cookie_file_name}", "rb"))
    cookie_header = "; ".join(f"{cookie['name']}={cookie['value']}" for cookie in cookies)
    headers['Cookie'] = cookie_header
except EOFError:
    # Handle end of file reached without any input
    cookies = ""
except FileNotFoundError:
    # Handle the case where the file doesn't exist
    cookies = ""
except Exception as e:
    # Handle any other potential exceptions
    print(f"An error occurred while storing cookies: {e}")
    cookies = ""
time.sleep(3)
if(cookies == ""):
	cookie_bar = driver.find_element(By.CSS_SELECTOR, ".ok")
	cookie_bar.click()
	viaemail = driver.find_element(By.CSS_SELECTOR, "div.action-btn:nth-child(4) > button:nth-child(1)")
	viaemail.click()
	time.sleep(2)
	print(Fore.MAGENTA + "\n[INFO] " + Fore.RESET + "Will be using creds to login: Gimme a sec...")
	email = driver.find_element(By.CSS_SELECTOR, "#email")
	email.send_keys(os.getenv('EMAIL'))
	password = driver.find_element(By.CSS_SELECTOR, "#password")
	password.send_keys(os.getenv('PASSWORD'))
	login = driver.find_element(By.CSS_SELECTOR, ".submit")
	login.click()
	time.sleep(5)
	cooked = driver.get_cookies()
	pickle.dump(cooked, open(f"{cookie_file_name}", "wb"))
else:
	print(Fore.MAGENTA + "\n[INFO] " + Fore.RESET + "Using cookies, you get a magic pass!")
	time.sleep(2)
	driver.delete_all_cookies()
	time.sleep(3)
	for cookie in cookies:
		keys = cookie.keys()
		driver.execute_cdp_cmd('Network.enable', {})
		driver.execute_cdp_cmd('Network.setCookie', cookie)
		driver.execute_cdp_cmd('Network.disable', {})
time.sleep(3)
driver.refresh()
driver.get(COURSE_URL)
driver.execute_cdp_cmd('Network.enable', {})
time.sleep(5)
course_title = driver.title
end_pt = course_title.find(title_ignorer, 0)
course_title = course_title[0:end_pt]
course_title = sanitize(course_title)
COURSE_PATH = OUTPUT_FOLDER+course_title+"/"
print(Fore.CYAN + "\n[INFO] " + Fore.RESET + "Course Page Title: ",driver.title)
sections = driver.find_elements(By.CSS_SELECTOR, "span[class='section-name']")
#sections
time.sleep(2)
if(len(sections) == 0):
	print(Fore.RED + "\n[ERROR] " + Fore.RESET + "Cookies expired or wrong, exiting!" + Fore.YELLOW + "\n[EXPLANATION] " + Fore.RESET + "To Fix this - Delete all data in cookies pickle file by using --remove-cookies or -rc flag, then try again!")
	driver.quit()
else:
	num = int(len(sections)/2)
	del sections[num-1:num]
	sections = sections[:num-1]
	print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f"Found {num-1} total sections in this course.")
	les = driver.find_element(By.XPATH, """//*[@id="section-lectures-0"]/ul/li[1]/a""").text
	end_pt = les.find("\n", 0)
	lesson_name = les[0:end_pt]
	index = 1
	indice = 1
	for index, section in enumerate(sections):
		print(Fore.MAGENTA + "\n[INFO] " + Fore.RESET + f"{section.text}")
		indice = 1
		index += 1
time.sleep(5)
time.sleep(5)
# wet, hot and ready...
soup = html.unescape((BeautifulSoup(driver.page_source, 'html.parser')))
# getting accountId
acc_pattern = r"\/(\d{13})\/[a-f0-9\-]{36}\/main\/"
account_id = re.search(acc_pattern, str(soup)).group(1)
print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f'Your Account\'s ID: {account_id}')
lesson_pattern = r'lesson">\s*(.*?)\s*<\/span>'
# Find all lessons
lessons = re.findall(lesson_pattern, str(soup))
print(Fore.MAGENTA + "\n[INFO] " + Fore.RESET + f' Found {len(lessons)} lectures in this Course.\n\tWill try to download video & captions, please report any issues on GitHub.')
total_lec_element = driver.find_element(By.XPATH, """//*[@id="__layout"]/div/header/nav/ul/li[1]/div[1]/div/div/div""").text
total_lec_pattern = r'/(?P<number>\d+)'
total_lecture = re.search(total_lec_pattern, total_lec_element)
lesson_index = int(total_lecture.group('number'))
while indice-1 <= lesson_index-1:
	lesson_name = lessons[indice-1]
	lesson_name_escaped = re.escape(lesson_name).replace('"', '&quot;')
	lesson_url_pattern = fr'href="([^"]+)"(?=[^>]*title="{lesson_name_escaped}")'
	try:
		lesson_url_match = re.search(lesson_url_pattern, str(soup))[0]
	except IndexError:
		lesson_url_match = None
	except TypeError:
		lesson_url_match = None
	if lesson_url_match is not None:
		lesson_url =  base_url[:-1] + lesson_url_match
		start_pt = lesson_url.find("/courses/")
		end_pt = lesson_url.find('" ', start_pt)
		lesson_url = lesson_url[start_pt:end_pt]
		lesson_url = base_url[:-1] + lesson_url
	else:
		les_name = lesson_name.replace('"', '')
		les_name = les_name.replace("'", '')
		lesson_name_extrap = les_name.replace(" ", '-')
		lesson_url = f"{base_url[:-1]}/courses/{COURSE_SLUG}/{lesson_name_extrap.lower()}/"
	print(Fore.CYAN + "\n[INFO] " + Fore.RESET + f" Lecture {indice} of {lesson_index}: {lesson_name}\n\thas URL {lesson_url}")
	current_url = driver.current_url
	if(lesson_url != current_url): #Next ones
		driver.get(lesson_url)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(6)
		time.sleep(6)
		# Wait for thex  page to load completely (you can customize this condition)
		WebDriverWait(driver, 10).until(
		    EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Wait for the body element to be present
		)
		# wet, hot and ready... (second timer)
		soup = html.unescape(str(BeautifulSoup(driver.page_source, 'lxml')))
		lecture_id, course_id, lecture_url, caption_url, expected_duration = extract_ids_and_lecture_url(soup, account_id, headers, COURSE_URL)
		lesson_name = sanitize(lesson_name)
		lesson_name = str(indice)+" - "+lesson_name
		download_lecture_part(COURSE_PATH, lecture_url, lesson_name, expected_duration)
		download_lecture_part(COURSE_PATH, caption_url, lesson_name, expected_duration)
	else: #First one
		time.sleep(6)
		time.sleep(6)
		WebDriverWait(driver, 10).until(
		    EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Wait for the body element to be present
		)
		soup = html.unescape(str(BeautifulSoup(driver.page_source, 'html.parser')))
		lecture_id, course_id, lecture_url, caption_url, expected_duration = extract_ids_and_lecture_url(soup, account_id, headers, COURSE_URL)
		# writing out for if we ever want to debug this mess, plus exercises
		os.makedirs(COURSE_PATH, exist_ok=True)
		with open(f'{COURSE_PATH}soup.html', 'w', encoding='utf-8') as out:
			out.write(f"{soup}")
			print(Fore.MAGENTA + "\n[INFO] " + Fore.RESET + f'Experimental, Saved page soup as HTML. (Best alternative for building exercises later)')
		lesson_name = sanitize(lesson_name)
		lesson_name = str(indice)+" - "+lesson_name
		download_lecture_part(COURSE_PATH, lecture_url, lesson_name, expected_duration)
		download_lecture_part(COURSE_PATH, caption_url, lesson_name, expected_duration)
	indice += 1
driver.quit()
time.sleep(5)
print(Fore.BLUE + "\n[END] " + Fore.RESET + "Course Download Completed! (exiting)")
exit()
