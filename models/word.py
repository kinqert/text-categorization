

class CountedWord:

    def __init__(self, text, counted = 1):
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

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.groupVector = []
    
    def __init__(self, word: GroupedWord):
        super().__init__()
        self.text = word.text 
        self.groupVector = []

        self.addWeight(word)

    def addWeight(self, word: GroupedWord):
        #Add a better way
        for groupedWord in self.groupVector:
            if groupedWord.group == word.group.name:
                groupedWord += word
                return
        
        self.groupVector.append(word)

    def __add__(self, newWord):
        if self.text != newWord.text:
            return
        
        for newGroupedWord in newWord.groupVector:
            groupMatch = False
            for existedGroupWord in self.groupVector:
                if newGroupedWord.group == existedGroupWord.group:
                    existedGroupWord += newGroupedWord
                    groupMatch = True
            
            if groupMatch is False:
                self.groupVector.append(newGroupedWord)


    def __str__(self):
        
        ris = f"word: {self.text}, weights: ["
        for group in self.groupVector:
            ris += f"{str(group)},"
        ris += "]"

        return ris;

    def getSumOfCounted(self):
        ris = 0

        for word in self.groupVector:
            ris += word.counted

        return ris


class Dictionary:
    def __init__(self):
        super().__init__()
        self.words = []

    def searchAndAddWord(self, newWord: CountedWord):
        if len(self.words) == 0:
            self.words.insert(0, newWord)
            return

        l = 0
        r = len(self.words)
        i = int((r - l) / 2)
        while True:
            if self.words[i].text == newWord.text:
                self.words[i] = __addWords__(self.words[i], newWord)
                break
            elif self.words[i].text > newWord.text:
                if (i - l) / 2 < 1:
                    self.__insertWords__(i, newWord)
                    break
                else:    
                    r = i 
                    i = int(l + ((i - l) / 2))
            elif self.words[i].text < newWord.text:
                if (r - i) / 2 < 1:
                    self.__insertWords__(i + 1, newWord)
                    break
                else:
                    l = i
                    i = int(i + ((r - i) / 2))
    
    def __addWords__(self, w1, w2):
        return w1 + w2

    def __insertWords__(self, index, newWord):
        self.words.insert(index, newWord)

        
    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.counted
        
        return ris
    
class WeightedDictionary(Dictionary):
    def __init__(self):
        super().__init__()
    
    def __addWords__(self, w1, w2):
        return w1.addWeight(w2)
    
    def __insertWords__(self, index, newWord):
        #TODO: Complete here

    def getSumOfCounted(self):
        ris = 0

        for word in self.weightedWords:
            ris += word.getSumOfCounted()
        
        return ris