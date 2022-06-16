# Instructions

1. Install [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://docs.docker.com/get-docker/ "Download Docker") and [![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/download "Download Visual Studio Code")
2. [Download the project](https://github.com/bilguun-zorigt/mongolbank-rate-scraper-in-different-programming-languages/archive/refs/heads/main.zip) or [clone](https://github.com/bilguun-zorigt/mongolbank-rate-scraper-in-different-programming-languages.git) with [![Git](https://img.shields.io/badge/git-%23F05033.svg?logo=git&logoColor=white)](https://git-scm.com/downloads "Download Git")
3. Open folder [![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=white)](https://www.python.org/downloads/ "Download Python") in Visual Studio Code
4. Press <kbd>F1</kbd> and type <kbd>Reopen in Container</kbd> and press <kbd>⏎ Enter</kbd>
5. Type <kbd>python src/main.js</kbd> in terminal and press <kbd>⏎ Enter</kbd>

<!-- https://github.com/Ileriayo/markdown-badges -->

# Instructions - venv

1. Install [![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=white)](https://www.python.org/downloads/ "Download Python") and [![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/download "Download Visual Studio Code")
2. [Download the project](https://github.com/bilguun-zorigt/mongolbank-rate-scraper-in-different-programming-languages/archive/refs/heads/main.zip) or [clone](https://github.com/bilguun-zorigt/mongolbank-rate-scraper-in-different-programming-languages.git) with [![Git](https://img.shields.io/badge/git-%23F05033.svg?logo=git&logoColor=white)](https://git-scm.com/downloads "Download Git")
3. Open folder [![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=white)](https://www.python.org/downloads/ "Download Python") in Visual Studio Code
4. Create and activate python virtual environment
    ```
    ***Linux or Mac***
    python3 -m venv ./venv
    source ./venv/bin/activate 

    ***Windows***
    python -m venv ./venv
    venv\Scripts\activate
    ```
5. Type <kbd>pip install -r requirements.txt</kbd> in terminal and press <kbd>⏎ Enter</kbd>
6. Type <kbd>python src/main.js</kbd> in terminal and press <kbd>⏎ Enter</kbd>
7. To create an executable
    ```
    pip install pyinstaller
    pyinstaller --clean --noconfirm pyinstaller.spec 
    ```
