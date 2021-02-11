import sys
import os
import time
import Trading
from Logs import Logs

trader = Trading.Trader()
tag = ""
pattern = None

def start(trader):
    while True:
        if(os.path.getsize("data.txt") > 1):
            trader.processTrade()
        else:
            trader.scan()
        time.sleep(10)

for arg in sys.argv[1:]:
    if(arg == "trade_testmode"):
        trader.php.TEST_MODE = True
        print("Trading in test mode.")
        start(trader)
    elif(arg == "trade"):
        print("Trading without test mode.")
        start(trader)
    elif(arg == "link" or arg == "xbt" or arg == "eth" or arg == "xrp" or arg == "ltc"):
        tag = arg
    elif(arg == "pattern"):
        pattern = Trading.Pattern()
    elif(arg == "simple"):
        pattern = Trading.Simple()
    elif(arg == "1" or arg == "5" or arg == "15" or arg == "30"):
        if(tag != "" and pattern != None):
            trader.addAsset(Trading.Asset(tag, pattern, arg, trader.php))
            tag = ""
            pattern = None
    elif(arg == "clear"):
        trader.logs.clear()
    else:
        print("Incorrect syntax:")
        print(arg)