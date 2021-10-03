import random
import linecache

from src.common import dicotomiaSearch


class WordManager:
    def __init__(self, filename: str, wordfilename: str):
        self.filename = filename
        self.wordfilename = wordfilename
        self.queryList = None

    def getRandomTextFile(self) -> str:
        text = None
        with open(self.filename, "r") as f:
            lineNumber = random.randint(0, sum(1 for _ in f) - 1)
        text = linecache.getline(self.filename, lineNumber)
        return text[:-1]

    def getRandomText(self) -> str:
        try:
            from pytrends.request import TrendReq
        except ImportError:
            return self.getRandomTextFile()

        if random.random() < 0.0:
            return self.getRandomTextFile()
        else:
            return self.getRandomTrends()

    def updateQueryList(self):
        from pytrends.request import TrendReq
        from math import ceil
        wordList = list()
        with open(self.wordfilename, "r") as f:
            wordList = f.read().split('\n')
        listRelatedQuery = list()
        pytrend = TrendReq()
        for i in range(ceil(len(wordList)/5)):
            pytrend.build_payload(kw_list=wordList[i*5:(i+1)*5])
            related_queries = pytrend.related_queries()
            for word in wordList[i*5:(i+1)*5]:
                try:
                    myList = related_queries[word]['top']['value'].tolist()
                    listRelatedQuery += related_queries[word]['top']['query'].tolist()[:dicotomiaSearch(myList, 40) + 1]
                except:
                    pass
        self.queryList = listRelatedQuery

    def getRandomTrends(self):
        if self.queryList is None:
            self.updateQueryList()
        return random.choice(self.queryList)
