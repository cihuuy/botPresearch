# Presearch Bot Farmer

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

This bot will farm pre token with presearch.
Before use this bot you need to register here [presearch](https://presearch.org/signup?rid=1800866)

Disclaimer: This use is against TOS of presearch. Its use is your responsibility.

## Installation

1. Download this repository or clone it
2. Use virtual environment or pass to step 3
3. Install requirements
```bash
$ pip install -r requirments.txt
```
4. Then go to 'data/account.txt' and write your 'mail|password'
5. (optional) Change phrases in text.tx and add words in wordList.txt
6. launch main.py in the parent directory
```bash
$ python3 /path/to/botPresearch/main.py
```
- For Windows:
```bash
$ c:\>c:\Python3\python c:\path\to\botPresearch\main.py
```
7. Verify that all works fine

### Using virtualenv

If you don't want to change your python configuration, consider using a venv.

1. upgrade pip and install virtualenv

```bash
$ pip3 install --upgrade pip
$ pip3 install virtualenv
```

2. Create a virtualenv
- For Linux/MacOs:
```bash
$ python3 -m venv /path/to/botPresearch/venv
```
- For Windows:
```bash
$ python3 -m venv c:\path\to\botPresearch\venv
```
3. Activate new environment
- For Linux/MacOs:
```bash
$ source /path/to/botPresearch/venv/bin/activate
```
- For Windows:
```bash
$ source c:\path\to\botPresearch\venv\Scrips\activate.bat
```
4. Verify that you have (venv) before command line
5. Return to normal installation

#### Deactivate venv

You only need to write in terminal:
```bash
$ deactivate
```

## Improvements

- [ ] Make secure password
- [ ] Adding recaptcha solver (or simplest way to solve captcha)
- [ ] Find a way to delete pytrends
- [ ] Adding a logger
- [ ] Verify internet connection