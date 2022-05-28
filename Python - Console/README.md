# About
Download official daily foreign currency exchange rates from Bank of Mongolia (BoM) website between chosen dates. https://www.mongolbank.mn/dblistofficialdailyrate.aspx

[screenshot](https://github.com/bilguun-zorigt/mongolbank-rate-downloader/tree/main/Python%20-%20Console/screenshot.png)

# Ready to use version
Download and run the executable file from:
https://github.com/bilguun-zorigt/mongolbank-rate-downloader/releases

# Create the bundle yourself

1. Install Python and Pip
2. Create and activate virtual environment
    ```
    ***Linux or Mac***
    python3 -m venv ./venv
    source ./venv/bin/activate 

    ***Windows***
    python -m venv ./venv
    venv\Scripts\activate
    ```
3. Install dependencies
    ```
    pip install --requirement requirements.txt
    ```
4. Create a bundled application
    ```
    pyinstaller --clean --noconfirm pyinstaller.spec 
    ```
