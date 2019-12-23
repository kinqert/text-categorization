class Table:
    groups = []
    totalWords = []
    type = ""

    def __init__(self, type, groups = [], totalWords = []):
        super().__init__()
        self.type = type
        self.groups = groups
        self.totalWords = totalWords
    
