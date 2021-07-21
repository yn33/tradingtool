import source.Simple as s

class Parabolic:

    tag = "parabolic"

    def testScan(self, asset, bars, SARs, trends, constants, trade):
        c = bars.count
        reversal = 0
        if trends[c - 1] == 1 and (trends[c - 2] == 0 or trends[c - 3] == 0):
            reversal = 1
        if reversal == 1:
            lower = bars.barAtIndex(c - 1).low
            other = bars.barAtIndex(c - 2).low
            if other < lower:
                prevLower = lower
                lower = other
                other = prevLower
            points = Points(bars, constants)
            points.countPoints(lower)
            if points.score >= constants.SCORE_LEVEL and points.barScore >= constants.SCORE_LEVEL/2:
                attempt = 1
                while attempt < 4:
                    if attempt == 1:
                        trade.stop = SARs[c - 1]
                    elif attempt == 2:
                        trade.stop = lower
                    elif attempt == 3:
                        trade.stop = other
                    trade.entry = bars.barAtIndex(c - 1).close
                    trade.calculateRisk()
                    if trade.risk > 0:
                        trade.calculateGoal()
                        trade.calculateBuyVolume()
                        cost = trade.calculateCost()
                        if cost <= constants.COST_HIGH and cost >= constants.COST_LOW:
                            return trade
                    attempt += 1
        return None
    
    def scan(self, asset, bars, trade):
        constants = asset.constants
        c = bars.count
        SARs, trends = bars.parabolicSAR()
        print(asset.tag.upper())
        print("Interval: {}".format(asset.interval))
        print("Past trends: {}, {}, {}, {}, {}".format(trends[c - 1], trends[c - 2], trends[c - 3], trends[c - 4], trends[c - 5]))
        print("Past SARs: {}, {}, {}, {}, {}".format(SARs[c - 1], SARs[c - 2], SARs[c - 3], SARs[c - 4], SARs[c - 5]))
        reversal = 0
        if trends[c - 1] == 1 and (trends[c - 2] == 0 or trends[c - 3] == 0):
            reversal = 1
        if reversal == 1:
            lower = bars.barAtIndex(c - 1).low
            other = bars.barAtIndex(c - 2).low
            if other < lower:
                prevLower = lower
                lower = other
                other = prevLower
            points = Points(bars, constants)
            points.countPoints(lower)
            print("Bar score: {}".format(points.barScore))
            print("Score: {}".format(points.score))
            print("Score level: {}".format(constants.SCORE_LEVEL))
            if points.score >= constants.SCORE_LEVEL and points.barScore >= constants.SCORE_LEVEL/2:
                attempt = 1
                while attempt < 4:
                    if attempt == 1:
                        trade.stop = SARs[c - 1]
                    elif attempt == 2:
                        trade.stop = lower
                    elif attempt == 3:
                        trade.stop = other
                    trade.entry = bars.barAtIndex(c - 1).close
                    trade.calculateRisk()
                    if trade.risk > 0:
                        trade.calculateGoal()
                        trade.calculateBuyVolume()
                        cost = trade.calculateCost()
                        if cost <= constants.COST_HIGH and cost >= constants.COST_LOW:
                            print("Entry: {}\n".format(trade.entry))
                            print("Stop: {}\n".format(trade.stop))
                            print("Cost: {}".format(cost))
                            return trade
                        else:
                            print("Cost was not within limits.")
                            print("Cost: {}".format(cost))
                            print("Risk: {}".format(trade.risk))
                    attempt += 1
        return None

    def processTrade(self, trade, asset, t):
        result = s.Simple().processTrade(trade, asset, t)
        return result

class Points:

    def __init__(self, bars, constants):

        self.bars = bars
        self.constants = constants
        self.score = 0
        self.barScore = 0

    def countPoints(self, pivot):

        i = 2
        changeLevel = self.bars.averageChange()*self.constants.CHANGE_LEVEL
        volumeLevel = self.bars.averageVolume()*self.constants.VOLUME_LEVEL

        while i < self.constants.AMOUNT_OF_BARS + 2 and i <= self.bars.count:
            currentBar = self.bars.barAtIndex(self.bars.count - i)
            if (currentBar.open - currentBar.close) > changeLevel:
                self.barScore += 1*self.constants.CHANGE_SCALE
            if currentBar.volume > volumeLevel and currentBar.open > currentBar.close:
                self.barScore += 1*self.constants.VOLUME_SCALE
                    

            i += 1
            
        distance = self.bars.averageChange()*self.constants.PIVOT_DIST_BAR_LENGTHS
        supportW = self.bars.countPivots(self.bars.supports(self.constants.CHUNK_SIZE), pivot, distance)  
        resistanceW = self.bars.countPivots(self.bars.resistances(self.constants.CHUNK_SIZE), pivot, distance)
        self.score = self.barScore + (supportW*self.constants.SUPPORT_SCALE + resistanceW*self.constants.RESISTANCE_SCALE)


    def resetPoints(self):
        self.score = 0
        self.barScore = 0

