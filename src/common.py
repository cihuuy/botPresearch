import time

import os
import time
import os.path
import random
from os import path
import sys

import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def safePage(driver: selenium.webdriver, waitElement: str = "") -> None:
    noFinish = True
    while noFinish:
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  waitElement)))
            noFinish = False
        except TimeoutException:
            driver.refresh()
        except selenium.common.exceptions.NoSuchElementException:
            driver.refresh()
    return


def guiWriteContentOnElement(element: selenium.webdriver.chrome, text: str, instant: bool = False) -> None:
    if not instant:
        for i in range(0, len(text)):
            element.send_keys(text[i])
            time.sleep((random.randint(1, 20) / 100.0))
    else:
        element.send_keys(text)
    return

def dicotomiaSearch(list, nb):
    min = 0
    max = len(list)
    while True:
        posMid = int(min + (max-min)/2)
        if list[posMid] < nb:
            max = posMid
        elif list[posMid] > nb:
            min = posMid
        elif list[posMid] == nb:
            min = max = posMid
            while(list[min +1] == nb):
                min+=1
            return min
        if min +1 == max:
            return min
        if min == max:
            return min
