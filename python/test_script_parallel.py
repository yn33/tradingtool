import sys
import os
import time
import math
import multiprocessing as mp
import source.Trading as Trading
from source.PHP import PHP
from source.Constants import Paths
from source.Constants import Constants
from source.Parabolic import Parabolic


def runScan(asset, pattern, barsArray, reverseArray, SARArray, trendsArray, constants, dataLen):
    totalR = 0
    trades = 0
    count = 0
    while count < dataLen - 2:
        bars = barsArray[count]
        scanResult = pattern.testScan(asset, bars, SARArray[count], trendsArray[count], constants, Trading.Trade(asset, pattern))
        if scanResult != None:
            stop = scanResult.stop
            goal = scanResult.goal
            entry = scanResult.entry
            risk = scanResult.risk
            buyVolume = scanResult.buyVolume
            remaining = reverseArray[count]
            for bar in remaining.bars:
                currLow = bar.low
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
    
def main():

    tag = "eth"
    php = PHP()
    php.TEST_MODE = True
    paths = Paths("paths.txt")
    php.setPaths(paths)
    constantsPath = paths.TEST_CONSTANTS_PATH
    testsPath = sys.argv[1]
    barDataPath = sys.argv[2]
    intervals = [15]
    pattern = Parabolic()
    cpucount = mp.cpu_count()
    print("Number of processors used: ", cpucount)


    for interval in intervals:
        
        asset = Trading.Asset(tag, interval, php, constantsPath)
        print("Initializing bar data...")
        barData = []
        if barDataPath == "API":
            barData = php.getOHLC(asset)
        else:
            barDataFile = open(barDataPath, 'r')
            dataString = barDataFile.read()  
            dataRows = dataString.split('\n')
            for row in dataRows:
                if row != '':
                    rowSplit = row.split(',')
                    barData.append(rowSplit)
            barDataFile.close()
        dataLen = len(barData)
        print("Bar data loaded, size: {}".format(dataLen))

        nRuns = 1
        if dataLen > 1000:
            nRuns = int(dataLen/1000)
        
        k = 0
        while k < nRuns:
            
            print("Bars {}-{} of {}".format(k*1000, (k + 1)*1000, dataLen))
            currBarData = []
            if nRuns == 1:
                currBarData = barData
            else:
                currBarData = barData[(dataLen-(k+1)*1000):(dataLen-k*1000)]
            currDataLen = len(currBarData)
            barsArray = []
            reverseArray = []
            SARArray = []
            trendsArray = []
            maxOffsetV = 5.0
            offsetChangeV = 1.0
            maxOffsetC = 7.0
            offsetChangeC = 1.0
            partitionSize = math.ceil((int(maxOffsetC/offsetChangeC + 1))/cpucount)
            r = []
            i = 0
            while i < cpucount:
                j = 0
                partition = []
                while j < partitionSize:
                    if (j + i*partitionSize)*offsetChangeC <= maxOffsetC:
                        partition.append((j + i*partitionSize)*offsetChangeC)
                    j += 1
                if len(partition) > 0:
                    r.append(partition)
                i += 1
            checkSum = 0
            for x in r:
                checkSum += len(x)
            if checkSum != int(maxOffsetC/offsetChangeC + 1):
                print("Partition error.")    
                print(checkSum)
                print(int(maxOffsetC/offsetChangeC + 1))
                exit()
            i = 2
            print("Creating data arrays...")
            
            while i < currDataLen:
                bars1 = Trading.Bars(currBarData[:i])
                bars2 = Trading.Bars(currBarData[i:])
                SARs, trends = bars1.parabolicSAR()
                barsArray.append(bars1)
                reverseArray.append(bars2)
                SARArray.append(SARs)
                trendsArray.append(trends)
                i += 1
            print("Initialized.")
            print("Starting tests.")
            volumeOffset = 0.0
            print("Starting with volume offset {}".format(volumeOffset))
            while volumeOffset <= maxOffsetV:
                volumeOffset += offsetChangeV
                q = mp.Queue()
                jobs = []
                for partition in r:
                    printStr = "Starting partition with volume offset {} and change offsets:".format(volumeOffset)
                    for x in partition:
                        printStr = printStr + " {}".format(x)
                    print(printStr)
                    p = mp.Process(target=runPartition, args=(volumeOffset, partition, asset, pattern, interval, q, constantsPath, barsArray, reverseArray, SARArray, trendsArray, currDataLen))
                    p.start()
                    jobs.append(p)
                testf = open(testsPath, "a")
                for job in jobs:
                    while job.is_alive():
                        while not q.empty():
                            testf.write(q.get())
                testf.close()
                print("All partitions finished for this volume offset, results written to file.")
    k += 1

def runPartition(volumeOffset, partition, asset, pattern, interval, q, constantsPath, barsArray, reverseArray, SARArray, trendsArray, dataLen):
    for x in partition:
        runTest(volumeOffset, x, asset, pattern, interval, q, constantsPath, barsArray, reverseArray, SARArray, trendsArray, dataLen)
        
