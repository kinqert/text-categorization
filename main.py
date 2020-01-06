import sys
import os

from prettytable import PrettyTable
from shutil import copyfile, copytree

from importing import startImport 
from factory.datasetFactory import createDataset
from mbm import createVectors
from log import printAndLog
from result import plotWordsCountForAllDocuments
from training import startTraining

def main():
    print('Welcome to Naive text classifier main program!')
    print('developed by Lorenzo Adreani')

    print('args: ', str(sys.argv))
    loadOperations()

def loadOperations():
    needToBeSplitted = False
    datasetPath = ""
    dataset = None

    for arg in sys.argv:
        if arg == '-s':
            needToBeSplitted = True
        elif arg == '-d':
            datasetPath = sys.argv[sys.argv.index(arg) + 1]
        elif arg == '--generate-tables' or arg == '-g':
            dataset = createDataset(sys.argv[sys.argv.index(arg) + 1])
            startTraining(dataset)
            plotWordsCountForAllDocuments(dataset)
        elif arg == '--show-datasets':
            printDatasets()
        elif arg == '--help':
            printHelp()
            return

    if datasetPath != "":
        importData(datasetPath, needToBeSplitted)

def printDatasets():
    table = PrettyTable()
    table.field_names = ["Datasets"]
    for file in os.listdir("data"):
        table.add_row(file)
    print(table)

def importData(datasetPath, needToBeSplitted):
    if os.path.isdir(sys.path[0] + "/data") is False:
        os.mkdir("data")

    x = PrettyTable()
    x.field_names = ["Category", "#dirs"]

    totData = 0

    for dir in os.listdir(datasetPath):
        if os.path.isdir(datasetPath + dir):
            nData= len(os.listdir(datasetPath + dir))
            totData += nData
            x.add_row([dir, str(nData)])
    
    print(x)
    print("Dimension of dataset(in files):" + str(totData))
    startImport(datasetPath)
    print("Data imported!")


def loadData(datasetPath):
    copytree(datasetPath, sys.path[0] + "/data-000001")


def printHelp():
    print("Questo e' il menu di help")

main()