import sys
import os
import copy

from progressbar import ProgressBar, Percentage, Bar

from models.weightedDictionary import WeightedDictionary, MBMWeightedDictionary, MMWeightedDictionary
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
        self.mmWeightedDictionary: MMWeightedDictionary
        self.mbmWeightedDictionary: MBMWeightedDictionary

    
    def readDataset(self):
        if self.datasetReaded is False:
            for group in self.trainGroups:
                group.readDocuments()
            for group in self.testGroups:
                group.readDocuments()

            self.datasetReaded = True
    
    def createDictionary(self):
        if self.datasetReaded is False:
            self.readDataset()

        self.mbmWeightedDictionary = MBMWeightedDictionary(self.trainGroups)
        self.mmWeightedDictionary = MMWeightedDictionary(self.trainGroups)

        print("Creating weight")
        for group in self.trainGroups:
            print(f"Adding weight from group {group.name}")
            bar = ProgressBar(len(group.dictionary.words), [Percentage(), Bar()]).start()
            i = 0
            for word in group.dictionary.words:
                self.mbmWeightedDictionary.searchAndAddWord(word)
                self.mmWeightedDictionary.searchAndAddWord(word)
                i += 1
                bar.update(i)
            bar.finish()
            print(f"Done adding weight from group {group.name}")

        self.mmWeightedDictionary.createParameters()
        self.mbmWeightedDictionary.createParameters()

        print(bcolors.OKGREEN + f"Dictionary MBM created with {len(self.mbmWeightedDictionary.words)} words" + bcolors.ENDC)
        print(bcolors.OKGREEN + f"Dictionary MM created with {len(self.mmWeightedDictionary.words)} words" + bcolors.ENDC)

    # Probably need multi-thread
    def startTest(self):
        #TODO: Add clean here
        cleanMBMDictionary = self.mbmWeightedDictionary.getCopy()
        cleanMMDictionary = self.mmWeightedDictionary.getCopy()

        cleanMBMDictionary.cleanDictionary()
        cleanMMDictionary.cleanDictionary()

        cleanMBMDictionary.createParameters()
        cleanMBMDictionary.createParameters()

        currentTestedFiles = 0
        correctMBMPrediction = 0
        correctMMPrediction = 0

        for testGroup in self.testGroups:
            print(f"Testing file in group {testGroup.name}")
            totalTestFiles = len(testGroup.documents)
            bar = ProgressBar(totalTestFiles, [Percentage(), Bar()]).start()
            documentTested = 0
            for document in testGroup.documents:
                mbmWeights = cleanMBMDictionary.classifyDictionary(document.dictionary)
                mmWeights = cleanMMDictionary.classifyDictionary(document.dictionary)

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

        accuracyMBM = correctMBMPrediction / currentTestedFiles
        accuracyMM = correctMMPrediction / currentTestedFiles

        print(bcolors.OKGREEN + "Done testing" + bcolors.ENDC)
        print(f"Total word in MBM dictionary: {len(cleanMBMDictionary.words)}")
        print(f"Total word in MM dictionary: {len(cleanMMDictionary.words)}")
        print(f"MBM accuracy: {accuracyMBM * 100}%; MM accuracy: {accuracyMM * 100}%")
        
        return accuracyMBM, accuracyMM
    
    def toString(self):
        string = f"Dataset: {self.name}\n"

        string += "Train Groups:\n"
        for trainGroup in self.trainGroups:
            string += trainGroup.toString()

        string += "Test Groups:\n"
        for testGroup in self.testGroups:
            string += testGroup.toString()
        
        return string

