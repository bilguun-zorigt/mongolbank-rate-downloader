# About
Download official daily foreign currency exchange rates from Bank of Mongolia (BoM) website between chosen dates. https://www.mongolbank.mn/dblistofficialdailyrate.aspx

![screenshot](https://github.com/bilguun-zorigt/mongolbank-rate-scraper/blob/main/screenshot.png)![screenshot](https://github.com/bilguun-zorigt/mongolbank-rate-scraper/blob/main/screenshot_console_version.png)


### Create and activate virtual environment
```
***Linux or Mac***
python3 -m venv ./venv
source ./venv/bin/activate 

***Windows***
python -m venv ./venv
venv\Scripts\activate
```

### Install dependencies
```
pip install --requirement requirements.txt
```

### Create a bundled application
```
pyinstaller --clean --noconfirm pyinstaller-console.spec 
pyinstaller --clean --noconfirm pyinstaller.spec 
```
