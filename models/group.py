from models.word import Word, GroupedWord

class Group:

    def __init__(self, name, path, type):
        super().__init__()
        self.name = name
        self.path = path
        self.type = type

        self.documents = []
        self.groupedWords = []
    
    def readDocuments(self):
        for document in self.documents:
            document.readWords()

            for word in document.words:
                self.searchAndAddGroupedWord(GroupedWord(word.text, word.counted))
        
    def searchWord(self, text):
        for word in self.groupedWords:
            if word.text == text:
                return word
        
        return None

    def searchAndAddGroupedWord(self, word: GroupedWord):
        existedWord = self.searchWord(word.text)

        if existedWord is not None:
            existedWord += word
        else:
            self.groupedWords.append(word)

    def toString(self):
        return f"Group: {self.name}, Type: {self.groupType},\nPath: {self.groupPath}, Documents: {len(self.documents)}\n"
