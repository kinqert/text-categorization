import math

from progressbar import ProgressBar, Percentage, Bar

from util.colors import bcolors

def isGTString(s1, s2):
    isGT = False
    ended = False
    for i in range(0, len(min(s1, s2)) - 1):
        if ord(s1[i]) < ord(s2[i]):
            ended = True
            break
        elif ord(s1[i]) > ord(s2[i]):
            ended = True
            isGT = True
            break
    
    if ended is False:
        isGT = s1 == min(s1,s2)
    
    return isGT

class CountedWord:

    def __init__(self, text, counted=1):
        super().__init__()
        self.text = text
        self.counted = counted
    
    def __add__(self, newWord):
        if self.text == newWord.text:
            self.counted += newWord.counted
            return self

class GroupedWord(CountedWord):

    def __init__(self, text, group, counted=1, documents=1):
        super().__init__(text, counted=counted)
        self.documents = documents
        self.group = group
    
    def __add__(self, newWord):
        if self.text == newWord.text:
            self.counted += newWord.counted
            self.documents += newWord.documents
            return self
    
    def __str__(self):
        return f"text: {self.text}, group: {self.group}, counted: {self.counted}, documents: {self.documents}"

class WeightedWordVector:

    def __init__(self, groups, word: GroupedWord):
        super().__init__()
        self.text = word.text 
        self.groupVector = []
        self.groups = groups

        self.addWeight(word)
        self.mbmWeights = []
        self.mmWeights = []

        for group in self.groups:
            self.mbmWeights.append(0)
            self.mmWeights.append(0)

    def addWeight(self, word: GroupedWord):
        for groupedWord in self.groupVector:
            if groupedWord.group == word.group.name:
                groupedWord += word
                return
        
        self.groupVector.append(word)

    def updateWeights(self):
        for groupedWord in self.groupVector:
            groupPosition = -1
            for i in range(0, len(self.groups)):
                if self.groups[i] == groupedWord.group:
                    groupPosition = i
                    break
           
            self.mbmWeights[groupPosition]  = (1 + groupedWord.documents)   / groupedWord.group.mbmDenominator
            self.mmWeights[groupPosition]   = (1 + groupedWord.counted)     / groupedWord.group.mmDenominator
        
        for i in range(0, len(self.groups)):
            if self.mbmWeights[i] == 0:
                self.mbmWeights[i]  = 1 / self.groups[i].mbmDenominator

            if self.mmWeights[i] == 0:
                self.mmWeights[i]   = 1 / self.groups[i].mmDenominator

    def __str__(self):
        
        ris = f"word: {self.text}, weights: ["
        for group in self.groupVector:
            ris += f"{str(group)},"
        ris += "]"

        return ris

    def getSumOfCounted(self):
        ris = 0

        for word in self.groupVector:
            ris += word.counted

        return ris


class Dictionary:
    def __init__(self):
        super().__init__()
        self.words = []

    def searchWord(self, text):
        if len(self.words) == 0:
            return False, 0

        l = 0
        r = len(self.words) - 1
        i = int((r + l) / 2)
        while l <= r:
            if self.words[i].text == text:
                return True, i
            elif self.words[i].text > text:
                r = i - 1
            else:
                l = i + 1
            i = int((r + l) / 2)

        if self.words[i].text < text:
            i += 1

        return False, i
    

    def searchAndAddWord(self, newWord: CountedWord):
        founded, index = self.searchWord(newWord.text)
        if founded:
            self.__addWord__(self.words[index], newWord)
        else:
            self.__insertWord__(index, newWord)

    def __addWord__(self, w1, w2):
        w1 = w1 + w2

    def __insertWord__(self, index, newWord):
        self.words.insert(index, newWord)

    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.counted
        
        return ris

    def clean(self):
        self.words = []
    
class WeightedDictionary(Dictionary):
    def __init__(self, groups):
        super().__init__()
        self.groups = groups
        self.mbmStartWeights = []
        
        for group in self.groups:
            self.mbmStartWeights.append(0)
    
    def __addWord__(self, w1, w2):
        w1.addWeight(w2)
        return w1
    
    def __insertWord__(self, index, newWord):
        self.words.insert(index, WeightedWordVector(self.groups, newWord))

    def getWeights(self, dictionary: Dictionary):
        resultMBMWeights = []
        resultMMWeights = []

        for i in range(0, len(self.groups)):
            resultMBMWeights.append(self.mbmStartWeights[i])
            resultMMWeights.append(0)

        for word in dictionary.words:
            wordExist, index = self.searchWord(word.text)

            #TODO: Add here speed improvement
            if wordExist:
                for i in range(0, len(resultMBMWeights)):
                    wordVector = self.words[index]
                    resultMBMWeights[i] -= math.log(wordVector.mbmWeights[i]) + math.log(1 - wordVector.mbmWeights[i])

                    wordCount = dictionary.words[i].counted
                    resultMMWeights[i] -= wordCount * math.log(wordVector.mmWeights[i]) - math.log(math.factorial(wordCount)) 

        return resultMBMWeights, resultMMWeights
    
    def createParameters(self):
        print("Starting calculating parameters from the dictionary")
        bar = ProgressBar(len(self.words), [Percentage(), Bar()]).start()
        i = 0
        for word in self.words:
            word.updateWeights()
            for j in range(0, len(self.mbmStartWeights)):
                self.mbmStartWeights[j] -= math.log(1 - word.mbmWeights[j])
            i += 1
            bar.update(i)
        bar.finish()
        print("Parameters created")

    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.getSumOfCounted()
        
        return ris

