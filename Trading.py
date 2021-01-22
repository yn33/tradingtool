from PHP import PHP
from Constants import Constants
import datetime
from Logs import Logs

class Trader:
    php = PHP()
    assets = []

    def addAsset(self, asset):
        self.assets.append(asset)

    def scan(self):
        for asset in self.assets:
            scanResult = asset.scan()
            if scanResult != None:
                scanResult.asset = asset
                tryEnter(scanResult)
    
    def tryEnter(self, trade):
        result = self.php.enter(trade.asset.tag, trade.stop, trade.buyVolume)
        if result:
            Logs.logTrade(trade, datetime.datetime.now)
    
    def processTrade(self):
            info = Logs.readTrade()
            trade = Trade()
            asset = Asset(info[0], info[1], self.php)
            time = info[2]
            trade.entry = info[3]
            trade.stop = info[4]
            trade.goal = info[5]
            trade.risk = info[6]
            trade.buyVolume = info[7]
            analytics = info[8]
            processResult = asset.processTrade(trade)
            if processResult != None:
                if processResult. == False:
                    formatted = Logs.formatData[asset.tag, time, trade.entry, trade.stop, 
                    trade.goal, trade.currR, trade.risk, analytics]
                    Logs.log(formatted)
                if processResult == True:
                    tryRaise(trade, time)

    def tryRaise(self, trade, time):
        result = self.php.raiseStop(trade.asset, trade.stop, trade.buyVolume)
        if result:
            Logs.logTrade(trade, time)
            



class Asset:

    def __init__(self, tag, interval, php)
        self.php = PHP()
        self.tag = tag
        self.interval = interval

    def scan(self):
        bars = Bars(self.php.getOHLC(self.tag, self.interval))
        averageChange = bars.averageChange
        lastBar = bars.barAtIndex(bars.count - 2)
        lastBarChange = lastBar.change
        print(self.tag.upper() + "\n")
        print("Interval: {}\n".format(self.interval))
        print("Average change: {}\n".format(averageChange))
        print("Last bar change: {}\n".format(lastBarChange))
        if lastBarChange < averageChange:
            points = Points(bars)
            trade = points.countPoints 
            trade.wData = points.getwData
            trade.asset = self
            risk = trade.calculateRisk
            if trade.entry >= trade.trigger and risk > 0 and points.score >= Constants.SCORE_LEVEL and points.barScore >= Constants.SCORE_LEVEL/2:
                buyVolume = trade.calculateBuyVolume
                cost = trade.calculateCost
                print("Cost: {}\n".format(cost))
                if cost <= Constants.COST_HIGH and cost >= Constants.COST_LOW:
                    return trade
        return None

    def processTrade(self, trade):
        bars = Bars(self.php.getOHLC(self.tag, self.interval))
        currBar = bars.barAtIndex(bars.count - 1)
        currHigh = currBar.high
        currClose = currBar.close
        trade.currR = (currClose - trade.entry)/trade.risk
        goal = trade.goal
        print(self.tag.upper() + "\n")
        print("Entry: {}\n".format(trade.entry))
        print("Stop: {}\n".format(trade.stop))
        print("Goal: {}\n").format(goal))
        print("Current price: {}\n".format(currClose))
        print("Current high: {}\n".format(currClose))
        print("R: {}\n".format(trade.risk))
        print("Current R: {}\n".format(currR))
        if currClose <= trade.stop and currClose != 0.0:
            originalStop = trade.entry - trade.risk
            trade.stop = originalStop
            return False
        elif currClose > trade.goal
            newGoal = trade.goal + trade.risk
            trade.goal = newGoal
            trade.stop = goal
            return True


class Bar:
    def __init__(self, array):
        self.time = array[0]
        self.open = array[1]
        self.high = array[2]
        self.low = array[3]
        self.close = array[4]
        self.volume = array[6]
        self.change = self.open - self.close

