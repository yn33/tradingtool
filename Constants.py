class Constants:
    def __init__(self):
        self.VOLUME_LEVEL = 2.0
        self.CHANGE_LEVEL = 2.0
        self.SCORE_LEVEL = 8.0
        self.AMOUNT_OF_BARS = 6.0
        self.CHUNK_SIZE = 10
        self.PIVOT_LEVEL = 1.0
        self.PIVOT_DIST_BAR_LENGTHS = 1.0
        self.CHANGE_SCALE = 2.0
        self.VOLUME_SCALE = 2.0
        self.SUPPORT_SCALE = 1.0
        self.RESISTANCE_SCALE = 1.0
        self.STOP = 0.3
        self.COST_HIGH = 36
        self.COST_LOW = 33

        self.DATA_PATH = "data.txt"
        self.LOG_PATH = "log.txt"
        self.PHP_PATH = "C:/PHP/php"
        self.KRAKEN_PATH = "C:/kraken-api-client-master/php/kraken.php"
    
    def getArray(self):
        array = [self.VOLUME_LEVEL, self.CHANGE_LEVEL, self.SCORE_LEVEL,
                self.AMOUNT_OF_BARS, self.CHUNK_SIZE, self.PIVOT_LEVEL,
                self.PIVOT_DIST_BAR_LENGTHS, self.CHANGE_SCALE, self.VOLUME_SCALE,
                self.SUPPORT_SCALE, self.RESISTANCE_SCALE, self.STOP, self.COST_HIGH,
                self.COST_LOW]
        return array