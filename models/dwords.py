class Dwords:
    word = ""
    counted = 0

    def __init__(self, word, counted = 1):
        super().__init__()
        self.word = word
        self.counted = counted