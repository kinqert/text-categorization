import sys
import os

from collections import namedtuple
from prettytable import PrettyTable
from progressbar import ProgressBar, Percentage, Bar

from log import appendLog

def createVectors(dataseth):
    datasethPath = "data/{}".format(dataseth)
    if os.path.isdir(datasethPath):
        loadFiles(datasethPath)

def loadFiles(datasethPath):
    trainPath = "{}/train".format(datasethPath)
    groupTables = []

    for group in os.listdir(trainPath):
        table = loadGroup(trainPath, group)
        groupTables.append({
            "group" : group,
            "table" : table
        })
        appendLog(str(table), "table-{}".format(group))

    printResultTables(groupTables)
    print("Done!")

def printResultTables(groupTables):
    printTable = PrettyTable()
    printTable.title = "Result learning"
    printTable.field_names = ["Category", "|V|"]
    
    for table in groupTables:
        printTable.add_row([table["group"], len(table["table"])])
    
    print(printTable)
    appendLog(str(printTable), "result-learning")

def loadGroup(trainPath, group):
    print("Learning group: {}".format(group))
    groupPath = "{}/{}".format(trainPath, group)
    bar = ProgressBar(len(os.listdir(groupPath)), [Percentage(), Bar()]).start()
    i = 0
    table = []
    for file in os.listdir(groupPath):

        table += createTable("{}/{}".format(groupPath, file))
        i += 1
        bar.update(i)
    bar.finish()

    return table

def createTable(filePath):
    file = open(filePath, "r", encoding= "ISO-8859-1")
    words = []

    for line in file.readlines():
        words += line.split(" ")
    vWords = []

    for word in words:
        try:
            vWords.index(word)
        except:
            vWords.append(word)
    
    table = PrettyTable()
    table.title = filePath
    table.field_names = vWords

    pathSplitted = filePath.split("/")
    fileName = pathSplitted.pop()
    fileGroup = pathSplitted.pop()

    #for word in vWords:
    #    appendLog(word, "mbm-{}-{}".format(fileGroup, fileName))
    
    return vWords
