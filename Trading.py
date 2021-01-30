from PHP import PHP
from Constants import Constants
from Constants import Paths
import datetime
from Logs import Logs

class Trader:
    php = PHP()
    assets = []
    logs = Logs()
    paths = Paths("constants/paths.txt")
    logs.setPaths(paths)
    php.setPaths(paths)

    def addAsset(self, asset):
        self.assets.append(asset)

    def scan(self):
        for asset in self.assets:
            scanResult = asset.pattern.scan(asset)
            if scanResult != None:
                scanResult.asset = asset
                self.tryEnter(scanResult)
    
    def tryEnter(self, trade):
        result = self.php.enter(trade.asset.tag, trade.stop, trade.buyVolume)
        if result:
            self.logs.logTrade(trade, datetime.datetime.now)
    
    def processTrade(self):
        info = self.logs.readTrade()
        trade = Trade()
        asset = Asset(info[0], info[1], self.php, info[2])
        time = info[3]
        trade.entry = info[4]
        trade.stop = info[5]
        trade.goal = info[6]
        trade.risk = info[7]
        trade.buyVolume = info[8]
        analytics = info[9]
        processResult = asset.pattern.processTrade(trade, asset)
        if processResult != None:
            if processResult == False:
                formatted = Logs().formatData([asset.tag, time, trade.entry, trade.stop, 
                trade.goal, trade.currR, trade.risk, analytics])
                self.logs.log(formatted)
            if processResult == True:
                self.tryRaise(trade, time)

    def tryRaise(self, trade, time):
        result = self.php.raiseStop(trade.asset, trade.stop, trade.buyVolume)
        if result:
            self.logs.logTrade(trade, time)
            

class Asset:

    def __init__(self, tag, pattern, interval, php):
        self.php = php
        self.tag = tag
        self.interval = interval
        self.pattern = pattern
        constantsPath = "constants/{}.txt".format(pattern.tag)
        self.constants = Constants(constantsPath)

class DipPattern:

    tag = "dip"

    def scan(self, asset):
        constants = asset.constants
        bars = Bars(asset.php.getOHLC(asset))
        averageChange = bars.averageChange()
        lastBar = bars.barAtIndex(bars.count - 2)
        lastBarChange = lastBar.change
        print(asset.tag.upper())
        print("Interval: {}".format(asset.interval))
        print("Average change: {}".format(averageChange))
        print("Last bar change: {}".format(lastBarChange))
        if lastBarChange < averageChange:
            points = Points(bars, asset)
            trade = points.countPoints()
            trade.wData = points.getwData()
            trade.asset = asset
            risk = trade.calculateRisk()
            if trade.entry >= trade.trigger and risk > 0 and points.score >= constants.SCORE_LEVEL and points.barScore >= constants.SCORE_LEVEL/2:
                trade.calculateBuyVolume()
                cost = trade.calculateCost()
                print("Cost: {}".format(cost))
                if cost <= constants.COST_HIGH and cost >= constants.COST_LOW:
                    return trade
        return None

    def processTrade(self, trade, asset):
        result = SimplePattern().processTrade(trade, asset)
        return result

class SimplePattern:

    tag = "simple"

    def scan(self, asset):
        constants = asset.constants
        bars = Bars(asset.php.getOHLC(asset))
        print(asset.tag.upper())
        print("Interval: {}".format(asset.interval))
        print("Attempting entry with stop at minimum of last 2 bars, with risk and cost limits preset.")
        points = Points(bars, asset)
        trade = points.countPoints()
        trade.asset = asset
        risk = trade.calculateRisk()
        if trade.entry >= trade.trigger and risk > 0:
            trade.calculateBuyVolume()
            cost = trade.calculateCost()
            print("Cost: {}".format(cost))
            if cost <= constants.COST_HIGH and cost >= constants.COST_LOW:
                return trade
    
    def processTrade(self, trade, asset):
        bars = Bars(asset.php.getOHLC(asset))
        currBar = bars.barAtIndex(bars.count - 1)
        currHigh = currBar.high
        currClose = currBar.close
        trade.currR = (currClose - trade.entry)/trade.risk
        print(asset.tag.upper())
        print("Entry: {}".format(trade.entry))
        print("Stop: {}".format(trade.stop))
        print("Goal: {}".format(trade.goal))
        print("Current price: {}".format(currClose))
        print("Current high: {}".format(currHigh))
        print("R: {}".format(trade.risk))
        print("Current R: {}".format(trade.currR))
        if currClose <= trade.stop and currClose != 0.0:
            originalStop = trade.entry - trade.risk
            trade.stop = originalStop
            return False
        elif currClose > trade.goal:
            newGoal = trade.goal + trade.risk
            oldGoal = trade.goal
            trade.goal = newGoal
            trade.roundGoal(asset.tag)
            trade.stop = oldGoal
            return True
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
            if str(type(entry)) == """<class 'Trading.Bar'>""":
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
        if index <= self.count - 1 and index >= 0:
            return self.bars[index]
        else:
            print("Index error at Bars.barAtIndex")
            return None

    def countPivots(self, pivots, stop, distance):
        count = 0
        for pivot in pivots:
            low = pivot.close - distance
            high = pivot.close + distance
            if(stop <= high and stop >= low):
                count += 1
        return count
        



