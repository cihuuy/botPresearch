import datetime
import os
import random
import time

import selenium
from selenium.webdriver.common.keys import Keys

from src import common, Printer
from src.driver import Driver, ChromeInstaller

from src.WordManager import WordManager


class PresearchScrapper:
    URL_PRESEARCH_MAIN_PAGE = "https://presearch.com"
    URL_LOGIN = "https://presearch.com/login"
    URL_REWARD_VIEWER = "https://presearch.com/account/tokens/rewards?page={:n}"

    XPATH_LOGIN_EMAIL = '//input[@name="sambojago8@gmail.com"]'
    XPATH_LOGIN_PASSWORD = '//input[@name="KOntolodon_303"]'
    XPATH_LOGIN_REMEMBER_ME = '//input[@name="remember"]'

    XPATH_MAX_HISTORY_PATH = '//*[@id="main"]/div[3]/div[1]/ul/li[last()-1]/a'
    XPATH_TOKEN_PER_SEARCH = '//*[@id="main"]/div[2]/div[1]/div[1]/div/div'
    XPATH_MAX_SEARCH = '//*[@id="main"]/div[2]/div[1]/div[2]/div/div'
    XPATH_REWARD_TABLE_HISTORY = '//*[@id="main"]/table/tbody'

    XPATH_TOTAL_COIN_EARN = '//*[@id="main"]/div[1]/div[3]/div/div[1]'
    XPATH_COIN_CAN_BE_REDEEM = '//*[@id="main"]/div[1]/div[2]/div/div[1]'
    XPATH_MIN_COIN_TO_REDEEM = '//*[@id="main"]/div[1]/div[1]/div/div[1]'

    XPATH_LOGIN_OR_REGISTER = "//div[contains(text(),'Register or Login')]"

    XPATH_SEARCH_BAR = '//input[@name="q"]'
    XPATH_PRESEARCH_MAIN_PAGE_SEARCH_BAR = '//input[@id="search"]'

    def __init__(self, chromePath: str, driverPath: str, filePath: str = None, debug: bool = False) -> None:

        self.debug = debug

        self.email = None
        self.password = None

        if filePath is not None:
            self.getAccount(filePath)

        self.driver = Driver.get_driver(driverPath, ChromeInstaller(chromePath), 0, not self.debug)
        self.cookies = None

        self.tokenPerSearch = None
        self.maxSearch = None
        self.searchLeft = None

        self.totalCoinEarn = None
        self.reachNbCoinToRedeem = None
        self.coinRedeem = None

    def get_search_state(self) -> None:
        return

    def verifyDriver(self):
        if self.driver is None:
            pass

    def getAccount(self, filePath: str) -> None:
        if (os.path.exists(filePath) == False):
            f = open(filePath, "w+")
            print(
                filePath + "has been created! Please write your email|password in the thame line. Then restart this "
                           "program")
            exit(1)
        accList = [line.rstrip("\n").split("|")
                   for line in open(filePath, "r", encoding='utf-8')]
        if len(accList) == 0:
            print("Error: no account has been provided. Please write in the file your email|pasword in the thame line")
            exit(1)
        if len(accList) > 1:
            print("Warning: Only first account will be used")
        self.email = accList[0][0]
        self.password = accList[0][1]
        return

    def parseSearchLeft(self) -> None:
        self.verifyDriver()
        pageNumber = 1
        nbSearchToday = 0

        self.driver.get(self.URL_REWARD_VIEWER.format(pageNumber))
        common.safePage(self.driver, self.XPATH_MAX_HISTORY_PATH)

        maxHistoryPage = int(self.driver.find_element_by_xpath(self.XPATH_MAX_HISTORY_PATH).text)
        self.tokenPerSearch = float(self.driver.find_element_by_xpath(self.XPATH_TOKEN_PER_SEARCH).text)
        self.maxSearch = int(self.driver.find_element_by_xpath(self.XPATH_MAX_SEARCH).text)

        self.totalCoinEarn = int(self.driver.find_element_by_xpath(self.XPATH_TOTAL_COIN_EARN).text)
        self.coinRedeem = int(self.driver.find_element_by_xpath(self.XPATH_COIN_CAN_BE_REDEEM).text)
        self.reachNbCoinToRedeem = int(self.driver.find_element_by_xpath(self.XPATH_MIN_COIN_TO_REDEEM).text.replace(',', ''))
        formatt = "%Y-%m-%d @ %I:%M %p"
        today = datetime.datetime.utcnow().date()

        havntFinish = True

        # Verify if we don't finish parse search for today or if we reach max search
        while havntFinish and pageNumber <= maxHistoryPage:

            table = self.driver.find_element_by_xpath(self.XPATH_REWARD_TABLE_HISTORY)
            history = table.find_elements_by_xpath(".//tr")

            for row in history:
                rowElements = row.find_elements_by_xpath(".//td")
                dt = datetime.datetime.strptime(rowElements[0].text, formatt)
                if dt.date() != today:
                    havntFinish = False
                    break
                if rowElements[3].text == 'Search Reward':
                    nbSearchToday += 1

            pageNumber += 1

            if pageNumber <= maxHistoryPage and havntFinish:
                self.driver.get(self.URL_REWARD_VIEWER.format(pageNumber))
                common.safePage(self.driver, self.XPATH_MAX_HISTORY_PATH)

        self.searchLeft = self.maxSearch - nbSearchToday
        return

    def login(self, setCookies: classmethod) -> None:
        print(type(setCookies))
        self.driver.get(self.URL_LOGIN)
        common.safePage(self.driver, self.XPATH_LOGIN_EMAIL)

        emailElement = self.driver.find_element_by_xpath(self.XPATH_LOGIN_EMAIL)
        common.guiWriteContentOnElement(emailElement, self.email, True)

        passwordElement = self.driver.find_element_by_xpath(self.XPATH_LOGIN_PASSWORD)
        common.guiWriteContentOnElement(passwordElement, self.password, True)

        # Click remember button to have longer cookies
        self.driver.find_element_by_xpath(self.XPATH_LOGIN_REMEMBER_ME).click()

        # TODO: Find something to make the recaptcha easily

        # Ugly
        current_url = self.driver.current_url
        while current_url != "https://presearch.com/":
            time.sleep(1)
            try:
                current_url = self.driver.current_url
            except:
                pass

        self.cookies = self.driver.get_cookies()
        setCookies(self.cookies)
        return

    def set_cookies(self, cookies: list) -> None:
        self.driver.get(self.URL_LOGIN)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def makeASearch(self, text: str) -> None:
        searchBarElement = None
        try:
            searchBarElement = self.driver.find_element_by_xpath(self.XPATH_SEARCH_BAR)
        except selenium.common.exceptions.NoSuchElementException:
            try:
                searchBarElement = self.driver.find_element_by_xpath(self.XPATH_PRESEARCH_MAIN_PAGE_SEARCH_BAR)
            except selenium.common.exceptions.NoSuchElementException:
                self.driver.get(self.URL_PRESEARCH_MAIN_PAGE)
                common.safePage(self.driver, self.XPATH_PRESEARCH_MAIN_PAGE_SEARCH_BAR)
                searchBarElement = self.driver.find_element_by_xpath(self.XPATH_PRESEARCH_MAIN_PAGE_SEARCH_BAR)
        # Mettre exept pour prendre les erreurs
        assert (searchBarElement is not None)

        searchBarElement.clear()
        time.sleep(1)
        common.guiWriteContentOnElement(searchBarElement, text)
        time.sleep(1)
        searchBarElement.send_keys(Keys.ENTER)
        common.safePage(self.driver, self.XPATH_SEARCH_BAR)
        return

    def begin_scrapping(self, wordMg: WordManager, updateCallback: staticmethod = None):
        if self.searchLeft is None:
            print("You must login before")
            exit(1)

        elif self.searchLeft == 0:
            print("All searches has been complete")
            exit(0)
        else:
            print("Search begin Now!")
            print()
            pb = Printer.ProgressBar(text="Make search", total_items=self.maxSearch, eta=False)
            pb.start()
            print("Searching...")
            pb.print()
            while self.searchLeft > 0:
                wordToSearch = wordMg.getRandomText()
                Printer.clearMutilines(2)
                print("Searching: ", wordToSearch)
                pb.set_progress(self.maxSearch - self.searchLeft)
                pb.print()
                self.makeASearch(wordToSearch)
                try:
                    registerButtons = self.driver.find_elements_by_xpath(self.XPATH_LOGIN_OR_REGISTER)
                    time.sleep(2)
                    for registerButton in registerButtons:
                        try:
                            registerButton.click()
                        except:
                            pass
                except:
                    pass
                self.searchLeft -= 1
                Printer.clearMutilines(2)
                print("Searching: ", wordToSearch)
                pb.set_progress(self.maxSearch - self.searchLeft)
                pb.print()
                if (self.searchLeft > 0):
                    timeToWait = random.randint(5, 120)
                    time.sleep(timeToWait)
                if (self.searchLeft % 4) == 0:
                    self.parseSearchLeft()

            Printer.clearMutilines(2)
            print("Search complete")
            pb.finish()
            print()
            if self.totalCoinEarn is not None:
                print("Coin earn today %d, total coins %d, and need %d more coins to redeem".format((self.maxSearch - self.searchLeft)*self.tokenPerSearch), self.totalCoinEarn, self.reachNbCoinToRedeem - self.coinRedeem)

    def makeLikeIAmHuman(self):
        pass

    def end_search(self):
        self.driver.quit()
