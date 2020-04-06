import math

from progressbar import ProgressBar, Percentage, Bar

from models.dictionary import Dictionary
from models.word import GroupedWord
from models.wordVector import WeightedWordVector, MBMWeightedWordVector, MMWeightedWordVector

# Abstract class not intended for direct usage
class WeightedDictionary(Dictionary):
    def __init__(self, groups):
        super().__init__()
        self.groups = groups
        self.startWeights = []

        for group in self.groups:
            self.startWeights.append(0)

    def resetStartWeight(self):        
        for i in range(0, len(self.startWeights)):
            self.startWeights[i] = 0
    
    def __addWord__(self, w1, w2):
        w1.addWeight(w2)
        return w1
    
    def __insertWord__(self, index, newWord):
        self.words.insert(index, WeightedWordVector(self, newWord))

    def classifyDictionary(self, dictionary: Dictionary):
        resultWeights = []

        for i in range(0, len(self.groups)):
            resultWeights.append(self.startWeights[i])

        for word in dictionary.words:
            wordExist, index = self.searchWord(word.text)

            #TODO: Add here speed improvement
            if wordExist:
                for i in range(0, len(resultWeights)):
                    wordVector = self.words[index]
                    resultWeights[i] -= self.__getWeightOfClass__(wordVector, word, i)

        return resultWeights
    
    def __getWeightOfClass__(self, wordVector: WeightedWordVector, word:GroupedWord, classIndex):
        return 
    
    def createParameters(self):
        print(f"Starting calculating parameters for {self.__strTypeDictionary__()}")
        bar = ProgressBar(len(self.words), [Percentage(), Bar()]).start()
        i = 0
        self.resetStartWeight()
        for word in self.words:
            word.updateWeights()
            self.__updateStartWeights__(word)
            i += 1
            bar.update(i)
        bar.finish()
        print("Parameters created")
    
    def __strTypeDictionary__(self):
        return "dictonary"
    
    def __updateStartWeights__(self, wordVector: WeightedWordVector):
        return

    def getCopy(self):
        newDictionary = self.__createNewInstance__()
        newDictionary.words = self.words
        newDictionary.startWeights = self.startWeights
        return newDictionary
    
    def __createNewInstance__(self):
        return WeightedDictionary(self.groups)    

    def cleanDictionary(self):
        print(f"Cleaning {self.__strTypeDictionary__()}")
        bar = ProgressBar(len(self.words), [Percentage(), Bar()]).start()
        cleanedWords = []
        for i in range(0, len(self.words)):
            wordInDocuments = 0
            for groupedWord in self.words[i].groupVector:
                if groupedWord != None:
                    wordInDocuments += self.__cleanValueWord__(groupedWord)
            
            if wordInDocuments > 1:
                cleanedWords.append(self.words[i])
            bar.update(i)
        bar.finish()
        removedWords = len(self.words) - len(cleanedWords)
        self.words = cleanedWords

        print(f"Removed {removedWords} words")
    
    def __cleanValueWord__(self, groupedWord):
        return 0

    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.getSumOfCounted()
        
        return ris

class MBMWeightedDictionary(WeightedDictionary):
    def __init__(self, groups):
        super().__init__(groups)

    def __insertWord__(self, index, newWord):
        self.words.insert(index, MBMWeightedWordVector(self, newWord))

    def __getWeightOfClass__(self, wordVector: WeightedWordVector, word:GroupedWord, classIndex):
        return math.log(wordVector.weights[classIndex]) - math.log(1 - wordVector.weights[classIndex])

    def __updateStartWeights__(self, wordVector: WeightedWordVector):
        for j in range(0, len(self.startWeights)):
            self.startWeights[j] -= math.log(1 - wordVector.weights[j])

    def __strTypeDictionary__(self):
        return "MBM dictonary"

    def __cleanValueWord__(self, groupedWord):
        return groupedWord.documents
    
    def __createNewInstance__(self):
        return MBMWeightedDictionary(self.groups)

class MMWeightedDictionary(WeightedDictionary):
    def __init__(self, groups):
        super().__init__(groups)

    def __insertWord__(self, index, newWord):
        self.words.insert(index, MMWeightedWordVector(self, newWord))

    def __getWeightOfClass__(self, wordVector: WeightedWordVector, word:GroupedWord, classIndex):
        wordCount = word.counted
        return wordCount * math.log(wordVector.weights[classIndex]) - math.log(math.factorial(wordCount)) 

    def __strTypeDictionary__(self):
        return "MM dictonary"

    def __cleanValueWord__(self, groupedWord):
        return groupedWord.counted

    def __createNewInstance__(self):
        return MMWeightedDictionary(self.groups)