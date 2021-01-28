def readConstants(path):
    array = []
    f = open(path, "r")
    for x in f:
        split = x.split()
        array.append(split[1].strip("\n"))
    f.close()
    return array

class Constants:
    
    def __init__(self, path):

        array = readConstants(path)

        self.VOLUME_LEVEL = float(array[0])
        self.CHANGE_LEVEL = float(array[1])
        self.SCORE_LEVEL = float(array[2])
        self.AMOUNT_OF_BARS = float(array[3])
        self.CHUNK_SIZE = int(array[4])
        self.PIVOT_LEVEL = float(array[5])
        self.PIVOT_DIST_BAR_LENGTHS = float(array[6])
        self.CHANGE_SCALE = float(array[7]) 
        self.VOLUME_SCALE = float(array[8])
        self.SUPPORT_SCALE = float(array[9])
        self.RESISTANCE_SCALE = float(array[10])
        self.STOP = float(array[11])
        self.COST_HIGH = float(array[12])
        self.COST_LOW = float(array[13])
    
    def getArray(self):
        array = [self.VOLUME_LEVEL, self.CHANGE_LEVEL, self.SCORE_LEVEL,
                self.AMOUNT_OF_BARS, self.CHUNK_SIZE, self.PIVOT_LEVEL,
                self.PIVOT_DIST_BAR_LENGTHS, self.CHANGE_SCALE, self.VOLUME_SCALE,
                self.SUPPORT_SCALE, self.RESISTANCE_SCALE, self.STOP, self.COST_HIGH,
                self.COST_LOW]
        return array


class Paths:

    def __init__(self, path):

        array = readConstants(path)
        
        self.DATA_PATH = array[0]
        self.LOG_PATH = array[1]
        self.PHP_PATH = array[2]
        self.KRAKEN_PATH = array[3]