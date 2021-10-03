import os
from urllib.request import urlopen
import ssl
import zipfile
from selenium import webdriver
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.common.exceptions import SessionNotCreatedException
import re

import platform
from src import Printer

class EventListener(AbstractEventListener):
    """Attempt to disable animations"""

    def after_click_on(self, url, driver):
        animation = \
            """
        try { jQuery.fx.off = true; } catch(e) {}
        """
        driver.execute_script(animation)


class ChromeInstaller:
    # get chrome from this aadress: https://download-chromium.appspot.com/
    def __init__(self, path: str) -> None:
        if platform.system() == "Windows":
            if not path.endswith(".exe"):
                path += ".exe"
        if (not os.path.exists(path)) or (not os.path.isfile(path)):
            self.clear_dir(path)
            self.download_chrome(path)
        self.chromeBin = path

    def clear_dir(self, path: str) -> None:
        import shutil
        all_files = os.listdir(os.path.dirname(path))
        for f in all_files:
            if os.path.isfile(os.path.join(os.path.dirname(path), f)):
                os.remove(os.path.join(os.path.dirname(path), f))
            elif os.path.isdir(os.path.join(os.path.dirname(path), f)):
                shutil.rmtree(os.path.join(os.path.dirname(path), f))

    def download_chrome(self, path: str) -> None:
        url = self.create_request()
        try:
            response = urlopen(
                url, context=ssl.SSLContext(ssl.PROTOCOL_TLS)
            )  # context args for mac
        except ssl.SSLError:
            response = urlopen(url)  # context args for mac
        zip_file_path = os.path.join(
            os.path.dirname(path), os.path.basename(url)
        )
        print("Download chrome")
        pb = Printer.IncrementalBar(text="Download chrome browser", total_items=int(response.headers.get('content-length')))

        with open(zip_file_path, 'wb') as zip_file:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                zip_file.write(chunk)
                pb.add_progress(1024)
                pb.print()

        pb.finish()
        print("Unzip archive")
        extracted_dir = os.path.splitext(zip_file_path)[0]
        with zipfile.ZipFile(zip_file_path, "r") as zip_file:
            zip_file.extractall(os.path.dirname(path))
        os.remove(zip_file_path)

        chromeFile = os.listdir(os.path.dirname(path))[0]

        all_files = os.listdir(os.path.join(os.path.dirname(path), chromeFile, ""))
        for f in all_files:
            try:
                os.rename(os.path.join(os.path.dirname(path), chromeFile, f), os.path.join(os.path.dirname(path), f))
                os.chmod(os.path.join(os.path.dirname(path), f), 0o755)
            # for Windows
            except FileExistsError:
                os.replace(os.path.join(os.path.dirname(path), chromeFile, f), os.path.join(os.path.dirname(path), f))

        os.rmdir(os.path.join(os.path.dirname(path), chromeFile))
        print("Finish")

    def create_request(self) -> str:
        preRequest = "https://download-chromium.appspot.com/dl/"
        p = platform.system()
        if p == "Linux":
            preRequest += "Linux"
        elif p == "Windows":
            preRequest += "Win"
        elif p == "Darwin":
            preRequest += "Mac"
        else:
            print("OS not supported")
            exit(1)
        a = platform.architecture()[0]

        if a == "64bit" and not (p == "Darwin"):
            preRequest += "_x64"
        elif a == "32bit" and not (p == "Darwin"):
            pass

        preRequest += "?type=snapshots"

        return preRequest

    def get_file_path(self) -> str:
        return self.chromeBin


