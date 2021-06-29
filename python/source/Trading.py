from source.PHP import PHP
from source.Constants import Paths
from source.Constants import Constants
from source.Logs import Logs
import datetime

class Trader:
    php = PHP()
    assets = []
    logs = Logs()
    paths = Paths("paths.txt")
    logs.setPaths(paths)
    php.setPaths(paths)

    def addAsset(self, asset):
        self.assets.append(asset)

    def scan(self, pattern):
        
        for asset in self.assets:
            bars = Bars(self.php.getOHLC(asset))
            scanResult = pattern.scan(asset, bars, Trade(asset, pattern))
            if scanResult != None:
                self.tryEnter(scanResult)
    
    def tryEnter(self, trade):
        result = self.php.enter(trade.asset.tag, trade.stop, trade.buyVolume)
        if result:
            self.logs.logTrade(trade, datetime.datetime.now())
    
    def processTrade(self, pattern, constantsPath):
        info = self.logs.readTrade()
        tag = info[1]
        if tag != pattern.tag:
            print("Tags do not match, read {} but should be {}".format(tag, pattern.tag))
            return None
        asset = Asset(info[0], int(info[2]), self.php, constantsPath)
        trade = Trade(asset, pattern)
        time = info[3]
        trade.entry = float(info[4])
        trade.stop = float(info[5])
        trade.goal = float(info[6])
        trade.risk = float(info[7])
        trade.buyVolume = float(info[8])
        bars = Bars(asset.php.getOHLC(asset))
        processResult = pattern.processTrade(trade, trade.asset, bars)
        if processResult != None:
            if processResult == False:
                buyFee = trade.buyFee()
                sellFee = trade.sellFee()
                feeR = (buyFee + sellFee)/(trade.risk)
                trade.currR = trade.currR - feeR
                formatted = Logs().formatData([asset.tag, time, trade.entry, trade.stop, 
                trade.goal, trade.currR, trade.risk])
                self.logs.log(formatted)
                self.logs.clear()
            if processResult == True:
                self.tryRaise(trade, time)

    def tryRaise(self, trade, time):
        result = self.php.raiseStop(trade.asset.tag, trade.stop, trade.buyVolume)
        if result:
            self.logs.logTrade(trade, time)
            

class Asset:

    def __init__(self, tag, interval, php, constantsPath):
        self.php = php
        self.tag = tag
        self.interval = interval
        if constantsPath != "":
            self.constants = Constants(constantsPath)
        else:
            print("No constants path for asset {}".format(self.tag))
            return None

class Bar:
    def __init__(self, array):
        self.time = int(array[0])
        self.open = float(array[1])
        self.high = float(array[2])
        self.low = float(array[3])
        self.close = float(array[4])
        self.volume = float(array[6])
        self.change = self.close - self.open