class Points:

    def __init__(self, bars, asset):

        self.bars = bars
        self.constants = asset.constants
        self.pattern = asset.pattern
        self.score = 0
        self.barScore = 0
        self.volumeW = 0
        self.changeW = 0
        self.supportW = 0
        self.resistanceW = 0

    def countPoints(self):
        tag = self.pattern.tag
        if(tag == "dip"):
            result = dip(self)
        if(tag == "simple"):
            result = simple(self)
        return result

    def simple(self):

        ongoingBar = self.bars.barAtIndex(self.bars.count - 1)
        trade = Trade()
        trade.stop = min(ongoingBar.low, self.bars.barAtIndex(self.bars.count - 2).low) 
        trade.entry = ongoingBar.close
        #constants can have different meanings when using different patterns
        trade.trigger = ongoingBar.open + self.constants.CHANGE_LEVEL
        return trade
    
    def dip(self):

        ongoingBar = self.bars.barAtIndex(self.bars.count - 1)
        trade = Trade()
        trade.stop = min(ongoingBar.low, self.bars.barAtIndex(self.bars.count - 2).low) 
        trade.entry = ongoingBar.close
        trade.trigger = ongoingBar.open

        i = 2
        changeLevel = self.bars.averageChange()*self.constants.CHANGE_LEVEL
        volumeLevel = self.bars.averageVolume()*self.constants.VOLUME_LEVEL

        while i < self.constants.AMOUNT_OF_BARS + 2:
            currentBar = self.bars.barAtIndex(self.bars.count - i)
            if (currentBar.open - currentBar.close) > changeLevel:
                self.score += 1*self.constants.CHANGE_SCALE
                self.barScore += 1*self.constants.CHANGE_SCALE
                self.changeW += 1
            if currentBar.volume > volumeLevel and currentBar.open > currentBar.close:
                self.score += 1*self.constants.VOLUME_SCALE
                self.barScore += 1*self.constants.VOLUME_SCALE
                self.volumeW += 1
            i += 1
        
        distance = self.bars.averageChange()*self.constants.PIVOT_DIST_BAR_LENGTHS
        self.supportW = self.bars.countPivots(self.bars.supports(self.constants.CHUNK_SIZE), trade.stop, distance)  
        self.resistanceW = self.bars.countPivots(self.bars.resistances(self.constants.CHUNK_SIZE), trade.stop, distance)
        self.score += (self.supportW*self.constants.SUPPORT_SCALE + self.resistanceW*self.constants.RESISTANCE_SCALE)
        print("Change bars: {}".format(self.changeW))
        print("Volume bars: {}".format(self.volumeW))
        print("Supports: {}".format(self.supportW))
        print("Resistances: {}".format(self.resistanceW))

        return trade

    def resetPoints(self):
        self.score = 0
        self.barScore = 0
        self.volumeW = 0
        self.changeW = 0
        self.supportW = 0
        self.resistanceW = 0

    def getwData(self):
        return [self.changeW, self.volumeW, self.supportW, self.resistanceW]

class Trade:

    def __init__(self):
        self.stop = 0
        self.entry = 0
        self.goal = 0
        self.risk = 0
        self.trigger = 0
        self.buyVolume = 0
        self.cost = 0
        self.asset = None
        self.currR = 0
        self.wData = []
    
    def calculateRisk(self):
        self.risk = self.entry - self.stop
        return self.risk
    
    def calculateBuyVolume(self):
        if self.risk > 0:
            self.buyVolume = self.asset.constants.STOP/self.risk
        return self.buyVolume
    
    def calculateCost(self):
        if self.buyVolume > 0 and self.entry > 0:
            self.cost = self.entry*self.buyVolume
        return self.cost 
    
    def calculateGoal(self):
        if self.risk > 0 and self.entry > 0:
            self.goal = self.entry + 2*self.risk
            self.roundGoal(self.asset.tag)
        return self.goal

    def roundGoal(self, tag):
        if tag == 'xbt' or tag == 'eth':
            self.goal = round(self.goal, 1)
        elif tag == 'ltc':
            self.goal = round(self.goal, 2)
        elif tag == 'xrp' or tag == 'link':
            self.goal == round(self.goal, 5)







        