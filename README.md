# Parent-Simulator

Pretend to be a parent talking to their child.

Used in AI presentation in the 2024 [Hak4Kidz Ethical Hacking Conference](https://www.hak4kidz.com/)

<br></br>

Installation instructions:
- Download [Python](python.org/downloads)
    - Run the downloaded executable
    - Go to advanced and add python to environment variables
- Download this repo (if you don't have git already)
    - Go to https://github.com/SnoringRhinoceros/Parent-Simulator 
    - Code -> download zip
    - Extract zip
    - cd into Parent-Simulator
- python3 -m venv venv
- venv/Scripts/activate (Windows) or source venv/bin/activate (Mac)
- Download FFmpeg
    - For Windows:
      - Go to [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)
      - Download Release builds -> ffmpeg-release-essentials.zip
      - Extract zip
      - Rename the new folder to FFmpeg
      - Move FFmpeg to root directory
      - Add FFmpeg to environment variables
          Settings -> Environment Variables -> system settings -> C:\FFmpeg\bin
    - For Mac:
      - Install [homebrew](https://brew.sh/)
      - brew install ffmpeg
- Download [ollama](https://ollama.com/download)
- ollama run llama3
- pip3 install -r requirements.txt

<br></br>
If you are getting:
  
  urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]

Make sure to install certifi
- pip install certifi
- /Applications/Python\ 3.6/Install\ Certificates.command

from [https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error](https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error)
