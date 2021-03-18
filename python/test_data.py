import sys
from Constants import Paths
from Constants import Constants

best = [""] * 10
bestValues = [-2000.0] * 10
averages = {}
amounts = {}

for arg in sys.argv[1:]:
    f = open(arg, "r")
    for line in f:

        array = line.split()
        interval = int(array[0])
        volume = float(array[1])
        change = float(array[2])
        score = float(array[3])
        amount = float(array[4])
        chunk = float(array[5])
        pivot = float(array[6])
        cscale = float(array[7])
        vscale = float(array[8])
        supp = float(array[9])
        res = float(array[10])
        trigger = float(array[11])
        value = float(array[12])

        IDString = "{} {} {} {} {} {} {} {} {} {} {} {}"\
        .format(interval, volume, change, score, amount, chunk, pivot, cscale, vscale, supp, res, trigger)

        if IDString in averages.keys():
            oldAverage = averages[IDString]
            oldAmount = amounts[IDString]
            newAverage = oldAverage + (value - oldAverage)/(oldAmount + 1)
            averages[IDString] = newAverage
            amounts[IDString] = oldAmount + 1
        else:
            averages[IDString] = value
            amounts[IDString] = 1
    f.close()
    
for key in averages.keys():
    value = averages[key]
    if value > bestValues[9] and value != 0:
        print(value)
        i = 0
        found = False
        while i < 10:
            if value > bestValues[i]:
                bestValues.insert(i, value)
                best.insert(i, key)
                bestValues.pop(10)
                best.pop(10)
                found = True
            if found:
                break
            i += 1

for x in range(10):
    array = best[x].split()
    interval = int(array[0])
    volume = float(array[1])
    change = float(array[2])
    score = float(array[3])
    amount = float(array[4])
    chunk = float(array[5])
    pivot = float(array[6])
    cscale = float(array[7])
    vscale = float(array[8])
    supp = float(array[9])
    res = float(array[10])
    trigger = float(array[11])
    n = amounts[key]
    value = bestValues[x]
    resString = "{}. In: {}, Vo: {}, Ch: {}, Sc: {}, Am: {}, Chu: {}, Pi: {}, Cs: {}, Vs: {}, Su: {}, Res: {}, Tri: {}, Avg: {}, N: {}"\
    .format(x + 1, interval, volume, change, score, amount, chunk, pivot, cscale, vscale, supp, res, trigger, value, n)
    print(resString)
    if x == 0:
        paths = Paths("paths.txt")
        constants = Constants(paths.PATTERN_CONSTANTS_PATH)
        pivotlevel = constants.PIVOT_LEVEL
        stop = constants.STOP
        costhigh = constants.COST_HIGH
        costlow = constants.COST_LOW

        f = open(paths.PATTERN_CONSTANTS_PATH, "w")
        f.write("VOLUME_LEVEL={}\n".format(volume))
        f.write("CHANGE_LEVEL={}\n".format(change))
        f.write("SCORE_LEVEL={}\n".format(score))
        f.write("AMOUNT_OF_BARS={}\n".format(amount))
        f.write("CHUNK_SIZE={}\n".format(chunk))
        f.write("PIVOT_LEVEL={}\n".format(pivotlevel))
        f.write("PIVOT_DIST_BAR_LENGTHS={}\n".format(pivot))
        f.write("CHANGE_SCALE={}\n".format(cscale))
        f.write("VOLUME_SCALE={}\n".format(vscale))
        f.write("SUPPORT_SCALE={}\n".format(supp))
        f.write("RESISTANCE_SCALE={}\n".format(res))
        f.write("STOP={}\n".format(stop))
        f.write("COST_HIGH={}\n".format(costhigh))
        f.write("COST_LOW={}\n".format(costlow))
        f.write("TRIGGER_BAR_LENGTHS={}".format(trigger))
        f.close()
        
