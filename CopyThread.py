import sys
import os
import os.path
import threading
import random
from progressbar import *

from shutil import copyfile

# code for future replace of loadData

# Input: datasetPath, splitted;
def startImport(datasetPath):
    path = createDestinationDir()
    createTestTrainDir(path)

    for group in os.listdir(datasetPath):
        files = os.listdir(datasetPath + group)
        nFiles = len(files)
        testFiles = []

        for i in range(0,  int(nFiles * 0.2)):
            random.seed()
            index = random.randrange(0, len(files))
            testFiles.append(files[index])
            files.remove(files[index])

        print("Copying group {}".format(group))

        trainPath = "{}train/{}".format(path, group)
        testPath = "{}test/{}".format(path, group)

        os.mkdir(trainPath)
        os.mkdir(testPath)

        copyFiles(datasetPath + group, files, trainPath)        
        copyFiles(datasetPath + group, testFiles, testPath)

def copyFiles(datasetPath, files, destinationPath):
    bar = ProgressBar(len(files), [Percentage(), Bar()]).start()
    i = 0
    for file in files:
        copyfile("{}/{}".format(datasetPath, file), "{}/{}".format(destinationPath, file))
        i += 1
        bar.update(i)
    
    bar.finish()

def createDestinationDir():
    nrDatasets = len(os.listdir("data"))
    print("creating new dataset folder {}".format(nrDatasets))
    destinationPath = "data/{}/".format(nrDatasets)
    os.mkdir(destinationPath)
    return destinationPath

def createTestTrainDir(destinationPath):
    os.mkdir(destinationPath + "train")
    os.mkdir(destinationPath + "test")
