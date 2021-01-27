from Logs import Logs

class Constants:
    
    def __init__(self, path):

        array = Logs().readConstants(path)

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

        paths = Logs().readConstants(path)
        
        self.DATA_PATH = paths[1]
        self.LOG_PATH = paths[2]
        self.PHP_PATH = paths[3]
        self.KRAKEN_PATH = paths[4]