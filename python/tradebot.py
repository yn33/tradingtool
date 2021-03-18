import sys
import os
import datetime
import time
import Trading
from Logs import Logs

trader = Trading.Trader()
tag = ""
pattern = None

def start(trader):
    while True:
        print(datetime.datetime.now())
        if(os.path.getsize("data.txt") > 1):
            try:
                trader.processTrade()
            except Exception as e:
                print("Error with processTrade(). Trying again.\n")
                print(e)
        else:
            try: 
                trader.scan()
            except Exception as e:
                print("Error with scan. Trying again.\n")
                print(e)
        time.sleep(10)

for arg in sys.argv[1:]:
    if(arg == "trade_testmode"):
        trader.php.TEST_MODE = True
        print("Trading in test mode.")
        start(trader)
    elif arg == "trade":
        print("Trading without test mode.")
        start(trader)
    elif arg == "link" or arg == "xbt" or arg == "eth" or arg == "xrp" or arg == "ltc":
        if pattern == None:
            tag = arg
        else:
            print("Incorrect syntax.")
            break
    elif arg == "pattern":
        pattern = Trading.Pattern()
    elif arg == "simple":
        pattern = Trading.Simple()
    elif arg == "1" or arg == "5" or arg == "15" or arg == "30":
        if tag != "" and pattern != None:
            constantsPath = ""
            if pattern.tag == "pattern":
                constantsPath = trader.paths.PATTERN_CONSTANTS_PATH
            if pattern.tag == "simple":
                constantsPath = trader.paths.SIMPLE_CONSTANTS_PATH
            trader.addAsset(Trading.Asset(tag, pattern, arg, trader.php, constantsPath))
            tag = ""
            pattern = None
        else:
            print("Incorrect syntax, use: tag pattern interval")
            break
    elif arg == "clear":
        trader.logs.clear()
    else:
        print("Incorrect syntax:")
        print(arg)
        break