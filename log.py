import os
import sys

def appendLog(messagge, name):
    createLogsFolderIfNotExist()
    logFile = open("logs/{}".format(name), "a")
    logFile.write(messagge)
    logFile.close

def printAndLog(message, name):
    print(message)
    appendLog(message, name)

def createLogsFolderIfNotExist():
    if checkLogsFolder() == False:
        os.mkdir("logs")

def checkLogsFolder():
    return os.path.isdir("logs")