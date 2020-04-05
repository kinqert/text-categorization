import sys
import os

from progressbar import ProgressBar, Percentage, Bar

from models.word import WeightedWordVector, WeightedDictionary
from models.group import Group
from util.colors import bcolors
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
        for group in self.testGroups:
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

        for group in self.trainGroups:
            group.setDenominator(len(self.weightedDictionary.words))
        self.weightedDictionary.createParameters()

        print(bcolors.OKGREEN + f"Dictionary created with {len(self.weightedDictionary.words)} words" + bcolors.ENDC)

    def printWeightDictionaryDebugInfo(self):
        for wordWeight in self.weightedDictionary.words:
            appendLog(f"{wordWeight}\n", "dataset-weight-vector")
                
    
    # Probably need multi-thread
    def startTest(self):
        currentTestedFiles = 0
        correctMBMPrediction = 0
        correctMMPrediction = 0

        for testGroup in self.testGroups:
            print(f"Testing file in group {testGroup.name}")
            totalTestFiles = len(testGroup.documents)
            bar = ProgressBar(totalTestFiles, [Percentage(), Bar()]).start()
            documentTested = 0
            for document in testGroup.documents:
                mbmWeights, mmWeights = self.weightedDictionary.getWeights(document.dictionary)

                groupMBMPosition = 0
                groupMMPosition = 0
                minMBMWeight = mbmWeights[0]
                minMMWeight = mmWeights[0]

                for i in range(0, len(mbmWeights)):
                    if minMBMWeight > mbmWeights[i]:
                        minMBMWeight = mbmWeights[i]
                        groupMBMPosition = i
                    if minMMWeight > mmWeights[i]:
                        minMMWeight = mmWeights[i]
                        groupMMPosition = i
                    
                if self.trainGroups[groupMBMPosition].name == testGroup.name:
                    correctMBMPrediction += 1
                if self.trainGroups[groupMMPosition].name == testGroup.name:
                    correctMMPrediction += 1

                currentTestedFiles += 1
                documentTested += 1
                bar.update(documentTested)
            bar.finish()
            print(f"Done testing group {testGroup.name}")
        
        return correctMBMPrediction / currentTestedFiles, correctMMPrediction / currentTestedFiles
    
    def toString(self):
        string = f"Dataset: {self.name}\n"

        string += "Train Groups:\n"
        for trainGroup in self.trainGroups:
            string += trainGroup.toString()

        string += "Test Groups:\n"
        for testGroup in self.testGroups:
            string += testGroup.toString()
        
        return string

