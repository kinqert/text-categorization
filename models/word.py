

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
        for groupedWord in self.groupVector:
            if groupedWord.group == word.group.name:
                groupedWord += word
                return
        
        self.groupVector.append(word)

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
            self.__insertWord__(0, newWord)
            return

        l = 0
        r = len(self.words)
        i = int((r - l) / 2)
        while True:
            if self.words[i].text == newWord.text:
                self.words[i] = self.__addWord__(self.words[i], newWord)
                break
            elif self.words[i].text > newWord.text:
                if (i - l) / 2 < 1:
                    self.__insertWord__(i, newWord)
                    break
                else:    
                    r = i 
                    i = int(l + ((i - l) / 2))
            elif self.words[i].text < newWord.text:
                if (r - i) / 2 < 1:
                    self.__insertWord__(i + 1, newWord)
                    break
                else:
                    l = i
                    i = int(i + ((r - i) / 2))
    
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
    def __init__(self):
        super().__init__()
    
    def __addWord__(self, w1, w2):
        w1.addWeight(w2)
        return w1
    
    def __insertWord__(self, index, newWord):
        self.words.insert(index, WeightedWordVector(newWord))

    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.getSumOfCounted()
        
        return ris