class Bars:

    def __init__(self, array):
        self.bars = []
        self.totalVolume = 0
        self.totalChange = 0
        self.count = 0
        self.chunks = []

        for entry in array:
            if str(type(entry)) == """<class 'source.Trading.Bar'>""":
                bar = entry
            else:
                bar = Bar(entry)
            self.bars.append(bar)
            self.totalVolume += bar.volume
            change = bar.change
            if(change >= 0):
                self.totalChange += change
            else:
                self.totalChange += -change
            self.count += 1
        
    def averageVolume(self):
        return self.totalVolume/self.count

    def averageChange(self):
        return self.totalChange/self.count

    def maxPriceBetween(self, start, stop):
        if start > self.count - 1 or start < 0 or stop > self.count or stop < 0:
            print("Index error at maxPriceBetween\n")
            return None
        i = start + 1
        maxPrice = self.bars[start].high
        while i <= stop:
            if self.bars[i].high > maxPrice:
                maxPrice = self.bars[i].high
            i += 1
        return maxPrice
    
    def minPriceBetween(self, start, stop):
        if start > self.count - 1 or start < 0 or stop > self.count or stop < 0:
            print("Index error at minPriceBetween\n")
            return None
        i = start + 1
        minPrice = self.bars[start].low
        while i <= stop:
            if self.bars[i].low < minPrice:
                minPrice = self.bars[i].low
            i += 1
        return minPrice

    def averagePriceBetween(self, start, stop):
        if start > self.count - 1 or start < 0 or stop > self.count or stop < 0:
            print("Index error at averagePriceBetween\n")
            return None
        i = start
        totalPrice = 0.0
        totalAmount = 0
        while i <= stop:
            totalPrice += self.bars[i].close()
            totalPrice += self.bars[i].open()
            totalAmount += 2
            i += 1
        averagePrice = totalPrice/totalAmount
        return averagePrice


    def toChunks(self, chunkSize):
        chunks = []
        chunk = []
        i = 0
        j = 0
        while i < self.count - chunkSize:
            bar = self.bars[i]
            chunk.append(bar)
            if(j == chunkSize):
                chunkBars = Bars(chunk)
                chunks.append(chunkBars)
                j = 0
                chunk = []
            i += 1
            j += 1
        self.chunks = chunks

    def lowest(self):
        lowest = self.bars[0]
        for bar in self.bars[1:]:
            if(bar.close < lowest.close):
                lowest = bar
        return lowest

    def supports(self, chunkSize):
        if len(self.chunks) == 0:
            self.toChunks(chunkSize)
        lowests = []
        for chunk in self.chunks:
            lowests.append(chunk.lowest())
        return lowests
    
    def highest(self):
        highest = self.bars[0]
        for bar in self.bars[1:]:
            if(bar.close > highest.close):
                highest = bar
        return highest
    
    def resistances(self, chunkSize):
        if len(self.chunks) == 0:
            self.toChunks(chunkSize)
        highests = []
        for chunk in self.chunks:
            highests.append(chunk.highest())
        return highests

    def barAtIndex(self, index):
        if index > self.count - 1 and index < 0:
            print("Index error at Bars.barAtIndex\n")
            return None
        return self.bars[index]

    def countPivots(self, pivots, stop, distance):
        count = 0
        for pivot in pivots:
            low = pivot.close - distance
            high = pivot.close + distance
            if(stop <= high and stop >= low):
                count += 1
        return count

    def parabolicSAR(self):
        highs = list(map(lambda x: x.high, self.bars))
        lows = list(map(lambda x: x.low, self.bars))
        acceleration = 0.02
        maximum = 0.2
        trend = 1
        length = self.count
        prevHigh = highs[0]
        prevLow = lows[0]
        EP = prevHigh
        SARs = [0]*self.count
        SARs[0] = prevLow
        trends = [0]*self.count
        trends[0] = trend
        SAR = prevLow
        i = 1
        while i < self.count:
            currHigh = highs[i]
            currLow = lows[i]
            if trend == 1:
                if SAR > currLow:
                    trend = 0
                    SAR = EP
                    acceleration = 0.02
                    EP = currHigh
            elif trend == 0:
                if SAR < currHigh:
                    trend = 1
                    SAR = EP
                    acceleration = 0.02
                    EP = currLow
            trends[i] = trend
            SARs[i] = SAR
            if trend == 1:
                if currHigh > EP:
                    if acceleration < 0.2:
                        acceleration += 0.02
                    EP = currHigh
            if trend == 0:
                if currLow < EP:
                    if acceleration < 0.2:
                        acceleration += 0.02
                    EP = currLow
            nextSAR = SAR + acceleration*(EP - SAR)
            if trend == 1:
                bound = min(prevLow, currLow)
                if nextSAR > bound:
                    nextSAR = bound
            if trend == 0:
                bound = max(prevHigh, currHigh)
                if nextSAR < bound:
                    nextSAR = bound
            SAR = nextSAR
            i += 1
            prevHigh = currHigh
            prevLow = currLow
        return SARs, trends

class Trade:

    def __init__(self, asset, pattern):
        self.stop = 0
        self.entry = 0
        self.goal = 0
        self.risk = 0
        self.buyVolume = 0
        self.cost = 0
        self.asset = asset
        self.currR = 0
        self.pattern = pattern
    
    def calculateRisk(self):
        if self.entry > 0 and self.stop > 0: 
            self.risk = self.entry - self.stop
        else:
            print("calculateRisk error")
        return self.risk
    
    def calculateBuyVolume(self):
        if self.risk > 0:
            self.buyVolume = self.asset.constants.STOP/self.risk
        else:
            print("calculateBuyVolume error")
        return self.buyVolume
    
    def calculateCost(self):
        if self.buyVolume > 0 and self.entry > 0:
            self.cost = self.entry*self.buyVolume
        else:
            print("calculateCost error")
        return self.cost 
    
    def calculateGoal(self):
        if self.risk > 0 and self.entry > 0:
            self.goal = self.entry + 2*self.risk
            self.roundGoal(self.asset.tag)
        else:
            print("calculateGoal error")
        return self.goal

    def roundGoal(self, tag):
        if tag == 'xbt' or tag == 'eth':
            self.goal = round(self.goal, 1)
        elif tag == 'ltc':
            self.goal = round(self.goal, 2)
        elif tag == 'xrp' or tag == 'link':
            self.goal == round(self.goal, 5)

    def buyFee(self):
        if self.buyVolume == 0:
            print("buyFee error")
        return 0.026*(self.entry*self.buyVolume)
    
    def sellFee(self):
        if self.buyVolume == 0:
            print("sellFee error")
            return 0
        return 0.026*(self.stop*self.buyVolume)







        