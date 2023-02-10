

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
            ".", ".", ".", ".", ".", ".", ".", ".", 
            ".", ".", ".", ".", ".", ".", ".", ".",
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
    
        self.knightMoves = (
            132096, 329728, 659712, 1319424, 2638848, 5277696, 10489856, 4202496, 33816580, 84410376, 
            168886289, 337772578, 675545156, 1351090312, 2685403152, 1075839008, 8657044482, 21609056261, 
            43234889994, 86469779988, 172939559976, 345879119952, 687463207072, 275414786112, 2216203387392, 
            5531918402816, 11068131838464, 22136263676928, 44272527353856, 88545054707712, 175990581010432, 
            70506185244672, 567348067172352, 1416171111120896, 2833441750646784, 5666883501293568, 11333767002587136, 
            22667534005174272, 45053588738670592, 18049583422636032, 145241105196122112, 362539804446949376, 
            725361088165576704, 1450722176331153408, 2901444352662306816, 5802888705324613632, 11533718717099671552, 
            4620693356194824192, 288234782788157440, 576469569871282176, 1224997833292120064, 2449995666584240128, 
            4899991333168480256, 9799982666336960512, 1152939783987658752, 2305878468463689728, 1128098930098176, 
            2257297371824128, 4796069720358912, 9592139440717824, 19184278881435648, 38368557762871296, 4679521487814656, 
            9077567998918656
            )
        
        self.kingMoves = (
            770, 1797, 3594, 7188, 14376, 28752, 57504, 49216, 197123, 460039, 920078, 1840156, 3680312, 7360624, 14721248, 
            12599488, 50463488, 117769984, 235539968, 471079936, 942159872, 1884319744, 3768639488, 3225468928, 12918652928, 
            30149115904, 60298231808, 120596463616, 241192927232, 482385854464, 964771708928, 825720045568, 3307175149568, 
            7718173671424, 15436347342848, 30872694685696, 61745389371392, 123490778742784, 246981557485568, 211384331665408, 
            846636838289408, 1975852459884544, 3951704919769088, 7903409839538176, 15806819679076352, 31613639358152704, 
            63227278716305408, 54114388906344448, 216739030602088448, 505818229730443264, 1011636459460886528, 
            2023272918921773056, 4046545837843546112, 8093091675687092224, 16186183351374184448, 13853283560024178688, 
            144959613005987840, 362258295026614272, 724516590053228544, 1449033180106457088, 2898066360212914176, 
            5796132720425828352, 11592265440851656704, 4665729213955833856
            )


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


    def pawnMoves(self, index):
        # given index of a pawn check in front to see if it is blocked by a piece
        #   - do this using a mask for all pieces on the board and the bitboard representing the square in front of current pawn
        # then check to the left and right in front of the pawn to see if it can capture a piece
        #   - use mask of squares attacked by current pawn and mask of enemy pieces
        # if pawn is in the a or h file, then it cannot attack diagonally outside the board
        # does not have code from stopping a white pawn from going from 8th rank to 9th and similarly for black
        uint64 = 18446744073709551615                    # use this to & a binary string and limit to only 64 bits
        pawnBb = self.index2Bitboard(index)
        pieceMask = self.pieceMask()
        if self.board[index] == "P":
            pawnForwardMask = pawnBb << 8 if self.fileRank[index][1] != 2 else pawnBb << 8 | pawnBb << 16
            enemyMask = self.enemyMask(True)
            if self.fileRank[index][0] == "a":
                return ((pawnForwardMask & pieceMask) | ((pawnBb << 8 & pieceMask) << 8)) ^ pawnForwardMask | pawnBb << 9 & enemyMask & uint64
            elif self.fileRank[index][0] == "h":
                return ((pawnForwardMask & pieceMask) | ((pawnBb << 8 & pieceMask) << 8)) ^ pawnForwardMask | pawnBb << 7 & enemyMask & uint64
            return ((pawnForwardMask & pieceMask) | ((pawnBb << 8 & pieceMask) << 8)) ^ pawnForwardMask | pawnBb << 7 & enemyMask | pawnBb << 9 & enemyMask & uint64
        elif self.board[index] == 'p':
            pawnForwardMask = pawnBb >> 8 if self.fileRank[index][1] != 7 else pawnBb >> 8 | pawnBb >> 16
            enemyMask = self.enemyMask(False)
            enemyMask |= enemyMask >> 8
            if self.fileRank[index][0] == "a":
                return ((pawnForwardMask & pieceMask) | ((pawnBb >> 8 & pieceMask) >> 8)) ^ pawnForwardMask | pawnBb >> 7 & enemyMask & uint64
            elif self.fileRank[index][0] == "h":
                return ((pawnForwardMask & pieceMask) | ((pawnBb >> 8 & pieceMask) >> 8)) ^ pawnForwardMask | pawnBb >> 9 & enemyMask & uint64
            return ((pawnForwardMask & pieceMask) | ((pawnBb >> 8 & pieceMask) >> 8)) ^ pawnForwardMask | pawnBb >> 7 & enemyMask | pawnBb >> 9 & enemyMask & uint64  
        print("Not a Pawn")
        return 0
    
    def knightMovesGen(self, index):
        uint64 = 18446744073709551615                    # use this to & a binary string and limit to only 64 bits
        notGH = 4557430888798830399
        notAB = 18229723555195321596
        knightBb = self.index2Bitboard(index)
        knightBb = (knightBb << 6 | knightBb << 10 | knightBb << 15 | knightBb << 17 | knightBb >> 6 | knightBb >> 10 | knightBb >> 15 | knightBb >> 17) & uint64
        if self.fileRank[index][0] == "a" or self.fileRank[index][0] == "b":
            return knightBb & notGH
        elif self.fileRank[index][0] == "g" or self.fileRank[index][0] == "h":
            return knightBb & notAB
        return knightBb
    
    def kingMovesGen(self, index):
        uint64 = 18446744073709551615                    # use this to & a binary string and limit to only 64 bits
        notGH = 4557430888798830399
        notAB = 18229723555195321596
        kingBb = self.index2Bitboard(index)
        kingBb =  (kingBb << 9 | kingBb << 8 | kingBb << 7 | kingBb << 1 | kingBb >> 1 | kingBb >> 7 | kingBb >> 8 | kingBb >> 9) & uint64
        if self.fileRank[index][0] == 'a':
            return kingBb & notGH 
        elif self.fileRank[index][0] == 'h':
            return kingBb & notAB
        return kingBb

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
print("---------------")

