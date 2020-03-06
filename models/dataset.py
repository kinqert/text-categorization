from models.word import WeightedWordVector, WeightedDictionary
from models.group import Group

from log import printAndLog, appendLog

class Dataset:

    def __init__(self, datasetName):
        super().__init__()
        self.name = datasetName
        self.testPath = f"data/{datasetName}/test"
        self.trainPath = f"data/{datasetName}/train"

        self.trainGroups = []
        self.testGroups = []
        self.dictionaryWords = []
        self.datasetReaded = False
        self.weightedDictionary = WeightedDictionary()

    
    def readDataset(self):
        for group in self.trainGroups:
            group.readDocuments()
        
        self.datasetReaded = True
    
    def createDictionary(self):
        if self.datasetReaded is False:
            return

        print("Creating weight")
        for group in self.trainGroups:
            for word in group.dictionary.words:
                self.weightedDictionary.searchAndAddWord(word)
        
        print(f"Dizionario creato con {len(self.weightedDictionary.weightedWords)}")
        self.printWeightDictionaryDebugInfo()

    def printWeightDictionaryDebugInfo(self):
        for wordWeight in self.weightedDictionary.weightedWords:
            appendLog(wordWeight, "dataset-weight-vector")
                
    def toString(self):
        string = f"Dataset: {self.name}\n"

        string += "Train Groups:\n"
        for trainGroup in self.trainGroups:
            string += trainGroup.toString()

        string += "Test Groups:\n"
        for testGroup in self.testGroups:
            string += testGroup.toString()
        
        return string

