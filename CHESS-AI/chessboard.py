

class Board:

    # Board initializes with a variable, fen, which holds the fen string of the current board
    # and a variable, board, which is a tuple with numbers 1-64
    # used to calculate possible piece moves
    def __init__(self):
        
        self.fileRank = (
            ("a", 1), ("b", 1),("c", 1), ("d", 1),("e", 1), ("f", 1),("g", 1), ("h", 1),
            ("a", 2), ("b", 2),("c", 2), ("d", 2),("e", 2), ("f", 2),("g", 2), ("h", 2),
            ("a", 3), ("b", 3),("c", 3), ("d", 3),("e", 3), ("f", 3),("g", 3), ("h", 3),
            ("a", 4), ("b", 4),("c", 4), ("d", 4),("e", 4), ("f", 4),("g", 4), ("h", 4),
            ("a", 5), ("b", 5),("c", 5), ("d", 5),("e", 5), ("f", 5),("g", 5), ("h", 5),
            ("a", 6), ("b", 6),("c", 6), ("d", 6),("e", 6), ("f", 6),("g", 6), ("h", 6),
            ("a", 7), ("b", 7),("c", 7), ("d", 7),("e", 7), ("f", 7),("g", 7), ("h", 7),
            ("a", 8), ("b", 8),("c", 8), ("d", 8),("e", 8), ("f", 8),("g", 8), ("h", 8)
        )

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

    def index2Bitboard(self, index):
        return 0b1 << index

    def bitboard2Index(self, bitboard):
        return (bitboard & -bitboard).bit_length()-1

brd = Board()
brd.board2Bitboard()
