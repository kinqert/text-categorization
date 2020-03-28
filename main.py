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

def loadOrCreateDataset(args):
    dataset = loadDataset(args.name)
    if dataset is None:
        dataset = createDataset(args.name)
        dataset.readDataset()
        dataset.createDictionary()
        analyzeLostWords(dataset)
        saveDataset(dataset)
    
    return dataset

def printDatasets(args):
    if os.path.isdir("data") is False:
        print('No datasets avaiable')
        return
    table = PrettyTable()
    table.field_names = ["Datasets"]
    for file in os.listdir("data"):
        table.add_row(file)
    print(table)

def importData(args):
    print(sys.path[0] + "/data")
    if os.path.isdir(sys.path[0] + "/data") is False:
        os.mkdir("data")

    x = PrettyTable()
    x.field_names = ["Category", "#dirs"]

    totData = 0

    for dir in os.listdir(args.path):
        if os.path.isdir(args.path + dir):
            nData= len(os.listdir(args.path + dir))
            totData += nData
            x.add_row([dir, str(nData)])
    
    print(x)
    print("Dimension of dataset(in files):" + str(totData))
    startImport(args.path)
    print("Data imported!")


def loadData(datasetPath):
    copytree(datasetPath, sys.path[0] + "/data-000001")

commands = {
    'import-data': importData,
    'start-training' : loadOrCreateDataset,
    'show-datasets' : printDatasets
    }

def main():
    print('Welcome to Naive text classifier main program!')
    print('developed by Lorenzo Adreani')
    parser = argparse.ArgumentParser(prog='text-categorization',description="Text-categorization")

    parser.add_argument('command', choices=commands.keys(), metavar='command', help=f'Commands avaiable: {str(commands.keys())}')
    parser.add_argument('-s', '--split', default=False, const=True, action='store_const')
    parser.add_argument('-p', '--path', nargs=1, metavar='dataset-path', help='Path to the folder of the dataset destination')
    parser.add_argument('-n', '--name', nargs=1, type=str, metavar='dataset-name')

    args = parser.parse_args()

    print(args)
    print(sys.argv)
    print(os.path.curdir)

    command = commands.get(args.command)
    command(args) 

main()