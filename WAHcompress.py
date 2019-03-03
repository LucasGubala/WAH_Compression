import csv

nameDict = {                #dictionary for referencing name
    "cat": '1000',
    "dog": '0100',
    "turtle": '0010',
    "bird": '0001'
}

dictAge = {                 #dictionary for referencing age 
    0: '1000000000',
    1: '0100000000',
    2: '0010000000',
    3: '0001000000',
    4: '0000100000',
    5: '0000010000',
    6: '0000001000',
    7: '0000000100',
    8: '0000000010',
    9: '0000000001'
}
class stats:
    OneRuns = 0
    ZeroRuns = 0
    TotalRuns = 0
    Literals = 0


def bitmapGenerator (filename, target):

    out = open(target,'w')      # open target file to be written to
    with open(filename) as f:
        reader = csv.reader(f, delimiter = ',')     # use csv reader to break up file into a list
        for line in reader:             #loop through the list lines
            rowBits = nameDict[line[0]]        #create row string to append onto for output and fill with correct name     
            rowBits = rowBits + dictAge[((int(line[1])-1)//10)]     #reference age dictionary and add onto row output
            if line[2] == "False":                  #adoption true false check
                rowBits = rowBits + "01"            #append onto rowBits for output
            elif line[2] == "True":
                rowBits = rowBits + "10"

            print (rowBits, file= out)          #print out the constructed row to the designated target file
        out.close()             #close the target file



def litChecker(list,wordSize):
    for x in list:
        if x != list[0]:
            return 0
    return 1
        


def compressor(filename,target,wordSize,STATS):
    maxCount = (2**(wordSize-1))-1      #max count that can be held by one fill word
    out = open(target,'w')
    with open(filename) as f:
        lines = f.readlines()
        
        for i in range(0,16):   #scanning across rows horizontally
            runCounter = 0
            runChar = 'N'       #placeholder character of runs
            
            for j in range(0,len(lines),wordSize-1):
                
                if j + (wordSize-1) > len(lines): #literal at end of file that is not even n*wordsize-1 rows
                    endLiteral ='0'
                    for L in range(j,len(lines)):
                        endLiteral += lines[L][i]
                    #print (endLiteral)
                    out.write(endLiteral)
                    STATS.Literals += 1
                    endLiteral = ''
                    continue

                vert=[]
                for x in range(0,wordSize-1):
                    
                    vert.append( lines[j+x][i] )

                if litChecker(vert,wordSize) == 1:  #run 
                    
                    runNum = vert[0]
                    if runNum == runChar and runCounter <= maxCount:
                            runCounter += 1
                    else:
                        if runCounter != 0:
                            doneRun = '1'
                            if runChar == '0':
                                doneRun += '0'
                            elif runChar == '1':
                                doneRun += '1'

                            doneRun += '{0:{wordSize-2}b}'.format(runCounter)
                            #print (doneRun)
                            out.write(doneRun)
                            if runChar == '1':
                                STATS.OneRuns += 1
                            elif runChar == '0':
                                STATS.ZeroRuns += 1
                            STATS.TotalRuns += runCounter
                        runChar = runNum
                        runCounter = 1


                elif litChecker(vert,wordSize) == 0:     #literal
                    if runCounter != 0:
                        doneRun = '1'
                        if runChar == '0':
                            doneRun += '0'
                        elif runChar == '1':
                            doneRun += '1'

                        doneRun += ("{0:0" + str(wordSize-2) + "b}").format(runCounter)
                        #print (doneRun)
                        out.write(doneRun)
                        if runChar == '1':
                            STATS.OneRuns += 1
                        elif runChar == '0':
                            STATS.ZeroRuns += 1
                        STATS.TotalRuns += runCounter

                        runChar = 'N'
                        runCounter = 0


                    #print('0'+''.join(vert))        #print literal
                    out.write('0'+''.join(vert))
                    STATS.Literals += 1
            out.write("\n")
    out.close()


animals_str = "data/animals.txt"
animals_sorted_str = "data/animals.txt"

compressed32 = "compressed32.txt"
compressed64 = "compressed64.txt"

animals = open("data/animals.txt",'r')

animalsSortedList = animals.readlines()
animalsSortedList.sort()

animalsSorted = open("animalsSorted.txt",'w')   #get file for sorted animals
for i in animalsSortedList:
    print (i, file=animalsSorted)
animalsSorted.close()


STATS1 = stats()

bitmapGenerator(animals_str,"bitmapUnsorted.txt")           #generation of unsorted bitmap
bitmapGenerator(animals_sorted_str,"bitmapSorted.txt")       #generation of sorted bitmap

wordSize = 32                   #setting initial word size                   

compressor("bitmapUnsorted.txt",compressed32,wordSize,STATS1)
print ("animals_compressed_32-- ", "Total Runs: ",STATS1.TotalRuns, "One Runs: ",STATS1.OneRuns,"Zero Runs: ", STATS1.ZeroRuns,"Literals: ", STATS1.Literals)
                    