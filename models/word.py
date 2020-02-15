class Word:

    def __init__(self, text, counted = 1):
        super().__init__()
        self.text = text
        self.counted = counted
    
    def __add__(self, newWord):
        if self.text == newWord.text:
            self.counted += newWord.counted

class GroupedWord(Word):

    def __init__(self, text, counted=1, documents=1):
        super().__init__(text, counted=counted)
        self.documents = documents
    
    def __add__(self, newWord):
        if self.text == newWord.text:
            self.counted += newWord.counted
            self.documents += newWord.documents

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