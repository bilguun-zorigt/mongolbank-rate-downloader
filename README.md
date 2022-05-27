# About
Download official daily foreign currency exchange rates from Bank of Mongolia (BoM) website between chosen dates. https://www.mongolbank.mn/dblistofficialdailyrate.aspx

![screenshot](https://github.com/bilguun-zorigt/mongolbank-rate-scraper/blob/main/Screenshot.png)


### Create and activate virtual environment
```
***venv***
python3 -m venv ./venv
or
***virtualenv***
virtualenv ./venv

***Linux / Mac***
source ./venv/bin/activate 

***Windows***
venv\Scripts\activate
```

### Install dependencies
```
pip install --requirement requirements.txt
```

### Create a bundled application
```
pyinstaller pyi.spec --clean --noconfirm --upx-dir "path/to/upx/dir/"
```
