import datetime
import os
import pickle


class CookieManager:
    def __init__(self, filePath: str = None) -> None:
        if filePath is None:
            print('You must register cookies in a dir')
            exit(1)
        self.filePath = filePath
        self.cookies = None
        self.endDate = None

    def update(self) -> None:
        minAge = int(datetime.datetime.now().timestamp()) + 60 * 60 * 1.5
        filename = ""

        fileList = os.listdir(self.filePath)
        for file in fileList:
            try:
                if file.endswith(".txt") and int(file[:-4]) > minAge:
                    minAge = int(file[:-4])
                    filename = file
            except:
                pass
        if filename != '':
            self.cookies = pickle.load(open(os.path.join(self.filePath, filename), "rb"))
            self.endDate = datetime.datetime.fromtimestamp(minAge)

    def get_cookies(self) -> list:
        if self.cookies is None:
            self.update()
        return self.cookies

    def get_end_time(self) -> datetime.datetime:
        if self.cookies is None:
            self.update()
        return self.endDate

    def set_cookies(self, cookies: list) -> None:
        filename = ""
        if cookies != list():
            if len(cookies) > 0:
                for cookie in cookies:
                    if cookie['name'] == "presearch_session":
                        self.endDate = datetime.datetime.fromtimestamp(cookie['expiry'])
                        self.cookies = cookies
                        filename = cookie['expiry']

                if filename != '':
                    pickle.dump(cookies, open(os.path.join(self.filePath, str(int(filename))) + '.txt', "wb"))

    def clear_useless_cookie_file(self) -> None:
        pass

    def need_new_cookies(self) -> bool:
        if self.get_end_time() is None:
            return True
        return False
