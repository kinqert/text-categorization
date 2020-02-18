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
            if groupedWord["group"] == word.group.name:
                groupedWord["word"] += word
                return
        
        self.groupVector.append(
            {
                "word" : word,
                "group" : word.group.name
            })


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
    
class WeightedDictionary(Dictionary):
    def __init__(self):
        super().__init__()
        self.weightedWords = []
    
    def searchWord(self, text):
        for word in self.words:
            if word.text == text:
                return word
        
        return None

    def searchAndAddWord(self, newWord: GroupedWord):
        existedWord = self.searchWord(newWord.text)

        if existedWord is not None:
                existedWord.addWeight(newWord)
        else:
            self.words.append(WeightedWordVector(newWord))