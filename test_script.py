import sys
import os
import time
import Trading
from PHP import PHP
from Constants import Paths

tag = "eth"
php = PHP()
php.TEST_MODE = True
paths = Paths("constants/paths.txt")
php.setPaths(paths)
interval = 5
pattern = Trading.Pattern()
asset = Trading.Asset(tag, pattern, interval, php)
count = 2
barData = php.getOHLC(asset)
totalR = 0

while count < len(barData):
    bars = Trading.Bars(barData[:count])
    scanResult = asset.pattern.scan(asset, bars)
    if scanResult != None:
        scanResult.asset = asset
        stop = scanResult.stop
        goal = scanResult.goal
        entry = scanResult.entry
        risk = scanResult.risk
        remaining = Trading.Bars(barData[count:])
        for bar in remaining.bars:
            currLow = bar.low
            currHigh = bar.high
            currR = (currLow - entry)/risk    
            if currLow <= stop:
                totalR += currR
                print(currR)
                break
            elif currHigh >= goal:
                goal = goal + risk
                stop = goal
                break
    count += 1

print(totalR)





    