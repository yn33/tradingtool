import subprocess
import json
import Trading
from Constants import Constants
from Logs import Logs

class PHP:

    TEST_MODE = False

    def getOHLC(self, asset, interval):
        output = subprocess.run([Constants.PHP_PATH, Constants.KRAKEN_PATH, str(asset), str(interval)], capture_output=True, text=True).stdout
        array = json.loads(output)
        return array
    
    def enter(self, asset, stop, buyVolume):
        if TEST_MODE:
            return True
        else:
            output = subprocess.run([Constants.PHP_PATH, Constants.KRAKEN_PATH, str(asset.tag), 'enter', str(stop), str(buyVolume)], capture_output=True, text=True).stdout
            result = json.loads(output).split()
            if result[0] == "OK":
                return True
            if result[0] == "ERR":
                strings = result[0].strip("\n").split()
                string = strings[1]
                Logs().log(string)
                return False
            print("Error with JSON-output at PHP-enter\n")
            Logs().log("Error with JSON-output at PHP-enter")
    
    def raiseStop(self, asset, stop, sellVolume):
        if TEST_MODE:
            return True
        else:
            output = subprocess.run([Constants.PHP_PATH, Constants.KRAKEN_PATH, str(asset.tag), 'goal', str(stop), str(sellVolume)], capture_output=True, text=True).stdout
            result = json.loads(output).split()
            if result[0] == "OK":
                return True
            if result[0] == "ERR":
                strings = result[0].strip("\n").split()
                string = strings[1]
                Logs().log(string)
                return False
            print("Error with JSON-output at PHP-raiseStop\n")
            Logs().log("Error with JSON-output at PHP-raiseStop")