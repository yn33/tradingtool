class Simple:

    tag = "simple"

    def scan(self, asset, bars, trade):

        print(asset.tag.upper())
        print("Interval: {}".format(asset.interval))
        print("Attempting entry with risk and cost limits preset.")
        ongoingBar = bars.barAtIndex(bars.count - 1)
        trade.entry = ongoingBar.close
        stopMax = trade.entry*(1 - (asset.constants.STOP/asset.constants.COST_HIGH))
        stopMin = trade.entry*(1 - (asset.constants.STOP/asset.constants.COST_LOW))
        print("Stop loss minimum: {}".format(stopMin))
        print("Stop loss maximum: {}".format(stopMax))
        prompt = input("Stop loss at: ")
        trade.stop = float(prompt)
        trade.calculateRisk()
        trade.calculateGoal()
        result = self.simpleEntry(trade)
        return result

    def simpleEntry(self, trade):
        constants = trade.asset.constants
        if trade.risk > 0:
            trade.calculateBuyVolume()
            cost = trade.calculateCost()
            if cost <= constants.COST_HIGH and cost >= constants.COST_LOW:
                print("Entry: {}".format(trade.entry))
                print("Stop: {}".format(trade.stop))
                print("Goal: {}".format(trade.goal))
                print("Cost: {}".format(cost))
                return trade
            else:
                print("Cost was not within limits.")
                print("Cost: {}".format(cost))
                print("Risk: {}".format(trade.risk))
        return None

    def processTrade(self, trade, asset, bars):
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
        elif currClose >= trade.goal:
            newGoal = trade.goal + trade.risk
            oldGoal = trade.goal
            trade.goal = newGoal
            trade.roundGoal(asset.tag)
            trade.stop = oldGoal
            return True
        return None
        

