import sys
import os

from collections import namedtuple
from prettytable import PrettyTable
from progressbar import ProgressBar, Percentage, Bar

from log import appendLog, printAndLog

def createVectors(dataseth):
    datasethPath = "data/{}".format(dataseth)
    if os.path.isdir(datasethPath):
        print("Creating multi-variate bernulli model")
        mbmTable = loadTableFromDataseth(datasethPath, "mbm")
        print("Creating multinomial model")
        mmTable = loadTableFromDataseth(datasethPath, "mm")

        printResultTables(mbmTable)
        printResultTables(mmTable)

        print("Done!")



def loadTableFromDataseth(datasethPath, type):
    trainPath = "{}/train".format(datasethPath)

    count = True

    if (type == "mbm"):
        count = False

    groups = []
    totalWords = []
    table = {
        "groups" : groups,
        "totalWords" : totalWords,
        "type" : type
    }
    for group in os.listdir(trainPath):
        group = loadGroup(trainPath, group, count)
        groups.append(group)
        totalWords = getDistictWords(group["dWords"], count, totalWords)

        appendLog(str(group), "group-{}".format(group))

    return table

def printResultTables(table):
    logname = "result-learning"
    printAndLog("Result Learning", logname)

    printTable = PrettyTable()
    printTable.title = table["type"]

    totalWords = 0
    singleWords = 0

    for word in table["totalWords"]:
        if word["count"] == 1:
            singleWords += 1
        printTable.add_column(word["word"], [word["count"]])
        totalWords += 1

   
    printAndLog(str(printTable), logname)
    printAndLog("Total words: {}". format(totalWords))

def loadGroup(trainPath, group, count):
    print("Learning group: {}".format(group))
    groupPath = "{}/{}".format(trainPath, group)
    bar = ProgressBar(len(os.listdir(groupPath)), [Percentage(), Bar()]).start()
    i = 0

    dWords = []
    wordsFiles = []

    group = {
        "group" : group,
        "dWords" : dWords,
        "wordsFiles" : wordsFiles
    }

    for file in os.listdir(groupPath):
        wordsFile = getWordsFromFile("{}/{}".format(groupPath, file), count)
        wordsFiles.append(wordsFile)
        dWords = getDistictWords(wordsFile, count, dWords)

        i += 1
        bar.update(i)
    bar.finish()

    return group

def getWordsFromFile(filePath, count):
    file = open(filePath, "r", encoding= "ISO-8859-1")
    dWords = []

    # modify here for add more rule for splitting 
    for line in file.readlines():
        words = line.split(" ")

        for word in words:
            dWords.append({
                "word" : word,
                "count" : 1
            })
    
    dWords = getDistictWords(dWords, count)

    pathSplitted = filePath.split("/")
    fileName = pathSplitted.pop()
    fileGroup = pathSplitted.pop()

    return dWords


def getDistictWords(words, count, dWords = []):
    #print("get distict words\nfrom: {}\nto: {}".format(str(words), str(dWords)))
    for newWord in words:
        exist = False

        ref = [dword for dword in dWords if dword["word"] == newWord["word"]]
        if (len(ref) >= 2):
            return
        elif (len(ref) == 1):
            exist = True
            if count == True:
                ref[0]["count"] = ref[0]["count"] + 1
        
        if exist == False:
            dWords.append(newWord)
    
    return dWords
