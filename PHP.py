import subprocess
import json
import Trading
from Constants import Paths
from Logs import Logs

class PHP:

    TEST_MODE = False
    paths = None
    
    def setPaths(self, paths):
        self.paths = paths

    def getOHLC(self, asset):
        if self.paths == None:
            print("No paths set at PHP")
            return None
        output = subprocess.run([self.paths.PHP_PATH, self.paths.KRAKEN_PATH, str(asset.tag), str(asset.interval)], capture_output=True, text=True).stdout
        array = json.loads(output)
        return array
    
    def enter(self, asset, stop, buyVolume):
        if self.TEST_MODE:
            return True
        else:
            if self.paths == None:
                print("No paths set at PHP")
                return None
            output = subprocess.run([self.paths.PHP_PATH, self.paths.KRAKEN_PATH, str(asset.tag), 'enter', str(stop), str(buyVolume)], capture_output=True, text=True).stdout
            result = json.loads(output).split()
            if result[0] == "OK":
                return True
            if result[0] == "ERR":
                strings = result[0].strip("\n").split()
                string = strings[1]
                Logs().log(string)
                return False
            print("Error with JSON-output at PHP-enter")
            Logs().log("Error with JSON-output at PHP-enter")
    
    def raiseStop(self, asset, stop, sellVolume):
        if self.TEST_MODE:
            return True
        else:
            if self.paths == None:
                print("No paths set at PHP")
                return None
            output = subprocess.run([self.paths.PHP_PATH, self.paths.KRAKEN_PATH, str(asset.tag), 'goal', str(stop), str(sellVolume)], capture_output=True, text=True).stdout
            result = json.loads(output).split()
            if result[0] == "OK":
                return True
            if result[0] == "ERR":
                strings = result[0].strip("\n").split()
                string = strings[1]
                Logs().log(string)
                return False
            print("Error with JSON-output at PHP-raiseStop")
            Logs().log("Error with JSON-output at PHP-raiseStop")