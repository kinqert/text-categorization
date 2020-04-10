import sys
import os
import os.path
import threading
import random

from shutil import copyfile

from util.defaultBar import defaultProgress

# Input: datasetPath, splitted(need to be implementated);
def startImport(args):
    path = createDestinationDir(args.name)
    createTestTrainDir(path)
    datasetFolderPath = args.path[0]

    if args.split is True:
        for group in os.listdir(datasetFolderPath):
            files = os.listdir(f"{datasetFolderPath}/{group}")
            nFiles = len(files)
            testFiles = []

            for i in range(0,  int(nFiles * 0.2)):
                random.seed()
                index = random.randrange(0, len(files))
                testFiles.append(files[index])
                files.remove(files[index])

            print("Copying group {}".format(group))

            trainPath = f"{path}/train/{group}"
            testPath = f"{path}/test/{group}"

            os.mkdir(trainPath)
            os.mkdir(testPath)

            copyFiles(f"{datasetFolderPath}/{group}", files, trainPath)
            copyFiles(f"{datasetFolderPath}/{group}", testFiles, testPath)
    else:
        print("need to be implementated")
def copyFiles(datasetPath, files, destinationPath):
    bar = defaultProgress(len(files)).start()
    i = 0
    for file in files:
        copyfile("{}/{}".format(datasetPath, file), "{}/{}".format(destinationPath, file))
        i += 1
        bar.update(i)
    
    bar.finish()

def createDestinationDir(datasetName):
    if datasetName == None:
        nrDatasets = len(os.listdir("data"))
        datasetName = f"{nrDatasets}"
    else:
        datasetName = datasetName[0]
    

    print(f"creating new dataset folder {datasetName}")
    destinationPath = f"{sys.path[0]}/data/{datasetName}"
    os.mkdir(destinationPath)
    return destinationPath

def createTestTrainDir(destinationPath):
    os.mkdir(f"{destinationPath}/train")
    os.mkdir(f"{destinationPath}/test")
