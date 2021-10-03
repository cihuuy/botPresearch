import sys
import time

try:
    from time import monotonic
except ImportError:
    from time import time as monotonic

HIDE_CURSOR = '\x1b[?25l'
SHOW_CURSOR = '\x1b[?25h'

class ProgressBar:
    total_items = 10
    max_bar_lenght = 20
    title = ""
    fillsymbol = " "
    symbol = ("#",)
    braketLeft = "["
    braketRight = "]"

    def __init__(self, **kwargs):

        if kwargs.get("total_items"):
            if kwargs.get("total_items") > 0:
                self.total_items = kwargs.get("total_items")
            else:
                raise ValueError

        if kwargs.get("max_bar_lenght"):
            if 0 < kwargs.get("max_bar_lenght") < 200:
                self.max_bar_lenght = kwargs.get("max_bar_lenght")
            else:
                raise ValueError
        else:
            self.max_bar_lenght = 20

        if kwargs.get("text"):
            self.title = kwargs.get("text")
        else:
            self.title = ""

        if kwargs.get("symbol"):
            self.symbol = kwargs.get("symbol")

        if "eta" in kwargs:
            self.etaEnable = kwargs.get("eta")
        else:
            self.etaEnable = True

        self.beginTime = None
        self.nbItems = 0
        self.totalProgressBarState = self.max_bar_lenght * len(self.symbol)

        sys.stdout.write(HIDE_CURSOR)

    def print(self):
        complete = self.nbItems / float(self.total_items)
        itemToShow = int(complete*self.totalProgressBarState)
        percentComplete = int(round(complete*100))
        nbProgressSymbolFull = int(itemToShow/float(len(self.symbol)))
        stateProgressSymbolNotFull = itemToShow%len(self.symbol)

        output = "\r"
        if self.title != "":
            output += self.title + ": "

        output += self.braketLeft + (self.symbol[len(self.symbol)-1] * nbProgressSymbolFull)
        if stateProgressSymbolNotFull != 0 or (len(self.symbol) >1 and itemToShow != self.totalProgressBarState):
            output += self.symbol[stateProgressSymbolNotFull]
            output += (self.fillsymbol * (self.max_bar_lenght - nbProgressSymbolFull - 1))
        else:
            output += (self.fillsymbol * (self.max_bar_lenght-nbProgressSymbolFull))

        output += self.braketRight

        output += " " + " "*(3-len(str(percentComplete))) + str(percentComplete) +"%"
        if self.nbItems != self.total_items and self.etaEnable:
            output += " " + str(self.eta)+'s'

        output += ' '

        sys.stdout.write(output)
        sys.stdout.flush()
        pass

    def add_progress(self, nbItems: int):
        if (self.beginTime is None):
            self.start()
        self.nbItems += nbItems
        if self.nbItems > self.total_items: self.nbItems = self.total_items
        if self.nbItems <0 : self.nbItems = 0

    def set_progress(self, nbItems: int):
        self.nbItems = nbItems
        if self.nbItems > self.total_items: self.nbItems = self.total_items
        if self.nbItems < 0: self.nbItems = 0

    @property
    def eta(self):
        dt = self.beginTime - monotonic()
        percentComplete = self.nbItems / float(self.total_items)
        if percentComplete == 0:
            return 0
        return int((dt*(percentComplete-1))/percentComplete)

    def finish(self):
        self.nbItems = self.total_items
        self.print()
        sys.stdout.write(" Done\n")
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

    def start(self):
        if (self.beginTime is None):
            self.beginTime = monotonic()


class IncrementalBar(ProgressBar):
    braketLeft = "|"
    braketRight = "|"
    if sys.platform.startswith('win'):
        symbol = (u' ', u'▌', u'█')
    else:
        symbol = (' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█')

class PixelBar(IncrementalBar):
    symbol = ('⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿')


class ShadyBar(IncrementalBar):
    symbol = (' ', '░', '▒', '▓', '█')


def clearMutilines(n:int):
    output = " \r" + (" "*100  + "\x1b\x5b\x01\x41\r")* (n-1) + " "*100 + "\r"
    sys.stdout.write(output)
    sys.stdout.flush()


if __name__=="__main__":
    print(42)
    print(1)
    print(38, end="")
    time.sleep(2)
    clearMutilines(3)
    print(8)