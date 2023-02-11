

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
            ("a", 1), ("b", 1), ("c", 1), ("d",
                                           1), ("e", 1), ("f", 1), ("g", 1), ("h", 1),
            ("a", 2), ("b", 2), ("c", 2), ("d",
                                           2), ("e", 2), ("f", 2), ("g", 2), ("h", 2),
            ("a", 3), ("b", 3), ("c", 3), ("d",
                                           3), ("e", 3), ("f", 3), ("g", 3), ("h", 3),
            ("a", 4), ("b", 4), ("c", 4), ("d",
                                           4), ("e", 4), ("f", 4), ("g", 4), ("h", 4),
            ("a", 5), ("b", 5), ("c", 5), ("d",
                                           5), ("e", 5), ("f", 5), ("g", 5), ("h", 5),
            ("a", 6), ("b", 6), ("c", 6), ("d",
                                           6), ("e", 6), ("f", 6), ("g", 6), ("h", 6),
            ("a", 7), ("b", 7), ("c", 7), ("d",
                                           7), ("e", 7), ("f", 7), ("g", 7), ("h", 7),
            ("a", 8), ("b", 8), ("c", 8), ("d",
                                           8), ("e", 8), ("f", 8), ("g", 8), ("h", 8)
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

        self.bishopMoves = (
            9241421688590303744, 36099303471056128, 141012904249856, 550848566272, 6480472064, 1108177604608, 283691315142656,
            72624976668147712, 4620710844295151618, 9241421688590368773, 36099303487963146, 141017232965652, 1659000848424,
            283693466779728, 72624976676520096, 145249953336262720, 2310355422147510788, 4620710844311799048, 9241421692918565393,
            36100411639206946, 424704217196612, 72625527495610504, 145249955479592976, 290499906664153120, 1155177711057110024,
            2310355426409252880, 4620711952330133792, 9241705379636978241, 108724279602332802, 145390965166737412, 290500455356698632,
            580999811184992272, 577588851267340304, 1155178802063085600, 2310639079102947392, 4693335752243822976, 9386671504487645697,
            326598935265674242, 581140276476643332, 1161999073681608712, 288793334762704928, 577868148797087808, 1227793891648880768,
            2455587783297826816, 4911175566595588352, 9822351133174399489, 1197958188344280066, 2323857683139004420, 144117404414255168,
            360293502378066048, 720587009051099136, 1441174018118909952, 2882348036221108224, 5764696068147249408, 11529391036782871041,
            4611756524879479810, 567382630219904, 1416240237150208, 2833579985862656, 5667164249915392, 11334324221640704, 22667548931719168,
            45053622886727936, 18049651735527937
        )

        self.rookMoves = (
            72340172838076926, 144680345676153597, 289360691352306939, 578721382704613623, 1157442765409226991, 2314885530818453727,
            4629771061636907199, 9259542123273814143, 72340172838141441, 144680345676217602, 289360691352369924, 578721382704674568,
            1157442765409283856, 2314885530818502432, 4629771061636939584, 9259542123273813888, 72340172854657281, 144680345692602882,
            289360691368494084, 578721382720276488, 1157442765423841296, 2314885530830970912, 4629771061645230144, 9259542123273748608,
            72340177082712321, 144680349887234562, 289360695496279044, 578721386714368008, 1157442769150545936, 2314885534022901792,
            4629771063767613504, 9259542123257036928, 72341259464802561, 144681423712944642, 289361752209228804, 578722409201797128,
            1157443723186933776, 2314886351157207072, 4629771607097753664, 9259542118978846848, 72618349279904001, 144956323094725122,
            289632270724367364, 578984165983651848, 1157687956502220816, 2315095537539358752, 4629910699613634624, 9259541023762186368,
            143553341945872641, 215330564830528002, 358885010599838724, 645993902138460168, 1220211685215703056, 2368647251370188832,
            4665518383679160384, 9259260648297103488, 18302911464433844481, 18231136449196065282, 18087586418720506884, 17800486357769390088,
            17226286235867156496, 16077885992062689312, 13781085504453754944, 9187484529235886208
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
        # use this to & a binary string and limit to only 64 bits
        uint64 = 18446744073709551615
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
        # use this to & a binary string and limit to only 64 bits
        uint64 = 18446744073709551615
        notGH = 4557430888798830399
        notAB = 18229723555195321596
        knightBb = self.index2Bitboard(index)
        knightBb = (knightBb << 6 | knightBb << 10 | knightBb << 15 | knightBb << 17 |
                    knightBb >> 6 | knightBb >> 10 | knightBb >> 15 | knightBb >> 17) & uint64
        if self.fileRank[index][0] == "a" or self.fileRank[index][0] == "b":
            return knightBb & notGH
        elif self.fileRank[index][0] == "g" or self.fileRank[index][0] == "h":
            return knightBb & notAB
        return knightBb

    def kingMovesGen(self, index):
        # use this to & a binary string and limit to only 64 bits
        uint64 = 18446744073709551615
        notGH = 4557430888798830399
        notAB = 18229723555195321596
        kingBb = self.index2Bitboard(index)
        kingBb = (kingBb << 9 | kingBb << 8 | kingBb << 7 | kingBb << 1 |
                  kingBb >> 1 | kingBb >> 7 | kingBb >> 8 | kingBb >> 9) & uint64
        if self.fileRank[index][0] == 'a':
            return kingBb & notGH
        elif self.fileRank[index][0] == 'h':
            return kingBb & notAB
        return kingBb

    def bishopMovesGen(self, index):
        uint64 = 18446744073709551615
        bishopBb = 0b0
        r = index//8
        f = index % 8
        atk_r = r + 1
        atk_f = f + 1
        while atk_r < 8 and atk_f < 8:  # Northeast
            bishopBb = (bishopBb | (0b1 << (atk_r*8 + atk_f))) & uint64
            atk_r += 1
            atk_f += 1
        atk_r = r + 1
        atk_f = f - 1
        while atk_r < 8 and atk_f >= 0:  # Northwest
            bishopBb = (bishopBb | (0b1 << (atk_r*8 + atk_f))) & uint64
            atk_r += 1
            atk_f -= 1
        atk_r = r - 1
        atk_f = f - 1
        while atk_r >= 0 and atk_f >= 0:  # Southwest
            bishopBb = (bishopBb | (0b1 << (atk_r*8 + atk_f))) & uint64
            atk_r -= 1
            atk_f -= 1
        atk_r = r - 1
        atk_f = f + 1
        while atk_r >= 0 and atk_f < 8:  # Southeast
            bishopBb = (bishopBb | (0b1 << (atk_r*8 + atk_f))) & uint64
            atk_r -= 1
            atk_f += 1
        return bishopBb

    def rookMovesGen(self, index):
        uint64 = 18446744073709551615
        knightBb = 0b0
        r = index//8
        f = index % 8
        atk_r = r + 1
        while atk_r < 8:  # North
            knightBb = (knightBb | (0b1 << (atk_r*8 + f))) & uint64
            atk_r += 1
        atk_r = r - 1
        while atk_r >= 0:  # South
            knightBb = (knightBb | (0b1 << (atk_r*8 + f))) & uint64
            atk_r -= 1
        atk_f = f + 1
        while atk_f < 8:  # East
            knightBb = (knightBb | (0b1 << (r*8 + atk_f))) & uint64
            atk_f += 1
        atk_f = f - 1
        while atk_f >= 0:  # West
            knightBb = (knightBb | (0b1 << (r*8 + atk_f))) & uint64
            atk_f -= 1
        return knightBb

    # toggles a bit

    def toggleBit(self, bitboard, index):
        return bitboard ^ 0b1 << index

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
# brd.fen2Board("bbrknqnr/pppppppp/8/8/8/8/PPPPPPPP/BBRKNQNR w KQkq - 0 1")
print("---------------")
# brd.printBitboard(brd.toggleBit(brd.knightMoves[34], 34))
print(brd.printBitboard(brd.rookMovesGen(23)))
