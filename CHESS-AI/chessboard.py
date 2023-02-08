

class Board:

    # Board initializes with instance variables fen, board and bitboard. There is also a fileRank
    # which is used to help get the file rank mapping of a piece square given index of board.
    # Each board is represented in three ways: board, fen, and bitboards.
    # (Board) A list of length 64 which contains information for the pieces on each
    # square of the board. Uppercase letters denote WHITE, lowercase denotes BLACK and "." denotes nothing.
    # (FEN) A fen string.
    # (Bitboards) Bitboards are used to represent sets of pieces. These sets can represents a number of different
    # types of squares (pieces, attacked squares, possible moves, pieces blocking sliding pieces, etc) and can be
    # manipulated efficientyly using set operations such as AND/OR. Piece bitboards are represented in a dictionary
    # called bitboards that takes characters from the board representation as keys. Bitboards are 64 bit integers
    # where the least significant position (first bit) corresponds with a1 and the most significant position (64th bit)
    # corresponds with h8.

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
            "R", "N", "B", "Q", "K", "B", "N", "R",
            "P", "P", "P", "P", "P", "P", "P", "P", 
            ".", ".", ".", ".", ".", ".", ".", ".", 
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", "P", ".", ".", ".", ".", ".", ".", 
            "p", "P", ".", ".", "P", ".", "P", ".",
            "p", "p", "p", "p", "p", "p", "p", "p",
            "r", "n", "b", "q", "k", "b", "n", "r"
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
            "K": 0b0
        }


    # function that takes the current board of the Board object and generates piece bitboards in the bitboards dictionary
    def board2Bitboard(self):
        # iterates over board
        for pieceIndex in range(63, -1, -1):
            # iterates of the keys of bitboards dictionary, if the piece == key, then a 1 bit is appended to the piece bitboard
            # otherwise the piece bitboard is shifted 1 to the left (append a 0 bit)
            for key in self.bitboards.keys():
                if self.board[pieceIndex] == key:
                    self.bitboards[key] = self.bitboards[key] << 1 | 0b1
                else:
                    self.bitboards[key] = self.bitboards[key] << 1


    def pawnMoveGen(self, index):
        # given index of a pawn check in front to see if it is blocked by a piece
        #   - do this using a mask for all pieces on the board and the bitboard representing the square in front of current pawn
        # then check to the left and right in front of the pawn to see if it can capture a piece
        #   - use mask of squares attacked by current pawn and mask of enemy pieces
        # if pawn is in the a or h file, then it cannot attack diagonally outside the board
        # does not have code from stopping a white pawn from going from 8th rank to 9th and similarly for black
        # FIXME: pawns that move 2 moves on the first move are able to hop over pieces in front of them
        pawnBb = self.index2Bitboard(index)
        pieceMask = self.pieceMask()
        if self.board[index] == "P":
            pawnForwardMask = pawnBb << 8 if self.fileRank[index][1] != 2 else pawnBb << 8 | pawnBb << 16
            enemyMask = self.enemyMask(True)
            if self.fileRank[index][0] == "a":
                return pawnForwardMask & pieceMask ^ pawnForwardMask | pawnBb << 9 & enemyMask
            elif self.fileRank[index][0] == "h":
                return pawnForwardMask & pieceMask ^ pawnForwardMask | pawnBb << 7 & enemyMask
            return pawnForwardMask & pieceMask ^ pawnForwardMask | pawnBb << 7 & enemyMask | pawnBb << 9 & enemyMask
        elif self.board[index] == 'p':
            pawnForwardMask = pawnBb >> 8 if self.fileRank[index][1] != 7 else pawnBb >> 8 | pawnBb >> 16
            enemyMask = self.enemyMask(False)
            if self.fileRank[index][0] == "a":
                return pawnForwardMask & pieceMask ^ pawnForwardMask | pawnBb >> 7 & enemyMask
            elif self.fileRank[index][0] == "h":
                return pawnForwardMask & pieceMask ^ pawnForwardMask | pawnBb >> 9 & enemyMask
            return pawnForwardMask & pieceMask ^ pawnForwardMask | pawnBb >> 7 & enemyMask | pawnBb >> 9 & enemyMask           
        print("Not a Pawn")
        return 0
    
    # returns bitboard that has a 1 on each square that has a piece on it
    def pieceMask(self):
        pieceMask = 0b0
        for bitboard in self.bitboards.values():
            pieceMask |= bitboard
        return pieceMask
    
    # given a boolean blackIsEnemy, if true, then generates bitboard mask of all black pieces
    # otherwise generates bitboard mask for white pieces
    def enemyMask(self, blackIsEnemy):
        enemyMask = 0b0
        if blackIsEnemy:
            for key in self.bitboards.keys():
                if key.islower():
                    enemyMask |= self.bitboards[key]
        else:
            for key in self.bitboards.keys():
                if key.isupper():
                    enemyMask |= self.bitboards[key]
        return enemyMask
    
    # function that returns the bitboard of the singular piece when given a board index
    # for instance index2Bitboard(6) returns 64 (0b1000000)
    def index2Bitboard(self, index):
        return 0b1 << index

    # returns the board index given a bitboard containing a single 1 bit
    # for instance index2Bitboard(0b1000000) returns 6
    def bitboard2Index(self, bitboard):
        return (bitboard & -bitboard).bit_length()-1
    
    # takes a FEN string and assigns it to the fen of the Board
    # also populates the board variable of Board according to the given FEN string
    def fen2Board(self, fen):
        self.fen = fen

        # splits given FEN string by whitespaces into a list
        fenList = self.fen.split()
        
        # fills board with "."
        self.board = ["." for i in range(64)]

        boardIndex = 0
        fenIndex = 0
        while fenIndex < len(fenList[0]):
            # fenList[0] contains only the board representation portion of the FEN string
            fenCurr = fenList[0][fenIndex]
            if fenCurr.isalpha():                   # checks to see if fenCurr is a letter
                self.board[boardIndex] = fenCurr
                fenIndex += 1
                boardIndex += 1
            elif fenCurr == '/':                    # increments fenIndex if fenCurr is "/"
                fenIndex += 1
            else:                                   # fenCurr is a number so fenCurr amount of squares are skipped
                fenIndex += 1
                boardIndex += int(fenCurr)

    def printBoard(self):
        count = 0
        i = 56
        while i > -1:
            while count < 8:
                print(self.board[i], end=" ")
                i += 1
                count += 1
            i -= 16
            count = 0
            print()

    def printBitboard(self, bitboard):
        bitboard = format(bitboard, "064b")
        count = 0
        i = 7
        while i < 64:
            while count < 8:
                print(bitboard[i], end=" ")
                i -= 1
                count += 1
            i += 16
            count = 0
            print()      

########################################
brd = Board()
brd2 = Board()
brd.board2Bitboard()
#brd.fen2Board("bbrknqnr/pppppppp/8/8/8/8/PPPPPPPP/BBRKNQNR w KQkq - 0 1")
brd.printBoard()
print("---------------")
brd.printBitboard(brd.pawnMoveGen(40))