class Driver:
    WEB_DEVICE = 0
    MOBILE_DEVICE = 1

    # Microsoft Edge user agents for additional points
    # agent src: https://www.whatismybrowser.com/guides/the-latest-user-agent/edge
    __WEB_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                       "Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63 "
    __MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/88.0.4324.152 Mobile Safari/537.36 EdgA/46.1.2.5140 "

    @staticmethod
    def __download_driver(driver_path: str, system: str, try_count: int = 0) -> None:
        # determine latest chromedriver version
        # version selection faq: http://chromedriver.chromium.org/downloads/version-selection
        try:
            response = urlopen(
                "https://sites.google.com/chromium.org/driver/downloads",
                context=ssl.SSLContext(ssl.PROTOCOL_TLS)
            ).read()
        except ssl.SSLError:
            response = urlopen(
                "https://sites.google.com/chromium.org/driver/downloads"
            ).read()
        # download second latest version,most recent is sometimes not out to public yet

        latest_version = re.findall(
            b"ChromeDriver \d{2,3}\.0\.\d{4}\.\d+", response
        )[try_count].decode().split()[1]
        print('Downloading chromedriver version: ' + latest_version)

        if system == "Windows":
            url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(
                latest_version
            )
        elif system == "Darwin":
            url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_mac64.zip".format(
                latest_version
            )
        elif system == "Linux":
            url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip".format(
                latest_version
            )

        try:
            response = urlopen(
                url, context=ssl.SSLContext(ssl.PROTOCOL_TLS)
            )  # context args for mac
        except ssl.SSLError:
            response = urlopen(url)  # context args for mac
        zip_file_path = os.path.join(
            os.path.dirname(driver_path), os.path.basename(url)
        )

        pb = Printer.IncrementalBar(text="Download chrome driver", total_items=int(response.headers.get('content-length')))

        with open(zip_file_path, 'wb') as zip_file:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                zip_file.write(chunk)
                pb.add_progress(1024)
                pb.print()

        pb.finish()

        print("Unzip archive")
        extracted_dir = os.path.splitext(zip_file_path)[0]
        with zipfile.ZipFile(zip_file_path, "r") as zip_file:
            zip_file.extractall(extracted_dir)
        os.remove(zip_file_path)

        driver = os.listdir(extracted_dir)[0]
        try:
            os.rename(os.path.join(extracted_dir, driver), driver_path)
        # for Windows
        except FileExistsError:
            os.replace(os.path.join(extracted_dir, driver), driver_path)

        os.rmdir(extracted_dir)
        os.chmod(driver_path, 0o755)
        print("Finish")

    @staticmethod
    def get_driver(path: str, chromeIntaller: ChromeInstaller, device: int, headless: bool):
        system = platform.system()
        if system == "Windows":
            if not path.endswith(".exe"):
                path += ".exe"
        if not os.path.exists(path):
            Driver.__download_driver(path, system)

        options = webdriver.ChromeOptions()
        options.binary_location = chromeIntaller.get_file_path()
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1280,1024")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-notifications")
        options.add_argument("disable-infobars")
        options.add_experimental_option(
            "prefs", {
                "profile.default_content_setting_values.geolocation": 1,
                "profile.default_content_setting_values.notifications": 2
            }
        )  # geolocation permission, 0=Ask, 1=Allow, 2=Deny
        if headless:
            options.add_argument("--headless")
        # else:
        #    options.add_argument("--window-position=-2000,0") # doesnt move off screen

        if device == Driver.WEB_DEVICE:
            options.add_argument("user-agent=" + Driver.__WEB_USER_AGENT)
        else:
            options.add_argument("user-agent=" + Driver.__MOBILE_USER_AGENT)

        # we start at try_count = 1 b/c we already downloaded the most recent version
        try_count = 1
        MAX_TRIES = 3
        is_dl_success = False
        while not is_dl_success:
            try:
                driver = webdriver.Chrome(path, options=options)
                is_dl_success = True
            # driver not up to date with Chrome browser, try different ver
            except SessionNotCreatedException:
                if try_count == MAX_TRIES:
                    raise SessionNotCreatedException(
                        f'Tried downloading the {try_count} most recent chromedrivers. None match your Chrome '
                        f'browswer version. Aborting now, please update your chrome browser.')
                Driver.__download_driver(path, system, try_count)
                try_count += 1

        # if not headless:
        #    driver.set_window_position(-2000, 0)
        return EventFiringWebDriver(driver, EventListener())
