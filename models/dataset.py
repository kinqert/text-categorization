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
        self.wordWeight = []
    
    def readDataset(self):
        for group in self.trainGroups:
            group.readDocuments()
        
        self.datasetReaded = True
    
    

    def createDictionary(self):
        if self.datasetReaded is False:
            return

        for group in self.trainGroups:
            for word in group.groupedWords:





    def toString(self):
        string = f"Dataset: {self.name}\n"

        string += "Train Groups:\n"
        for trainGroup in self.trainGroups:
            string += trainGroup.toString()

        string += "Test Groups:\n"
        for testGroup in self.testGroups:
            string += testGroup.toString()
        
        return string

