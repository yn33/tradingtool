import sys
import os
import time
import Trading
from PHP import PHP
from Constants import Paths

tag = "eth"
php = PHP()
php.TEST_MODE = True
paths = Paths("paths.txt")
php.setPaths(paths)
constantsPath = paths.TEST_CONSTANTS_PATH
testprevPath = paths.TESTPREV_PATH
testsPath = sys.argv[1]
intervals = [15]
pattern = Trading.Pattern()
counter = 0
prev = False

def runScan(asset, barsArray, reverseArray, SARArray, trendsArray, constants):
    totalR = 0
    count = 0
    trades = 0
    while count < len(barData) - 2:
        bars = barsArray[count]
        scanResult = asset.pattern.testScan(asset, bars, SARArray[count], trendsArray[count], constants)
        if scanResult != None:
            stop = scanResult.stop
            goal = scanResult.goal
            entry = scanResult.entry
            risk = scanResult.risk
            buyVolume = scanResult.buyVolume
            remaining = reverseArray[count]
            for bar in remaining.bars:
                currLow = bar.low
                currHigh = bar.high
                currR = (currLow - entry)/risk    
                if currLow <= stop:
                    currR = currR - (0.026*(entry*buyVolume))/risk - (0.026*(stop*buyVolume))/risk
                    totalR += currR
                    trades += 1
                    break
                elif currLow >= goal:
                    oldGoal = goal
                    goal = goal + risk
                    stop = oldGoal
        count += 1
    average = 0
    if trades > 0:    
        average = totalR/trades
    return average
    
f = open(testprevPath, "r")
line = f.read()
f.close()
array = line.split()
PREV_TESTPATH = array[0]

