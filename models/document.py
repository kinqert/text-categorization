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

        lines = file.readlines()
        
        for line in lines:
            self.readedWords += line.split()
            
        
        for word in self.readedWords:
            self.dictionary.searchAndAddWord(Word(word))
        
    
    def clearReadedWords(self):
        self.readedWords = []
