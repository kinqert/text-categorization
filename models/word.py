class Word:

    def __init__(self, text, counted = 1):
        super().__init__()
        self.text = text
        self.counted = counted
    
    def __add__(self, newWord):
        if self.text == newWord.text:
            self.counted += newWord.counted

class GroupedWord(Word):

    def __init__(self, text, group, counted=1, documents=1):
        super().__init__(text, counted=counted)
        self.documents = documents
        self.group = group
    
    def __add__(self, newWord):
        if self.text == newWord.text:
            self.counted += newWord.counted
            self.documents += newWord.documents
    
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
    
    def searchWord(self, text):
        for word in self.words:
            if word.text == text:
                return word
        
        return None

    def searchAndAddWord(self, newWord: Word):
        existedWord = self.searchWord(newWord.text)

        if existedWord is not None:
                existedWord += newWord
        else:
            self.words.append(newWord)
        
    def getSumOfCounted(self):
        ris = 0

        for word in self.words:
            ris += word.counted
        
        return ris
    
class WeightedDictionary(Dictionary):
    def __init__(self):
        super().__init__()
        self.weightedWords = []
    
    def searchWord(self, text):
        for word in self.weightedWords:
            if word.text == text:
                return word
        
        return None

    def searchAndAddWord(self, newWord: GroupedWord):
        existedWord = self.searchWord(newWord.text)

        if existedWord is not None:
                existedWord.addWeight(newWord)
        else:
            self.weightedWords.append(WeightedWordVector(newWord))
    
    def getSumOfCounted(self):
        ris = 0

        for word in self.weightedWords:
            ris += word.getSumOfCounted()
        
        return ris