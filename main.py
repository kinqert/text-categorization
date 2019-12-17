import sys
import os
from prettytable import PrettyTable

def main():
    print('Welcome to text classifier main program!')
    print('developed by Lorenzo Adreani')

    print('args: ', str(sys.argv))
    loadOperations()

def loadOperations():
    needToBeSplitted = False
    datasetPath = ""
    for arg in sys.argv:
        if arg == '-s':
            needToBeSplitted = True
        elif arg == '-d':
            datasetPath = sys.argv[sys.argv.index(arg) + 1]
        elif arg == '--help':
            printHelp()
            return
    importData(datasetPath, needToBeSplitted)

def importData(datasetPath, needToBeSplitted):
    # os.mkdir("data")

    x = PrettyTable()
    x.field_names = ["Category", "#dirs"]

    totData = 0

    for dir in os.listdir(datasetPath):
        if os.path.isdir(datasetPath + dir):
            nData = len(os.listdir(datasetPath + dir))
            totData += nData
            x.add_row([dir, str(nData)])
    
    print(x)
    print("Dimension of dataset(in files):" + str(totData))

def printHelp():
    print("Questo e' il menu di help")

main()