# About
Download official daily foreign currency exchange rates from Bank of Mongolia (BoM) website between chosen dates. https://www.mongolbank.mn/dblistofficialdailyrate.aspx

![screenshot](https://github.com/bilguun-zorigt/mongolbank-rate-scraper/blob/main/Screenshot%20from%202022-05-27%2001-27-42.png)


### Create and activate virtual environment
```
python3 -m venv ./venv

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
pyinstaller pyi.spec
```
