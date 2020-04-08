from sklearn.feature_extraction.text import CountVectorizer

from models.word import CountedWord
from models.dictionary import Dictionary

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
            if line.startswith("Newsgroups:"):
                lines.remove(line)
        vectorizer = CountVectorizer()
        x = vectorizer.fit_transform(lines)
        self.readedWords = vectorizer.get_feature_names()    
        self.totalWords = len(self.readedWords)
        
        for arrayLine in x.toarray():
            for i in range(0, len(arrayLine)):
                if arrayLine[i] != 0:
                    self.dictionary.searchAndAddWord(CountedWord(self.readedWords[i], arrayLine[i]))
        
    
    def clearReadedWords(self):
        self.readedWords = []
