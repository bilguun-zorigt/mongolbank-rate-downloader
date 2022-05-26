# mongolbank-rate-scraper
Download official daily foreign currency exchange rates from Bank of Mongolia website between chosen dates. https://www.mongolbank.mn/dblistofficialdailyrate.aspx

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
