from Constants import Constants

class Logs:
    
    dpath = Constants.DATA_PATH
    lpath = Constants.LOG_PATH

    def logTrade(self, trade, time):
        f = open(dpath, "w")
        f.write("{}\n".format(trade.asset.tag))
        f.write("{}\n".format(trade.asset.interval))
        f.write("{}\n".format(time))
        f.write("{}\n".format(trade.entry))
        f.write("{}\n".format(trade.stop))
        f.write("{}\n".format(trade.goal))
        f.write("{}\n".format(trade.risk))
        f.write("{}\n".format(trade.buyVolume))
        f.write("{}\n".format(self.formatData(Constants.getArray() + trade.wData)))
        f.close()
    
    def formatData(self, array):
        string = ""
        for x in array:
            string = string + str(x) + " "
        string = string[:-1]
        return string

    def log(self, string):
        f = open(lpath, "a")
        f.write("{}\n".format(string))
        f.close()

    def clear(self):
        f = open(dpath, "w")
        f.close()

    def readTrade(self):
        info = []
        f = open(dpath, "r")
        for x in f:
            info.append(x.strip("\n"))
        f.close()
        return info