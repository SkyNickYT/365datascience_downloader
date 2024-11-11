# Any Current Offers Show Here:
#### Will remove when no offers, Current offer: Nov. 1, 2024 to Nov. 21, 2024
<img src="https://i.imgur.com/IShuD9o.png" alt="Imgur Image" width="500"/>

# 365 Data Science + Financial Analyst Downloader

### 365datascience_downloader or 365financialanalyst_downloader

-   A Simple course downloader for 365datascience.com and 365financialanalyst.com platforms.

-   This program is WIP, the code is provided as-is and I am not held resposible for any legal issues resulting from the use of this program.

## Requirements
The following are a list of required third-party tools, you will need to ensure they are in your systems path and that typing their name in a terminal invokes them.

> [!NOTE]  
> These are seperate requirements that are not installed with the pip command!
>
> You will need to download and install these manually!

1. Install [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) Also add it to your OS `PATH`
2. Install [Python 3.10+](https://www.xda-developers.com/how-to-install-python/) I prefer `Python 3.12`
3. Install [Selenium Chrome WebDriver](https://googlechromelabs.github.io/chrome-for-testing/) & Know the path, where it's downloaded.

## Setup

### Get your account's policy key to access API.

1. Clone this repo, and keep it in the same directory where you want the courses to go, this can be changed later using `.env`.

2. Copy & Paste `.env.sample` file and rename it to `.env`

3. Open any course's lecture, doesn't matter first, last or middle (should display a video on this page)

4. Refresh this page after opening your browser's DevTools (F12) `Network tab`, search/filter for `edge`, now you should see a request with a bunch of numbers, click on this

   -> Go to its Headers

   -> Copy the `Accept` header's `;pk=whatever_value_here` <--- `whatever_value_here part` only

   -> Paste the `whatever_value_here` part after `=` in `.env` in front of `POLICY_KEY=` text. Double-Quotes are *NOT* necessary.

6. More setup requires editing the `.env` file and installing `dependencies`, read below.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`

2. Setup `.env` file with your account credentials and policy key etc. MAKE SURE, not the google login one - it's not what script aims to achieve.

3. Paste the path to your `chromedriver` file just after `WEBDRIVER_PATH=` in the `.env` file.

4. Run the course download script: `python main.py -c {course_url}` <- Check how to get started section below don't be confused, this requires full first lecture's link

5. Once over you will find the course in `out_dir` folder, this is created automatically on initial startup of script.
   In the same directory the script `main.py` is kept. You can edit where the courses go, by changing `.env` file's `OUTPUT_FOLDER=` value.

6. Cookies automatically generate on your first login, you don't need credentials everytime you use the tool.

7. If you get `cookies have expired error`, delete them by using the `-rc` or `--remove-cookies` flag.

## Usage

In a `Windows terminal`, `bash shell` or a `shell` application of your choosing, examples given below.

#### For Windows,
```
(Normal Usage)
python main.py --course https://learn.365datascience.com/courses/data-literacy/what-exactly-is-data-literacy/
OR
python main.py -c https://learn.365financialanalyst.com/courses/who-does-what-in-finance/course-introduction/

(Deleting Cookies)
python main.py --course https://learn.365financialanalyst.com/courses/who-does-what-in-finance/course-introduction/ --rc
OR
python main.py -c https://learn.365datascience.com/courses/data-literacy/what-exactly-is-data-literacy/ --remove-cookies
```

#### For Linux or Mac,
```
(Normal Usage)
$ python3 main.py --course https://learn.365datascience.com/courses/data-literacy/what-exactly-is-data-literacy/
OR
$ python3 main.py -c https://learn.365financialanalyst.com/courses/who-does-what-in-finance/course-introduction/

(Deleting Cookies)
$ python3 main.py --course https://learn.365financialanalyst.com/courses/who-does-what-in-finance/course-introduction/ --rc
OR
$ python3 main.py -c https://learn.365datascience.com/courses/data-literacy/what-exactly-is-data-literacy/ --remove-cookies
```

> [!IMPORTANT] 
> **PROVIDE** Link for the **first lecture** from the course, or you will get **errors**.

**By Default**: Video quality is *1080p*, anything lower blurs screen text. Why would you even want that? Be Better!

**Video Captions**: Get Converted to SRT from VTT, if you have no problem with that use this tool or edit `main.py` yourself. Later I'll put an option to choose between these.

> [!CAUTION]
> **Missing Captions**: Some videos don't have captions attached, that's not my fault. This tool will let you know when it happens.

<details>
<summary><---Preview Download Folders' structure for "Introduction to Data and Data Science" and "Who Does What in Finance" courses:</summary>

```
📦out_dir
 ┗ 📂Introduction to Data and Data Science
 ┃ ┣ 🎥1 - Course Introduction.mp4
 ┃ ┣ 📜1 - Course Introduction.srt
 ┃ ┣ 🎥2 - Why are there so many business and data science buzzwords_.mp4
 ┃ ┣ 📜2 - Why are there so many business and data science buzzwords_.srt
 ┃ ┣ 🎥3 - Analysis vs Analytics.mp4
 ┃ ┣ 📜3 - Analysis vs Analytics.srt
 ┃ ┣ 🎥4 - Intro to Business Analytics, Data Analytics, and Data Science.mp4
 ┃ ┣ 📜4 - Intro to Business Analytics, Data Analytics, and Data Science.srt
 ┃ ┣ 🎥5 - Adding Business Intelligence (BI), Machine Learning (ML), and Artificial Intelligence (AI) to the picture.mp4
 ┃ ┣ 📜5 - Adding Business Intelligence (BI), Machine Learning (ML), and Artificial Intelligence (AI) to the picture.srt
 ┃ ┣ 🎥6 - An Overview of our Data Science Infographic.mp4
 ┃ ┣ 📜6 - An Overview of our Data Science Infographic.srt
 ┃ ┣ 🎥7 - When are Traditional data, Big Data, BI, Traditional Data Science and ML applied_.mp4
 ┃ ┣ 📜7 - When are Traditional data, Big Data, BI, Traditional Data Science and ML applied_.srt
 ┃ ┣ 🎥8 - Why do we Need each of these Disciplines_.mp4
 ┃ ┣ 📜8 - Why do we Need each of these Disciplines_.srt
 ┃ ┣ 🎥9 - Traditional Data_ Techniques.mp4
 ┃ ┣ 📜9 - Traditional Data_ Techniques.srt
 ┃ ┣ 🎥10 - Traditional Data_ Real-life Examples.mp4
 ┃ ┣ 📜10 - Traditional Data_ Real-life Examples.srt
 ┃ ┣ 🎥11 - Big Data_ Techniques.mp4
 ┃ ┣ 📜11 - Big Data_ Techniques.srt
 ┃ ┣ 🎥12 - Big Data_ Real-life Examples.mp4
 ┃ ┣ 📜12 - Big Data_ Real-life Examples.srt
... and so on.

Similarly,

📦out_dir
 ┗ 📂 Who Does What in Finance
 ┃ ┣ 🎥1 - Course Introduction.mp4
 ┃ ┣ 📜1 - Course Introduction.srt
 ┃ ┣ 🎥2 - The company lifecycle model.mp4
 ┃ ┣ 📜2 - The company lifecycle model.srt
 ┃ ┣ 🎥3 - The introductory stage.mp4
 ┃ ┣ 📜3 - The introductory stage.srt
 ┃ ┣ 🎥4 - Growth stage.mp4
 ┃ ┣ 📜4 - Growth stage.srt
 ┃ ┣ 🎥5 - Enterprise stage.mp4
 ┃ ┣ 📜5 - Enterprise stage.srt
 ┃ ┣ 🎥6 - IPO and Large enterprise stage.mp4
 ┃ ┣ 📜6 - IPO and Large enterprise stage.srt
 ┃ ┣ 🎥7 - Post-IPO developments.mp4
 ┃ ┣ 📜7 - Post-IPO developments.srt

... I think you get the idea.
```

</details>

## CURRENTLY NOT POSSIBLE - SO, YOU DO MANUALLY

- Download all course resource (.zip) This is a single click process on website.
  So while you're copying the first lecture link, save it in the same directory as the course or anywhere you want.
  
- Download exercises (yes exercises, not resources neither exams), alternatively `soup.html` is generated containing all raw exercise data.
  (later I might add to this, for now keep it safe for later use)

- Feel free to open GitHub Issues or Enhancement Requests, if you encounter some issues or have ideas to contribute.

## WHAT WILL NOT BE ADDED? - COURSE EXAMS

Sharing Final Course exams break 365 platforms' ToS. So, this tool has no scope to address that.
Similarly, I'm not sure about the course practice exams.
