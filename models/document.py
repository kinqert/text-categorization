from models.word import Word

class Document:
    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.words = []
    
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
                self.searchAndAddWord(Word(word))

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