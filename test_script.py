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
intervals = [15]
pattern = Trading.Pattern()
counter = 0
prev = False

def runScan(asset, barsArray, reverseArray, avgChanges, lastBarChanges, constants):
    totalR = 0
    count = 0
    while count < len(barData) - 2:
        bars = barsArray[count]
        scanResult = asset.pattern.testScan(asset, bars, avgChanges[count], lastBarChanges[count], constants)
        if scanResult != None:
            stop = scanResult.stop
            goal = scanResult.goal
            entry = scanResult.entry
            risk = scanResult.risk
            remaining = reverseArray[count]
            for bar in remaining.bars:
                currLow = bar.low
                currHigh = bar.high
                currR = (currLow - entry)/risk    
                if currLow <= stop:
                    totalR += currR
                    break
                elif currLow >= goal:
                    oldGoal = goal
                    goal = goal + risk
                    stop = oldGoal
        count += 1    
    return totalR
    
for interval in intervals:
    asset = Trading.Asset(tag, pattern, interval, php)
    barData = php.getOHLC(asset)
    i = 2
    barsArray = []
    reverseArray = []
    avgChanges = []
    lastBarChanges = []
    while i < len(barData):
        bars1 = Trading.Bars(barData[:i])
        bars2 = Trading.Bars(barData[i:])
        barsArray.append(bars1)
        reverseArray.append(bars2)
        averageChange = bars1.averageChange()
        lastBar = bars1.barAtIndex(bars1.count - 2)
        lastBarChange = lastBar.change
        avgChanges.append(averageChange)
        lastBarChanges.append(lastBarChange)
        i += 1


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
    TRIGGER_BAR_LENGTHS = asset.constants.TRIGGER_BAR_LENGTHS


    VOLUME_LEVEL_OFFSET = -1
    while VOLUME_LEVEL_OFFSET <= 4:
        asset.constants.VOLUME_LEVEL = VOLUME_LEVEL + VOLUME_LEVEL_OFFSET
        CHANGE_LEVEL_OFFSET = -1
        if not prev and interval == 15 and asset.constants.VOLUME_LEVEL == 1.0:
            CHANGE_LEVEL_OFFSET = -1
            prev = True
        while CHANGE_LEVEL_OFFSET <= 4:
            asset.constants.CHANGE_LEVEL = CHANGE_LEVEL + CHANGE_LEVEL_OFFSET
            SCORE_LEVEL_OFFSET = -4
            if prev:
                SCORE_LEVEL_OFFSET = -3
            while SCORE_LEVEL_OFFSET <= 10:
                asset.constants.SCORE_LEVEL = SCORE_LEVEL + SCORE_LEVEL_OFFSET
                AMOUNT_OF_BARS_OFFSET = -3
                if prev:
                    AMOUNT_OF_BARS_OFFSET = -3
                while AMOUNT_OF_BARS_OFFSET <= 10:
                    asset.constants.AMOUNT_OF_BARS = AMOUNT_OF_BARS + AMOUNT_OF_BARS_OFFSET
                    CHUNK_SIZE_OFFSET = 0
                    if prev:
                        CHUNK_SIZE_OFFSET = 0
                    while CHUNK_SIZE_OFFSET <= 0:
                        asset.constants.CHUNK_SIZE = CHUNK_SIZE + CHUNK_SIZE_OFFSET
                        PIVOT_DIST_OFFSET = 0.0
                        if prev:
                            PIVOT_DIST_OFFSET = 0.0
                        while PIVOT_DIST_OFFSET <= 0.0:
                            asset.constants.PIVOT_DIST_BAR_LENGTHS = PIVOT_DIST_BAR_LENGTHS + PIVOT_DIST_OFFSET
                            CHANGE_SCALE_OFFSET = 0.0
                            if prev:
                                CHANGE_SCALE_OFFSET = 0.0
                            while CHANGE_SCALE_OFFSET <= 0.0:
                                asset.constants.CHANGE_SCALE = CHANGE_SCALE + CHANGE_SCALE_OFFSET
                                VOLUME_SCALE_OFFSET = 0.0
                                if prev:
                                    VOLUME_SCALE_OFFSET = 0.0
                                while VOLUME_SCALE_OFFSET <= 0.0:
                                    asset.constants.VOLUME_SCALE = VOLUME_SCALE + VOLUME_SCALE_OFFSET
                                    SUPPORT_SCALE_OFFSET = 0.0
                                    if prev:
                                        SUPPORT_SCALE_OFFSET = 0.0
                                    while SUPPORT_SCALE_OFFSET <= 0.0:
                                        asset.constants.SUPPORT_SCALE = SUPPORT_SCALE + SUPPORT_SCALE_OFFSET
                                        RESISTANCE_SCALE_OFFSET = 0.0
                                        if prev:
                                            RESISTANCE_SCALE_OFFSET = 0.0
                                        while RESISTANCE_SCALE_OFFSET <= 0.0:
                                            asset.constants.RESISTANCE_SCALE = RESISTANCE_SCALE + RESISTANCE_SCALE_OFFSET
                                            TRIGGER_BAR_LENGTHS_OFFSET = -0.1
                                            if prev:
                                                TRIGGER_BAR_LENGTHS_OFFSET = 0.1
                                                prev = False
                                            while TRIGGER_BAR_LENGTHS_OFFSET <= 0.1:
                                                asset.constants.TRIGGER_BAR_LENGTHS = TRIGGER_BAR_LENGTHS + TRIGGER_BAR_LENGTHS_OFFSET
                                                result = runScan(asset, barsArray, reverseArray, avgChanges, lastBarChanges, asset.constants)
                                                resultString = "{} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(
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
                                                    asset.constants.TRIGGER_BAR_LENGTHS,
                                                    result)
                                                print(resultString)
                                                f = open("tests.txt", "a")
                                                f.write(resultString)
                                                f.close()
                                                counter += 1

                                                TRIGGER_BAR_LENGTHS_OFFSET += 0.1
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

print("Scans finished, ran {} scans.".format(counter))



    