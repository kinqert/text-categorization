import sys
import os

from progressbar import ProgressBar, Percentage, Bar

from models.word import WeightedWordVector, WeightedDictionary
from models.group import Group

from log import printAndLog, appendLog

class Dataset:

    def __init__(self, datasetName):
        super().__init__()
        self.name = datasetName
        self.testPath = f"{sys.path[0]}/data/{datasetName}/test"
        self.trainPath = f"{sys.path[0]}/data/{datasetName}/train"

        self.trainGroups = []
        self.testGroups = []
        self.dictionaryWords = []
        self.datasetReaded = False
        self.weightedDictionary: WeightedDictionary

    
    def readDataset(self):
        for group in self.trainGroups:
            group.readDocuments()
        
        self.datasetReaded = True
    
    def createDictionary(self):
        if self.datasetReaded is False:
            self.readDataset()

        self.weightedDictionary = WeightedDictionary(self.trainGroups)

        print("Creating weight")
        for group in self.trainGroups:
            print(f"Adding weight from group {group.name}")
            bar = ProgressBar(len(group.dictionary.words), [Percentage(), Bar()]).start()
            i = 0
            for word in group.dictionary.words:
                self.weightedDictionary.searchAndAddWord(word)
                i += 1
                bar.update(i)
            bar.finish()
            print(f"Done adding weight from group {group.name}")

        print(f"Dizionario creato con {len(self.weightedDictionary.words)}")
        self.printWeightDictionaryDebugInfo()

    def printWeightDictionaryDebugInfo(self):
        for wordWeight in self.weightedDictionary.words:
            appendLog(f"{wordWeight}\n", "dataset-weight-vector")
                
    def toString(self):
        string = f"Dataset: {self.name}\n"

        string += "Train Groups:\n"
        for trainGroup in self.trainGroups:
            string += trainGroup.toString()

        string += "Test Groups:\n"
        for testGroup in self.testGroups:
            string += testGroup.toString()
        
        return string

