import sys
import os
import datetime
import time
import Trading
from Logs import Logs
from Parabolic import Parabolic
from Simple import Simple

#to add a new pattern module, modify Constants.Paths and paths.txt
#the pattern class must include functions 
#scan(self, asset, bars, trade) returns Trade or None
#processTrade(self, trade, asset, trade) returns Trade or None

trader = Trading.Trader()
tags = ["link", "xbt", "eth", "xrp", "ltc"]
tag = ""
pattern = None
constantsPath = ""
interval = 0

def start(trader):
    while True:
        print(datetime.datetime.now())
        if(os.path.getsize("data.txt") > 1):
            try:
                print("Processing trade.")
                trader.processTrade(pattern, constantsPath)
            except Exception as e:
                print("Error with processTrade(). Trying again.\n")
                print(e)
        else:
            try: 
                print("Scanning.")
                trader.scan(pattern)
            except Exception as e:
                print("Error with scan. Trying again.\n")
                print(e)
        time.sleep(10)
    
def add(trader, tag, interval, pattern):
    if tag != "" and pattern != None and interval != 0:
        trader.addAsset(Trading.Asset(tag, interval, trader.php, constantsPath))
        tag = ""
        interval = 0
        return 1
    else:
        print("Incorrect syntax, use help.")
        return 0

for arg in sys.argv[1:]:
    if(arg == "testmode"):
        trader.php.TEST_MODE = True
    elif arg == "trade":
        if trader.php.TEST_MODE:
            print("Trading in test mode.")
        else:
            print("Trading without test mode.")
        start(trader)
    elif arg in tags:
        if pattern == None and interval == 0 and tag == "":
            tag = arg
        else:
            print("Incorrect syntax, use help.")
            break
    elif arg == "parabolic":
        if pattern == None and tag != "" and interval != 0:
            pattern = Parabolic()
            constantsPath = trader.paths.PARABOLIC_CONSTANTS_PATH
            ret = add(trader, tag, interval, pattern)
            if ret == 0:
                break
        else: 
            print("Incorrect syntax, use help.")
            break
    elif arg == "simple":
        if pattern == None and tag != "" and interval != 0:
            pattern = Simple()
            constantsPath = trader.paths.SIMPLE_CONSTANTS_PATH
            ret = add(trader, tag, interval, pattern)
            if ret == 0:
                break
        else:
            print("Incorrect syntax, use help.")
            break
    elif arg == "1" or arg == "5" or arg == "15" or arg == "30":
        if tag != "" and pattern == None and interval == 0:
            interval = arg
        else:
            print("Incorrect syntax, use help.")
            break
    elif arg == "H":
        if tag != "" and pattern != None and interval == 0:
            interval = 60
        else:
            print("Incorrect syntax, use help.")
            break
    elif arg == "D":
        if tag != "" and pattern != None and interval == 0:
            interval = 1440
        else:
            print("Incorrect syntax, use help.")
            break
    elif arg == "clear":
        trader.logs.clear()
    elif arg == "help":
        print("Commands: ")
        print("For adding an asset, use: tag interval pattern")
        tagsstr = "Tags:"
        for t in tags:
            tagsstr = tagsstr + " " + t
        print(tagsstr)
        print("Intervals: 1 15 15 30 H D")
        print("Patterns: parabolic simple")
        print("Simple is a manual entry. Patterns work automatically.")
        print("When assets have been added, optionally use command testmode to disable real trades.")
        print("Finally, use command trade.")
        print("Using command clear will clear the trade data file, should only be used in case of a failure.")



    else:
        print("Incorrect syntax, use help.")
        break