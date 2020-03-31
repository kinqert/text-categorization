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

    def addWeight(self, word: GroupedWord):
        for groupedWord in self.groupVector:
            if groupedWord.group == word.group.name:
                groupedWord += word
                return
        
        self.groupVector.append(word)

    def getMBM(self):
        weights = []
        for group in self.groups:
            weights.append(0)

        for groupedWord in self.groupVector:
            n = 1 + groupedWord.documents
            d = 2 + len(groupedWord.group.documents)

            groupPosition = -1
            for i in range(0, len(self.groups) - 1):
                if self.groups[i] == groupedWord.group:
                    groupPosition = i
                    break

            weights[groupPosition] = n/d
        return weights

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

    def searchWord(self, newWord: CountedWord):
        if len(self.words) == 0:
            return False, 0

        l = 0
        r = len(self.words)
        i = int((r - l) / 2)
        while True:
            if self.words[i].text == newWord.text:
                return True, i
            elif self.words[i].text > newWord.text:
                if (i - l) / 2 < 1:
                    return False, i
                else:
                    r = i 
                    i = int(l + ((i - l) / 2))
            elif self.words[i].text < newWord.text:
                if (r - i) / 2 < 1:
                    return False, i + 1
                else:
                    l = i
                    i = int(i + ((r - i) / 2))

    def searchAndAddWord(self, newWord: CountedWord):
        founded, index = self.searchWord(newWord)
        if founded:
            self.__addWord__(self.words[index], newWord)
        else:
            self.__insertWord__(index, newWord)

    def __addWord__(self, w1, w2):
        return w1 + w2

    def __insertWord__(self, index, newWord):
        self.words.insert(index, newWord)

    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.counted
        
        return ris
    
class WeightedDictionary(Dictionary):
    def __init__(self, groups):
        super().__init__()
        self.groups = groups
    
    def __addWord__(self, w1, w2):
        w1.addWeight(w2)
        return w1
    
    def __insertWord__(self, index, newWord):
        self.words.insert(index, WeightedWordVector(newWord))

    def getMBMWeight(self, dictionary: Dictionary):
        resultWeight = []
        for i in range(0, len(self.groups) - 1):
                resultWeight.append(1)

        for word in self.words:
            wordWeights = word.getMBM()
            wordExist, index = dictionary.searchWord(word)

            if wordExist:
                for i in range(0, len(resultWeight)):
                    resultWeight[i] *= wordWeights[i]
            else:
                for i in range(0, len(resultWeight)):
                    resultWeight[i] *= 1 - wordWeights[i]

        return resultWeight


    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.getSumOfCounted()
        
        return ris

