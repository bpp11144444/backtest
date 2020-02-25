from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smashortPeriod,smalongPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__shortsma = ma.SMA(self.__prices, smashortPeriod)
        self.__longsma = ma.SMA(self.__prices, smalongPeriod)

    def getshortSMA(self):
        return self.__shortsma

    def getlongSMA(self):
        return self.__longsma
    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
    def getshares(self):
        self.getBroker().getShares(self.__instrument)
    def onBars(self, bars):
        # get shares holding now
        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        if shares == 0 and cross.cross_above(self.__shortsma, self.__longsma) > 0:

            sharesToBuy = int(self.getBroker().getCash() / bar.getClose())

            self.marketOrder(self.__instrument, sharesToBuy,False,False)


        elif shares > 0 and cross.cross_below(self.__shortsma, self.__longsma) > 0:

            self.marketOrder(self.__instrument, -1*shares)

