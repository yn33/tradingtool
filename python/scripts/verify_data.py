import sys

def main():
    filename = sys.argv[1]
    index = int(sys.argv[2])
    f = open(filename, "r")
    values = []
    counts = []
    for line in f:
        splitLine = line.split()
        value = splitLine[index]
        found = False
        for i in range(len(values)):
            if values[i] == value:
                counts[i] += 1
                found = True
        if not found:
            values.append(value)
            counts.append(1)
    
    firstTarget = counts[0]
    verified = True
    for count in counts:
        if count != firstTarget:
            verified = False

    for i in range(len(values)):
        print("Value: {}, count: {}".format(values[i], counts[i]))
    if verified:
        print("Verification successful.")
    else:
        print("Verification failed.")


   
if __name__ == '__main__':
    main()     