def runTest(VOLUME_LEVEL_OFFSET, CHANGE_LEVEL_OFFSET, asset, pattern, interval, q, constantsPath, barsArray, reverseArray, SARArray, trendsArray, dataLen):

    printCount = 999
    counter = 0
    constants = Constants(constantsPath)
    VOLUME_LEVEL = constants.VOLUME_LEVEL
    CHANGE_LEVEL = constants.CHANGE_SCALE
    SCORE_LEVEL = constants.SCORE_LEVEL
    AMOUNT_OF_BARS = constants.AMOUNT_OF_BARS
    CHUNK_SIZE = constants.CHUNK_SIZE
    PIVOT_DIST_BAR_LENGTHS = constants.PIVOT_DIST_BAR_LENGTHS
    CHANGE_SCALE = constants.CHANGE_SCALE
    VOLUME_SCALE = constants.VOLUME_SCALE
    SUPPORT_SCALE = constants.SUPPORT_SCALE
    RESISTANCE_SCALE = constants.RESISTANCE_SCALE 

    constants.VOLUME_LEVEL = VOLUME_LEVEL + VOLUME_LEVEL_OFFSET
    constants.CHANGE_LEVEL = CHANGE_LEVEL + CHANGE_LEVEL_OFFSET
    SCORE_LEVEL_OFFSET = 0.0
    while SCORE_LEVEL_OFFSET <= 10.0:
        constants.SCORE_LEVEL = SCORE_LEVEL + SCORE_LEVEL_OFFSET
        AMOUNT_OF_BARS_OFFSET = 0.0
        while AMOUNT_OF_BARS_OFFSET <= 10.0:
            constants.AMOUNT_OF_BARS = AMOUNT_OF_BARS + AMOUNT_OF_BARS_OFFSET
            CHUNK_SIZE_OFFSET = 0.0
            while CHUNK_SIZE_OFFSET <= 0.0:
                constants.CHUNK_SIZE = CHUNK_SIZE + CHUNK_SIZE_OFFSET
                PIVOT_DIST_OFFSET = 0.0
                while PIVOT_DIST_OFFSET <= 1.0:
                    constants.PIVOT_DIST_BAR_LENGTHS = PIVOT_DIST_BAR_LENGTHS + PIVOT_DIST_OFFSET
                    CHANGE_SCALE_OFFSET = 0.0
                    while CHANGE_SCALE_OFFSET <= 2.0:
                        constants.CHANGE_SCALE = CHANGE_SCALE + CHANGE_SCALE_OFFSET
                        VOLUME_SCALE_OFFSET = 0.0
                        while VOLUME_SCALE_OFFSET <= 2.0:
                            constants.VOLUME_SCALE = VOLUME_SCALE + VOLUME_SCALE_OFFSET
                            SUPPORT_SCALE_OFFSET = 0.0
                            while SUPPORT_SCALE_OFFSET <= 2.0:
                                constants.SUPPORT_SCALE = SUPPORT_SCALE + SUPPORT_SCALE_OFFSET
                                RESISTANCE_SCALE_OFFSET = 0.0
                                while RESISTANCE_SCALE_OFFSET <= 2.0:
                                    constants.RESISTANCE_SCALE = RESISTANCE_SCALE + RESISTANCE_SCALE_OFFSET
                                            
                                    result = runScan(asset, pattern, barsArray, reverseArray, SARArray, trendsArray, constants, dataLen)
                                    resultString = "{} {} {} {} {} {} {} {} {} {} {} {} ".format(
                                    interval,
                                    constants.VOLUME_LEVEL,
                                    constants.CHANGE_LEVEL,
                                    constants.SCORE_LEVEL,
                                    constants.AMOUNT_OF_BARS,
                                    constants.CHUNK_SIZE,
                                    constants.PIVOT_DIST_BAR_LENGTHS,
                                    constants.CHANGE_SCALE,
                                    constants.VOLUME_SCALE,
                                    constants.SUPPORT_SCALE,
                                    constants.RESISTANCE_SCALE,
                                    result)
                                    printCount += 1
                                    if printCount == 1000:
                                        print(resultString)
                                        printCount = 0
                                    q.put(resultString + '\n')
                                    counter += 1

                                    RESISTANCE_SCALE_OFFSET += 0.5
                                SUPPORT_SCALE_OFFSET += 0.5
                            VOLUME_SCALE_OFFSET += 0.5
                        CHANGE_SCALE_OFFSET += 0.5
                    PIVOT_DIST_OFFSET += 0.5
                CHUNK_SIZE_OFFSET += 5
            AMOUNT_OF_BARS_OFFSET += 1
        SCORE_LEVEL_OFFSET += 1
    print("Scans finished, ran {} scans.".format(counter))

if __name__ == '__main__':
    main()