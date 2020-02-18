from models.word import Word, Dictionary

class Document:
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.dictionary = Dictionary()
    
    def readWords(self):
        file = open(self.path, 'r', encoding="ISO-8859-1")

        readedWords = []

        for line in file.readline():
            readedWords.append(line)
        
        splitters = [" ", ",", "."]

        for splitter in splitters:
            splittedWords = []
            for word in readedWords:
                splittedWords += word.split(splitter)
            
            readedWords = splittedWords
        
        for word in readedWords:
            if word is not "":
                self.dictionary.searchAndAddWord(Word(word))