class Bars:
    bars = []
    totalVolume = 0
    totalChange = 0
    count = 0
    def __init__(self, array):
        for entry in array:
            bar = Bar(entry)
            self.bars.append(bar)
            totalVolume += bar.volume
            change = bar.change
            if(change >= 0):
                totalChange += change
            else:
                totalChange += -change
            count += 1
        
    def averageVolume(self):
        return totalVolume/count

    def averageChange(self):
        return totalChange/count

    def toChunks(self, chunkSize):
        chunks = []
        chunk = []
        i = 0
        j = 0
        while i < count - chunkSize:
            bar = self.bars[i]
            chunk += bar
            if(j == chunkSize):
                chunks += Bars(chunk)
                j = 0
                chunk = []
            i += 1
            j += 1
        return chunks

    def lowest(self):
        lowest = self.bars[0]
        for bar in self.bars[1:]:
            if(bar.close < lowest.close):
                lowest = bar
        return lowest

    def supports(self, chunks):
        lowests = []
        for chunk in chunks:
            lowests += chunk.lowest
        return lowests
    
    def highest(self):
        highest = self.bars[0]
        for bar in self.bars[1:]:
            if(bar.close > highest.close):
                highest = bar
        return highest
    
    def resistances(self, chunks):
        highests = []
        for chunk in chunks:
            highests += chunk.highest
        return highests

    def barAtIndex(self, index):
        if index <= self.count - 1 and index >= 0:
            return self.bars(index)
        else:
            print("Index error at Bars.barAtIndex\n")
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

    score = 0
    barScore = 0
    volumeW = 0
    changeW = 0
    supportW = 0
    resistanceW = 0

    def __init__(self, bars):
        self.bars = bars
    
    def countPoints(self):

        ongoingBar = self.bars.barAtIndex(count - 1)
        trade = Trade()
        trade.stop = min(ongoingBar.low, self.bar.barAtIndex(count - 2).low) 
        trade.entry = ongoingBar.close
        trade.trigger = ongoingBar.open

        i = 2
        changeLevel = self.bars.averageChange*CHANGE_LEVEL
        volumeLevel = self.bars.averageVolume*VOLUME_LEVEL

        while i < Constants.AMOUNT_OF_BARS + 2:
            currentBar = self.bars.barAtIndex(count - i)
            if (currentBar.open - currentBar.close) > changeLevel:
                self.score += 1*Constants.CHANGE_SCALE
                self.barScore += 1*Constants.CHANGE_SCALE
                self.changeW += 1
            if currentBar.volume > volumeLevel and currentBar.open > currentBar.close:
                self.score += 1*Constants.VOLUME_SCALE
                self.barScore += 1*Constants.VOLUME_SCALE
                self.volumeW += 1
            i += 1

        distance = self.bars.averageChange*Constants.PIVOT_DIST_BAR_LENGTHS
        self.supportW = countPivots(self.bars.supports, trade.stop, distance)  
        self.resistanceW = countPivots(self.bars.resistances, trade.stop, distance)
        self.score += (self.supportW*Constants.SUPPORT_SCALE + self.resistanceW*Constants.RESISTANCE_SCALE)

        print("Change bars: {}\n".format(self.changeW))
        print("Volume bars: {}\n".format(self.volumeW))
        print("Supports: {}\n".format(self.supportW))
        print("Resistances: {}\n".format(self.resistanceW))

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

    stop = 0
    entry = 0
    goal = 0
    risk = 0
    trigger = 0
    buyVolume = 0
    cost = 0
    asset = None
    currR = 0
    wData = []
    
    def calculateRisk(self):
        self.risk = self.entry - self.stop
        return self.risk
    
    def calculateBuyVolume(self):
        if self.risk > 0:
            self.buyVolume = Constants.STOP/self.risk
        return self.buyVolume
    
    def calculateCost(self):
        if self.buyVolume > 0 and self.entry > 0:
            self.cost = self.entry*self.buyVolume
        return self.cost 
    
    def calculateGoal(self):
        if self.risk > 0 and self.entry > 0:
            self.goal = self.entry + 2*self.risk
            if self.tag == 'xbt' or tag == 'eth':
                self.goal = round(self.goal, 1)
            elif self.tag == 'ltc':
                self.goal = round(self.goal, 2)
            elif self.tag == 'xrp' or self.tag == 'link':
                self.goal == round(self.goal, 5)
        return self.goal







        