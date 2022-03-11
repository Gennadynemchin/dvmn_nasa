# Space pictures every day bot

For starting the bot just run main.py on command line. The bot has several methods
for downloading pictures from https://api.spacexdata.com - get photos from last launch,
NASA APOD from https://api.nasa.gov/planetary/apod and NASA EPIC.
```
python main.py
```
You have to change some variables in .env:
```
NASATOKEN='<YOUR TOKEN FOR NASA API SERVICE>'
DESTINATION_FOLDER='<NAME OF FOLDER THAT YOU ARE GOING TO USE FOR PHOTOS>'
TELEGRAM_TOKEN='<TOKEN YOU GOT FROM THE @BOTFATHER OF TELEGRAM>'
TELEGRAM_CHANNEL='@YOUR_TELEGRAM_CHANNEL'
SENDING_DELAY='DELAY BETWEEN PICTURE POSTING IN SECONDS'
```
Please see how to generate you NASA API token here:
```
https://api.nasa.gov/
```
After that just create a Telegram channel and add your bot to administrators.

### How to install
Clone the project:
```
git clone https://github.com/Gennadynemchin/dvmn_nasa.git
cd dvmn_nasa
```
Create and activate a virtual environment:
```
python3 -m venv env
source env/bin/activate
```
Install requirements:
```
pip install -r requirements.txt
```
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
