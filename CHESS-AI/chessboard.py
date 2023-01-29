

class Board:

    # Board initializes with a variable, fen, which holds the fen string of the current board
    # and a variable, board, which is a tuple with numbers 1-64
    # used to calculate possible piece moves
    def __init__(self, fen):
        
        self.fen = fen
        self.board = (i for i in range(1, 65))



