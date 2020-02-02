from models.word import Word

class Document:
    def __init__(self, documentName, documentPath):
        super().__init__()
        self.documentName = documentName
        self.documentPath = documentPath
        self.words = []
    
    def readWords(self):
        file = open(self.documentPath)

    def searchAndAddWord(self, word: Word):
        for w in self.words:
            if word.word == w.word:
                w.counted += word.counted 
                return
        
        self.words.append(word)