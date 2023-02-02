

class Board:

    # Board initializes with a variable, fen, which holds the fen string of the current board
    # and a variable, board, which is a tuple with numbers 1-64
    # used to calculate possible piece moves
    def __init__(self):
        
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = [
            "R", "N", "B", "K", "Q", "B", "N", "R",
            "P", "P", "P", "P", "P", "P", "P", "P", 
            ".", ".", ".", ".", ".", ".", ".", ".", 
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".", 
            ".", ".", ".", ".", ".", ".", ".", ".",
            "p", "p", "p", "p", "p", "p", "p", "p",
            "r", "n", "b", "k", "q", "b", "n", "r"
        ]

        self.bitboards = {
            "p": 0b0,
            "r": 0b0,
            "n": 0b0,
            "b": 0b0,
            "q": 0b0,
            "k": 0b0,
            "P": 0b0,
            "R": 0b0,
            "N": 0b0,
            "B": 0b0,
            "Q": 0b0,
            "K": 0b0,  
        }



    def appendBit2Bitboard(self, bitboard):
        return bitboard << 1 | 0b0
    
    def board2Bitboard(self):
        for piece in self.board:
            for key in self.bitboards.keys():
                if piece == key:
                    self.bitboards[key] = self.bitboards[key] << 1 | 0b1
                else:
                    self.bitboards[key] = self.bitboards[key] << 1
    def pawnMoveGen(self):
        pawnMoves = self.bitboards["p"] << 8 | self.bitboards["P"] >> 8
        print(format(pawnMoves, "064b"))

brd = Board()
brd.board2Bitboard()

for key in brd.bitboards.keys():
    print(key + ": " + format(brd.bitboards[key], "064b"))



brd.pawnMoveGen()