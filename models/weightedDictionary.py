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
        self.featureSelectionAvg = True

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

    def featureSelection(self, maxLength):
        mutualInformation = self.__getMutualInformationArray__()
        mutualInformation.sort(reverse=True, key=lambda tup:tup[0])
        remainingWords = []

        print(f"Selecting feature for {self.__strTypeDictionary__()}")
        bar = ProgressBar(maxLength, [Percentage(), Bar()]).start()
        for i in range(0, maxLength):
            remainingWords.append(mutualInformation[i][1])
            bar.update(i)
        bar.finish()
        print("Done selecting feature")
        self.__setNewWordsVectors__(remainingWords)

    def __getMutualInformationArray__(self):
        return []

    def __selectInformation__(self, mi, totalDocuments):
        if self.featureSelectionAvg:
            avg = 0
            for i in range(0, len(mi)):
                totalGroupDocuments = len(self.groups[i].documents)
                avg -= (totalGroupDocuments / totalDocuments) * mi[i]
            return avg
        
        else:
            return max(mi)


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
    
    def __setNewWordsVectors__(self, words):
        self.words = []
        for word in words:
            exist, index = self.searchWord(word.text)
            self.words.insert(index, word)


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

    def __getMutualInformationArray__(self):
        totalDocuments = 0
        for group in self.groups:
            totalDocuments += len(group.documents)
        mutualInformation = []

        print(f"Calculating mutual information for {self.__strTypeDictionary__()}")
        bar = ProgressBar(len(self.words), [Percentage(), Bar()]).start()
        j = 0
        for wordVector in self.words:
            mi = 0
            B = wordVector.getSumOfDocuments()

            for i in range(0, len(wordVector.groupVector)):
                groupedWord = wordVector.groupVector[i]
                A = 0
                if groupedWord is not None:
                    A = groupedWord.documents

                C = len(self.groups[i].documents)
    
                n1 = A * totalDocuments
                n0 = (C - A) * totalDocuments
                d1 = B * C
                d0 = (totalDocuments - B) * C
                if A != 0:
                    mi += (A/totalDocuments) * math.log(n1/d1) 
                if C - A != 0:
                    mi += ((C-A) / totalDocuments) * math.log(n0/d0)

            mutualInformation.append([mi, wordVector])
            j += 1
            bar.update(j)
        bar.finish()
        
        return mutualInformation

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

    def __getMutualInformationArray__(self):
        totalWords = 0
        totalClassWords = [0] * len(self.groups)

        for wordVector in self.words:
            for i in range(0, len(wordVector.groupVector)):
                groupedWord = wordVector.groupVector[i]
                if groupedWord != None:
                    totalWords += groupedWord.counted
                    totalClassWords[i] += groupedWord.counted

        mutualInformation = []

        print(f"Calculating mutual information for {self.__strTypeDictionary__()}")
        bar = ProgressBar(len(self.words), [Percentage(), Bar()]).start()
        j = 0
        for wordVector in self.words:
            mi = 0
            B = wordVector.getSumOfCounted()

            for i in range(0, len(wordVector.groupVector)):
                groupedWord = wordVector.groupVector[i]
                A = 0
                if groupedWord is not None:
                    A = groupedWord.counted

                C = totalClassWords[i]
    
                n1 = A * totalWords
                n0 = (C - A) * totalWords
                d1 = B * C
                d0 = (totalWords - B) * C
                if A != 0:
                    mi += (A/totalWords) * math.log(n1/d1) 
                if C - A != 0:
                    mi += ((C-A) / totalWords) * math.log(n0/d0)

            mutualInformation.append([mi, wordVector])
            j += 1
            bar.update(j)
        bar.finish()
        
        return mutualInformation

    def __strTypeDictionary__(self):
        return "MM dictonary"

    def __cleanValueWord__(self, groupedWord):
        return groupedWord.counted

    def __createNewInstance__(self):
        return MMWeightedDictionary(self.groups)