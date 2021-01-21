import sys
import os
from Trading import Trader
from Trading import Asset

trader = Trader()
tag = ""

for arg in sys.argv[1:]:
    if(arg == "trade_testmode"):
        trader.php.TEST_MODE = True
        print("Trading in test mode.")
        print("\n")
        if(os.path.getsize("data.txt") > 1):
            "a"#processTrade()
        else:
            trader.scan()
    elif(arg == "trade"):
        print("Trading without test mode.")
        print("\n")
        if(os.path.getsize("data.txt") > 1):
            "a"#processTrade()
        else:
            trader.scan()
    elif(arg == "link" or arg == "xbt" or arg == "eth" or arg == "xrp" or arg == "ltc"):
        tag = arg
    elif(arg == "1" or arg == "5" or arg == "15" or arg == "30"):
        if(tag != ""):
            trader.addAsset(Asset(tag, arg))
    elif(arg == "clear"):
        "a"#clear()
    else:
        print("Incorrect syntax.")
        print("\n")