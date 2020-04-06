import sys
import os
import argparse

from prettytable import PrettyTable
from shutil import copyfile, copytree

from importing import startImport
from factory.datasetFactory import createDataset
from log import printAndLog
from result import plotWordsCountForAllDocuments
from saving import saveDataset, loadDataset
from dataloss import analyzeLostWords
from util.colors import bcolors

def loadOrCreateDataset(args):
    dataset = loadDataset(args.name[0])
    if dataset is None:
        dataset = createDataset(args.name[0])

    return dataset

def startTraining(args):
    if args.name is None:
        print(bcolors.FAIL + "Name must be provided!" + bcolors.ENDC)
        return
    dataset = loadOrCreateDataset(args)

    dataset.readDataset()
    dataset.createDictionary()
    #analyzeLostWords(dataset)
    saveDataset(dataset)
    print(bcolors.OKGREEN + "Done learning!" + bcolors.ENDC)

def printDatasets(args):
    dataDir = f"{sys.path[0]}/data"
    if os.path.isdir(dataDir) is False:
        print(bcolors.WARNING + "No datasets avaiable" + bcolors.ENDC)
        return
    table = PrettyTable()
    table.field_names = ["Datasets"]
    for file in os.listdir(dataDir):
        table.add_row([file])
    print(table)


def importData(args):
    if args.path is None:
        print(bcolors.FAIL + "Import path must be provided!" + bcolors.ENDC)
    dataPath = sys.path[0] + "/data"
    if os.path.isdir(dataPath) is False:
        os.mkdir(dataPath)

    x = PrettyTable()
    x.field_names = ["Category", "#dirs"]

    totData = 0
    print(args.path[0])
    for dir in os.listdir(args.path[0]):
        if os.path.isdir(f"{args.path[0]}/{dir}"):
            nData = len(os.listdir(f"{args.path[0]}/{dir}"))
            totData += nData
            x.add_row([dir, str(nData)])

    print(x)
    print("Dimension of dataset(in files):" + str(totData))
    startImport(args)
    print(bcolors.OKGREEN + "Data imported!" + bcolors.ENDC)


def loadData(datasetPath):
    copytree(datasetPath, sys.path[0] + "/data-000001")

def startTesting(args):
    if args.name is None:
        print(bcolors.FAIL + "Name must be provided!" + bcolors.ENDC)
        return

    dataset = loadOrCreateDataset(args)

    if dataset.datasetReaded is False:
        print(bcolors.FAIL + f"Dataset must learned first!" + bcolors.ENDC)
        return

    accuracyMBM, accuracyMM = dataset.startTest()

   
commands = {
    'import-data': importData,
    'start-training': startTraining,
    'show-datasets': printDatasets,
    'start-testing': startTesting
}


def main():
    print('Welcome to Naive text classifier main program!')
    print('developed by Lorenzo Adreani')
    parser = argparse.ArgumentParser(prog='text-categorization', description="Text-categorization")

    parser.add_argument('command', choices=commands.keys(), metavar='command',
                        help=f'Commands avaiable: {str(commands.keys())}')
    parser.add_argument('-s', '--split', default=False, const=True, action='store_const', help='Split the dataset path into train and test with 80:20 ratio')
    parser.add_argument('-p', '--path', nargs=1, type=str, metavar='dataset-path',
                        help='Path to the folder of the dataset destination; Needed for import-dataset')
    parser.add_argument('-n', '--name', nargs=1, type=str, metavar='dataset-name', help='Name of the dataset selected; Needed for start-training')

    args = parser.parse_args()

    command = commands.get(args.command)
    command(args)


main()
