from models.word import CountedWord, Dictionary

class Document:
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.dictionary = Dictionary()
        self.readedWords = []
        self.totalWords = 0
    
    def readWords(self):
        self.dictionary.clean()

        file = open(self.path, 'r', encoding="ISO-8859-1")

        lines = file.readlines()
        
        for line in lines:
            self.readedWords += line.split()
            
        self.totalWords = len(self.readedWords)
        
        for word in self.readedWords:
            self.dictionary.searchAndAddWord(CountedWord(word))
        
    
    def clearReadedWords(self):
        self.readedWords = []
