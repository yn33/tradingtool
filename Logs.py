from Constants import Paths

class Logs:


    def setPaths(self, path):
        paths = Paths(path)
        self.dpath = paths.DATA_PATH
        self.lpath = paths.LOG_PATH

    def logTrade(self, trade, time):
        f = open(self.dpath, "w")
        f.write("{}\n".format(trade.asset.tag))
        f.write("{}\n".format(trade.asset.interval))
        f.write("{}\n".format(trade.asset.pattern))
        f.write("{}\n".format(time))
        f.write("{}\n".format(trade.entry))
        f.write("{}\n".format(trade.stop))
        f.write("{}\n".format(trade.goal))
        f.write("{}\n".format(trade.risk))
        f.write("{}\n".format(trade.buyVolume))
        f.write("{}\n".format(self.formatData(trade.wData)))
        f.close()
    
    def formatData(self, array):
        string = ""
        for x in array:
            string = string + str(x) + " "
        string = string[:-1]
        return string

    def log(self, string):
        f = open(self.lpath, "a")
        f.write("{}\n".format(string))
        f.close()

    def clear(self):
        f = open(self.dpath, "w")
        f.close()

    def readTrade(self):
        array = []
        f = open(self.dpath, "r")
        for x in f:
            array.append(x.strip("\n"))
        f.close()
        return array

    def readConstants(self, path):
        array = []
        f = open(path, "r")
        for x in f:
            split = x.split(":")
            array.append(split[1].strip("\n"))
        f.close()
        return array