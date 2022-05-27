# About
Download official daily foreign currency exchange rates from Bank of Mongolia (BoM) website between chosen dates. https://www.mongolbank.mn/dblistofficialdailyrate.aspx

![screenshot](https://github.com/bilguun-zorigt/mongolbank-rate-scraper/blob/main/screenshot.png)


### Create and activate virtual environment
```
***create virtual environment***
python3 -m venv ./venv

***activete on Linux or Mac***
source ./venv/bin/activate 

***activate on Windows***
venv\Scripts\activate
```

### Install dependencies
```
pip install --requirement requirements.txt
```

### Create a bundled application
```
pyinstaller pyinstaller.spec --clean --noconfirm
```
