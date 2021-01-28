from Constants import Paths

class Logs:

    paths = None

    def setPaths(self, paths):
        self.paths = paths

    def logTrade(self, trade, time):
        if self.paths == None:
            print("No paths set at Logs\n")
            return None
        f = open(self.paths.DATA_PATH, "w")
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
        if self.paths == None:
            print("No paths set at Logs\n")
            return None
        f = open(self.paths.LOG_PATH, "a")
        f.write("{}\n".format(string))
        f.close()

    def clear(self):
        if self.paths == None:
            print("No paths set at Logs\n")
            return None
        f = open(self.paths.DATA_PATH, "w")
        f.close()

    def readTrade(self):
        if self.paths == None:
            print("No paths set at Logs\n")
            return None
        array = []
        f = open(self.paths.DATA_PATH, "r")
        for x in f:
            array.append(x.strip("\n"))
        f.close()
        return array
