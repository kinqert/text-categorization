import os
import sys

def appendLog(messagge, group):
    createLogsFolderIfNotExist()
    logFile = open("logs/{}".format(group), "a")
    logFile.write(messagge)
    logFile.close

def createLogsFolderIfNotExist():
    if checkLogsFolder() == False:
        os.mkdir("logs")

def checkLogsFolder():
    return os.path.isdir("logs")