for interval in intervals:
    printCount = 999
    asset = Trading.Asset(tag, pattern, interval, php, constantsPath)
    barData = php.getOHLC(asset)
    i = 2
    barsArray = []
    reverseArray = []
    SARArray = []
    trendsArray = []
    print("Initializing bar data...")
    while i < len(barData):
        bars1 = Trading.Bars(barData[:i])
        bars2 = Trading.Bars(barData[i:])
        SARs, trends = bars1.parabolicSAR()
        barsArray.append(bars1)
        reverseArray.append(bars2)
        SARArray.append(SARs)
        trendsArray.append(trends)
        i += 1
    print("Initialized.")
    VOLUME_LEVEL = asset.constants.VOLUME_LEVEL
    CHANGE_LEVEL = asset.constants.CHANGE_SCALE
    SCORE_LEVEL = asset.constants.SCORE_LEVEL
    AMOUNT_OF_BARS = asset.constants.AMOUNT_OF_BARS
    CHUNK_SIZE = asset.constants.CHUNK_SIZE
    PIVOT_DIST_BAR_LENGTHS = asset.constants.PIVOT_DIST_BAR_LENGTHS
    CHANGE_SCALE = asset.constants.CHANGE_SCALE
    VOLUME_SCALE = asset.constants.VOLUME_SCALE
    SUPPORT_SCALE = asset.constants.SUPPORT_SCALE
    RESISTANCE_SCALE = asset.constants.RESISTANCE_SCALE

    PREV_VOLUME = 0.0
    PREV_CHANGE = 0.0
    PREV_SCORE = 0.0
    PREV_AMOUNT = 0.0
    PREV_CHUNK = 0.0
    PREV_PIVOT = 0.0
    PREV_CSCALE = 0.0
    PREV_VSCALE = 0.0
    PREV_SUPP = 0.0
    PREV_RES = 0.0

    if PREV_TESTPATH == testsPath:
        PREV_INTERVAL = float(array[1])
        if interval == PREV_INTERVAL:
            print("Setting previous values.")
            prev = True
            PREV_VOLUME = float(array[2])
            PREV_CHANGE = float(array[3])
            PREV_SCORE = float(array[4])
            PREV_AMOUNT = float(array[5])
            PREV_CHUNK = float(array[6])
            PREV_PIVOT = float(array[7])
            PREV_CSCALE = float(array[8])
            PREV_VSCALE = float(array[9])
            PREV_SUPP = float(array[10])
            PREV_RES = float(array[11])

            PREV_VOLUME = PREV_VOLUME - VOLUME_LEVEL
            PREV_CHANGE = PREV_CHANGE - CHANGE_LEVEL
            PREV_SCORE = PREV_SCORE - SCORE_LEVEL
            PREV_AMOUNT = PREV_AMOUNT - AMOUNT_OF_BARS
            PREV_CHUNK = PREV_CHUNK - CHUNK_SIZE
            PREV_PIVOT = PREV_PIVOT - PIVOT_DIST_BAR_LENGTHS
            PREV_CSCALE = PREV_CSCALE - CHANGE_SCALE
            PREV_VSCALE = PREV_VSCALE - VOLUME_SCALE
            PREV_SUPP = PREV_SUPP - SUPPORT_SCALE
            PREV_RES = PREV_RES - RESISTANCE_SCALE

    print("Starting tests.")
    VOLUME_LEVEL_OFFSET = 0.0
    if prev:
        VOLUME_LEVEL_OFFSET = PREV_VOLUME
    while VOLUME_LEVEL_OFFSET <= 5.0:
        asset.constants.VOLUME_LEVEL = VOLUME_LEVEL + VOLUME_LEVEL_OFFSET
        CHANGE_LEVEL_OFFSET = 0.0
        if prev:
            CHANGE_LEVEL_OFFSET = PREV_CHANGE
        while CHANGE_LEVEL_OFFSET <= 5.0:
            asset.constants.CHANGE_LEVEL = CHANGE_LEVEL + CHANGE_LEVEL_OFFSET
            SCORE_LEVEL_OFFSET = 0.0
            if prev:
                SCORE_LEVEL_OFFSET = PREV_SCORE
            while SCORE_LEVEL_OFFSET <= 10.0:
                asset.constants.SCORE_LEVEL = SCORE_LEVEL + SCORE_LEVEL_OFFSET
                AMOUNT_OF_BARS_OFFSET = 0.0
                if prev:
                    AMOUNT_OF_BARS_OFFSET = PREV_AMOUNT
                while AMOUNT_OF_BARS_OFFSET <= 10.0:
                    asset.constants.AMOUNT_OF_BARS = AMOUNT_OF_BARS + AMOUNT_OF_BARS_OFFSET
                    CHUNK_SIZE_OFFSET = 0.0
                    if prev:
                        CHUNK_SIZE_OFFSET = PREV_CHUNK
                    while CHUNK_SIZE_OFFSET <= 0.0:
                        asset.constants.CHUNK_SIZE = CHUNK_SIZE + CHUNK_SIZE_OFFSET
                        PIVOT_DIST_OFFSET = 0.0
                        if prev:
                            PIVOT_DIST_OFFSET = PREV_PIVOT
                        while PIVOT_DIST_OFFSET <= 1.0:
                            asset.constants.PIVOT_DIST_BAR_LENGTHS = PIVOT_DIST_BAR_LENGTHS + PIVOT_DIST_OFFSET
                            CHANGE_SCALE_OFFSET = 0.0
                            if prev:
                                CHANGE_SCALE_OFFSET = PREV_CSCALE
                            while CHANGE_SCALE_OFFSET <= 2.0:
                                asset.constants.CHANGE_SCALE = CHANGE_SCALE + CHANGE_SCALE_OFFSET
                                VOLUME_SCALE_OFFSET = 0.0
                                if prev:
                                    VOLUME_SCALE_OFFSET = PREV_VSCALE
                                while VOLUME_SCALE_OFFSET <= 2.0:
                                    asset.constants.VOLUME_SCALE = VOLUME_SCALE + VOLUME_SCALE_OFFSET
                                    SUPPORT_SCALE_OFFSET = 0.0
                                    if prev:
                                        SUPPORT_SCALE_OFFSET = PREV_SUPP
                                    while SUPPORT_SCALE_OFFSET <= 2.0:
                                        asset.constants.SUPPORT_SCALE = SUPPORT_SCALE + SUPPORT_SCALE_OFFSET
                                        RESISTANCE_SCALE_OFFSET = 0.0
                                        if prev:
                                            RESISTANCE_SCALE_OFFSET = PREV_RES
                                            prev = False
                                        while RESISTANCE_SCALE_OFFSET <= 2.0:
                                            asset.constants.RESISTANCE_SCALE = RESISTANCE_SCALE + RESISTANCE_SCALE_OFFSET
                                        
                                            result = runScan(asset, barsArray, reverseArray, SARArray, trendsArray, asset.constants)
                                            resultString = "{} {} {} {} {} {} {} {} {} {} {} {} ".format(
                                            interval,
                                            asset.constants.VOLUME_LEVEL,
                                            asset.constants.CHANGE_LEVEL,
                                            asset.constants.SCORE_LEVEL,
                                            asset.constants.AMOUNT_OF_BARS,
                                            asset.constants.CHUNK_SIZE,
                                            asset.constants.PIVOT_DIST_BAR_LENGTHS,
                                            asset.constants.CHANGE_SCALE,
                                            asset.constants.VOLUME_SCALE,
                                            asset.constants.SUPPORT_SCALE,
                                            asset.constants.RESISTANCE_SCALE,
                                            result)
                                            printCount += 1
                                            if printCount == 1000:
                                                print(resultString)
                                                printCount = 0
                                            f = open(testsPath, "a")
                                            f.write(resultString + '\n')
                                            f.close()
                                            f = open(testprevPath, "w")
                                            f.write(testsPath + " " + resultString)
                                            f.close()
                                            counter += 1

                                            RESISTANCE_SCALE_OFFSET += 0.5
                                        SUPPORT_SCALE_OFFSET += 0.5
                                    VOLUME_SCALE_OFFSET += 0.5
                                CHANGE_SCALE_OFFSET += 0.5
                            PIVOT_DIST_OFFSET += 0.5
                        CHUNK_SIZE_OFFSET += 5
                    AMOUNT_OF_BARS_OFFSET += 1
                SCORE_LEVEL_OFFSET += 1
            CHANGE_LEVEL_OFFSET += 1
        VOLUME_LEVEL_OFFSET += 1

f = open(testprevPath, "w")
f.write("0")
f.close()
print("Scans finished, ran {} scans.".format(counter))



    