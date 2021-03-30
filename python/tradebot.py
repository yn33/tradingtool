import sys
import os
import datetime
import time
import Trading
from Logs import Logs

trader = Trading.Trader()
tags = ["link", "xbt", "eth", "xrp", "ltc"]
tag = ""
pattern = None
interval = 0

def start(trader):
    while True:
        print(datetime.datetime.now())
        if(os.path.getsize("data.txt") > 1):
            try:
                print("Processing trade.")
                trader.processTrade()
            except Exception as e:
                print("Error with processTrade(). Trying again.\n")
                print(e)
        else:
            try: 
                print("Scanning.")
                trader.scan()
            except Exception as e:
                print("Error with scan. Trying again.\n")
                print(e)
        time.sleep(10)
    
def add(trader, tag, interval, pattern):
    if tag != "" and pattern != None and interval != 0:
        constantsPath = ""
        if pattern.tag == "pattern":
            constantsPath = trader.paths.PATTERN_CONSTANTS_PATH
        if pattern.tag == "simple":
            constantsPath = trader.paths.SIMPLE_CONSTANTS_PATH
        trader.addAsset(Trading.Asset(tag, pattern, interval, trader.php, constantsPath))
        tag = ""
        pattern = None
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
    elif arg == "pattern":
        if pattern == None and tag != "" and interval != 0:
            pattern = Trading.Pattern()
            ret = add(trader, tag, interval, pattern)
            if ret == 0:
                break
        else: 
            print("Incorrect syntax, use help.")
            break
    elif arg == "simple":
        if pattern == None and tag != "" and interval != 0:
            pattern = Trading.Simple()
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
        print("Patterns: pattern simple")
        print("Simple is a manual entry, pattern is the algorithm.")
        print("When assets have been added, optionally use command testmode to disable real trades.")
        print("Finally, use command trade.")
        print("Using command clear will clear the trade data file, should only be used in case of a failure.")



    else:
        print("Incorrect syntax, use help.")
        break