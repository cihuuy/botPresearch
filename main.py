import os
import os.path

from src.CookieManager import CookieManager
from src.PresearchScrapper import PresearchScrapper
from src.WordManager import WordManager

CHROME_DIR = "chrome"

DRIVERS_DIR = "drivers"
DRIVER = "chromedriver"

LOG_DIR = "logs"
ERROR_LOG = "error.log"
RUN_LOG = "run.log"
SEARCH_LOG = "search.log"

COOKIE_DIR = "cookies"
DATA_DIR = "data"
WORD_FILE = "text.txt"
WORD_LIST_FILE = "wordList.txt"

ACCOUNT_FILE = "account.txt"

DEBUG = True


# TODO: test internet connection

# TODO: make a logger

def main() -> None:
    dir_run_from = os.getcwd()

    # Log gesture
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if not os.path.exists(CHROME_DIR):
        os.mkdir(CHROME_DIR)

    if not os.path.exists(DRIVERS_DIR):
        os.mkdir(DRIVERS_DIR)

    if not os.path.exists(COOKIE_DIR):
        os.mkdir(COOKIE_DIR)

    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    cookieMg = CookieManager(COOKIE_DIR)
    # Verifier que le fichier existe
    wordMg = WordManager(os.path.join(DATA_DIR, WORD_FILE), os.path.join(DATA_DIR, WORD_LIST_FILE))
    preEarn = PresearchScrapper(os.path.join(dir_run_from, CHROME_DIR, 'chrome'),
                                os.path.join(dir_run_from, DRIVERS_DIR, DRIVER),
                                os.path.join(dir_run_from,DATA_DIR, ACCOUNT_FILE), DEBUG)
    if cookieMg.need_new_cookies():
        preEarn.login(cookieMg.set_cookies)
    else:
        preEarn.set_cookies(cookieMg.get_cookies())

    preEarn.parseSearchLeft()

    preEarn.begin_scrapping(wordMg)

    preEarn.end_search()


if __name__ == '__main__':
    main()
    exit(0)
