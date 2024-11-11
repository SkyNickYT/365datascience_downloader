# 365datascience_downloader
Simple course downloader for 365datascience.com and 365financialanalyst.com platforms.

## Pre-Requisite

1. Install [ffmpeg](https://www.videoproc.com/resource/how-to-install-ffmpeg.htm) Also add it to your `PATH`
2. Install [Python 3.10+](https://www.xda-developers.com/how-to-install-python/) I prefer `Python 3.12`
3. Install [Selenium Chrome WebDriver](https://googlechromelabs.github.io/chrome-for-testing/) & Know the path, where it's installed.

## Usage

### Get your account's policy key to access API.

Will list other steps soon.

1. Clone this repo, and keep it in same directory where you want the courses to go.

2. Copy paste `.env.sample` file and rename to `.env`

3. In your browser's DevTools (F12) network tab, look for `edge.api.brightcove.com` -> Go to Headers -> Copy policy-key-raw -> Paste it in `.env` in front of `POLICY_KEY=`. This remains unchanged and will work for both platforms.
   
[wait a little] more steps coming soon. (including how to add login details, managing cookies, etc.)

### Downloading a course

In a `Windows terminal`, `bash shell` or a shell of your choosing.

Example Usage:

For Windows,
```
python main.py -c https://learn.365datascience.com/courses/data-literacy/what-exactly-is-data-literacy/
```

For Linux,
```
python3 main.py -c https://learn.365datascience.com/courses/data-literacy/what-exactly-is-data-literacy/
```

**IMPORTANT**: *PROVIDE Link for the first lecture from the course*, or you will get **errors**.

*By Default*: Video quality is *1080p*, anything lower blurs screen text. Why would you even want that? Be Better!
*Captions*: Get Converted to SRT from VTT.

#### Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the course download script: `python main.py {course_url}` <- Check usage above don't be confused, this requires full first lecture's link
3. Once over you will find the course in `out_dir` folder, this is created automatically on initial startup of script.
   In the same directory the script `main.py` is kept. Later I'll add something so you can change this, but for now this is it.

<details>
<summary>Download folders for "Introduction to Data and Data Science" and "Who Does What in Finance" courses:</summary>

```
📦out_dir
 ┗ 📂Introduction to Data and Data Science
 ┃ ┣ 📜1 - Course Introduction.mp4
 ┃ ┣ 📜1 - Course Introduction.srt
 ┃ ┣ 📜2 - Why are there so many business and data science buzzwords_.mp4
 ┃ ┣ 📜2 - Why are there so many business and data science buzzwords_.srt
 ┃ ┣ 📜3 - Analysis vs Analytics.mp4
 ┃ ┣ 📜3 - Analysis vs Analytics.srt
 ┃ ┣ 📜4 - Intro to Business Analytics, Data Analytics, and Data Science.mp4
 ┃ ┣ 📜4 - Intro to Business Analytics, Data Analytics, and Data Science.srt
 ┃ ┣ 📜5 - Adding Business Intelligence (BI), Machine Learning (ML), and Artificial Intelligence (AI) to the picture.mp4
 ┃ ┣ 📜5 - Adding Business Intelligence (BI), Machine Learning (ML), and Artificial Intelligence (AI) to the picture.srt
 ┃ ┣ 📜6 - An Overview of our Data Science Infographic.mp4
 ┃ ┣ 📜6 - An Overview of our Data Science Infographic.srt
 ┃ ┣ 📜7 - When are Traditional data, Big Data, BI, Traditional Data Science and ML applied_.mp4
 ┃ ┣ 📜7 - When are Traditional data, Big Data, BI, Traditional Data Science and ML applied_.srt
 ┃ ┣ 📜8 - Why do we Need each of these Disciplines_.mp4
 ┃ ┣ 📜8 - Why do we Need each of these Disciplines_.srt
 ┃ ┣ 📜9 - Traditional Data_ Techniques.mp4
 ┃ ┣ 📜9 - Traditional Data_ Techniques.srt
 ┃ ┣ 📜10 - Traditional Data_ Real-life Examples.mp4
 ┃ ┣ 📜10 - Traditional Data_ Real-life Examples.srt
 ┃ ┣ 📜11 - Big Data_ Techniques.mp4
 ┃ ┣ 📜11 - Big Data_ Techniques.srt
 ┃ ┣ 📜12 - Big Data_ Real-life Examples.mp4
 ┃ ┣ 📜12 - Big Data_ Real-life Examples.srt
... and so on.

Similarly,

📦out_dir
 ┗ 📂 Who Does What in Finance
 ┃ ┣ 📜1 - Course Introduction.mp4
 ┃ ┣ 📜1 - Course Introduction.srt
 ┃ ┣ 📜2 - The company lifecycle model.mp4
 ┃ ┣ 📜2 - The company lifecycle model.srt
 ┃ ┣ 📜3 - The introductory stage.mp4
 ┃ ┣ 📜3 - The introductory stage.srt
 ┃ ┣ 📜4 - Growth stage.mp4
 ┃ ┣ 📜4 - Growth stage.srt
 ┃ ┣ 📜5 - Enterprise stage.mp4
 ┃ ┣ 📜5 - Enterprise stage.srt
 ┃ ┣ 📜6 - IPO and Large enterprise stage.mp4
 ┃ ┣ 📜6 - IPO and Large enterprise stage.srt
 ┃ ┣ 📜7 - Post-IPO developments.mp4
 ┃ ┣ 📜7 - Post-IPO developments.srt

... I think you get the idea.
```

</details>

## CURRENTLY NOT POSSIBLE - SO, YOU DO MANUALLY

- Download all course resource (.zip) This is a single click process on website.
  So while you're copying the first lecture link, save it in the same directory as the course or anywhere you want.
  
- Download exercises (yes exercises, not resources), alternatively soup.html is generated containing all raw exercise data.
  (later I might add to this, for now keep it safe for later use)

## WHAT WILL NOT BE ADDED? - FINAL COURSE EXAMS
These break 365's platforms' ToS. So, this tool has no scope to address that.
I'm not sure about course practice exams too.
