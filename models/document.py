from models.word import Word, Dictionary

class Document:
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.dictionary = Dictionary()
        self.readedWords = []
    
    def readWords(self):
        file = open(self.path, 'r', encoding="ISO-8859-1")

        self.readedWords = file.readlines()
        
        for word in self.readedWords:
            self.readedWords += word.split()
            
        
        for word in self.readedWords:
            self.dictionary.searchAndAddWord(Word(word))