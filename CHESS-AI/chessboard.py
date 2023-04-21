import struct
import numpy as np


class Board:

    # Board initializes with instance variables fen, board and bitboard. There is also a fileRank
    # which is used to help get the file rank mapping of a piece square given index of board.
    # Each board is represented in three ways: board, fen, and bitboards.
    # (Board) A list of length 64 which contains information for the pieces on each
    # square of the board. Uppercase letters denote WHITE, lowercase denotes BLACK and "." denotes nothing.
    # (FEN) A fen string.
    # (Bitboards) Bitboards are used to represent sets of pieces. These sets can represents a number of different
    # types of squares (pieces, attacked squares, possible moves, pieces blocking sliding pieces, etc) and can be
    # manipulated efficiently using bit operations such as AND/OR. Piece bitboards are represented in a dictionary
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

        self.fileRank2index = {
            "a1": 0, "b1": 1, "c1": 2, "d1": 3, "e1": 4, "f1": 5, "g1": 6, "h1": 7,
            "a2": 8, "b2": 9, "c2": 10, "d2": 11, "e2": 12, "f2": 13, "g2": 14, "h2": 15,
            "a3": 16, "b3": 17, "c3": 18, "d3": 19, "e3": 20, "f3": 21, "g3": 22, "h3": 23,
            "a4": 24, "b4": 25, "c4": 26, "d4": 27, "e4": 28, "f4": 29, "g4": 30, "h4": 31,
            "a5": 32, "b5": 33, "c5": 34, "d5": 35, "e5": 36, "f5": 37, "g5": 38, "h5": 39,
            "a6": 40, "b6": 41, "c6": 42, "d6": 43, "e6": 44, "f6": 45, "g6": 46, "h6": 47,
            "a7": 48, "b7": 49, "c7": 50, "d7": 51, "e7": 52, "f7": 53, "g7": 54, "h7": 55,
            "a8": 56, "b8": 57, "c8": 58, "d8": 59, "e8": 60, "f8": 61, "g8": 62, "h8": 63
        }

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
            "K": 0b0,
            "white": 0b0,
            "black": 0b0,
            "whiteatk": 0b0,
            "blackatk": 0b0,
            ".": 0
        }

        self.enpassant = 0

        self.fileMasks = {
            0: 72340172838076673,
            1: 144680345676153346,
            2: 289360691352306692,
            3: 578721382704613384,
            4: 1157442765409226768,
            5: 2314885530818453536,
            6: 4629771061636907072,
            7: 9259542123273814144
        }

        self.rankMasks = {
            0: 255,
            1: 65280,
            2: 16711680,
            3: 4278190080,
            4: 1095216660480,
            5: 280375465082880,
            6: 71776119061217280,
            7: 18374686479671623680,
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

        self.bishopForeslash = (
            9241421688590303744, 36099303471055872, 141012904183808, 550831656960, 2151686144, 8404992, 32768, 0, 4620710844295151616,
            9241421688590303233, 36099303471054850, 141012904181764, 550831652872, 2151677968, 8388640, 64, 2310355422147510272,
            4620710844295020800, 9241421688590041601, 36099303470531586, 141012903135236, 550829559816, 2147491856, 16416, 1155177711056977920,
            2310355422114021376, 4620710844228043008, 9241421688456086017, 36099303202620418, 141012367312900, 549757915144, 4202512, 577588851233521664,
            1155177702483820544, 2310355404967706624, 4620710809935413504, 9241421619870827009, 36099166032102402, 140738026276868, 1075843080,
            288793326105133056, 577586656505233408, 1155173313027244032, 2310346626054553600, 4620693252109107456, 9241386504218214913,
            36028934726878210, 275415828484, 144115188075855872, 288231475663339520, 576462955621646336, 1152925911260069888, 2305851822520205312,
            4611703645040410880, 9223407290080821761, 70506452091906, 0, 281474976710656, 564049465049088, 1128103225065472, 2256206466908160,
            4512412933881856, 9024825867763968, 18049651735527937
        )

        self.bishopBackslash = (
            0, 256, 66048, 16909312, 4328785920, 1108169199616, 283691315109888, 72624976668147712, 2, 65540, 16908296, 4328783888, 1108169195552,
            283691315101760, 72624976668131456, 145249953336262656, 516, 16778248, 4328523792, 1108168675360, 283691314061376, 72624976666050688,
            145249953332101120, 290499906664136704, 132104, 4295231504, 1108102090784, 283691180892224, 72624976399712384, 145249952799424512,
            290499905598783488, 580999811180789760, 33818640, 1099579265056, 283674135240768, 72624942308409472, 145249884616818688, 290499769233571840,
            580999538450366464, 1161999072605765632, 8657571872, 281492291854400, 72620578621636736, 145241157243273216, 290482314486480896,
            580964628956184576, 1161929253617401856, 2323857407723175936, 2216338399296, 72062026714726528, 144124053429452800, 288248106858840064,
            576496213700902912, 1152992423106838528, 2305983746702049280, 4611686018427387904, 567382630219904, 1134765260439552, 2269530520813568,
            4539061024849920, 9078117754732544, 18155135997837312, 36028797018963968, 0
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

        self.queenMoves = (
            9313761861428380670, 180779649147209725, 289501704256556795, 578721933553179895, 1157442771889699055, 2314886638996058335,
            4630054752952049855, 9332167099941961855, 4693051017133293059, 9386102034266586375, 325459994840333070, 578862399937640220,
            1157444424410132280, 2315169224285282160, 4702396038313459680, 9404792076610076608, 2382695595002168069, 4765391190004401930,
            9530782384287059477, 614821794359483434, 1157867469641037908, 2387511058326581416, 4775021017124823120, 9550042029937901728,
            1227517888139822345, 2455035776296487442, 4910072647826412836, 9820426766351346249, 1266167048752878738, 2460276499189639204,
            4920271519124312136, 9840541934442029200, 649930110732142865, 1299860225776030242, 2600000831312176196, 5272058161445620104,
            10544115227674579473, 2641485286422881314, 5210911883574396996, 10421541192660455560, 361411684042608929, 722824471891812930,
            1517426162373248132, 3034571949281478664, 6068863523097809168, 12137446670713758241, 5827868887957914690, 11583398706901190788,
            287670746360127809, 575624067208594050, 1079472019650937860, 2087167920257370120, 4102559721436811280, 8133343319517438240,
            16194909420462031425, 13871017173176583298, 18303478847064064385, 18232552689433215490, 18090419998706369540, 17806153522019305480,
            17237620560088797200, 16100553540994408480, 13826139127340482880, 9205534180971414145
        )

    # function that takes self.board from the Board object and populates self.bitboards

    def board2Bitboard(self):

        for key in self.bitboards.keys():
            self.bitboards[key] = 0b0
        # iterates over board
        for pieceIndex in range(63, -1, -1):
            # iterates of the keys of bitboards dictionary, if the piece == key, then a 1 bit is appended to the piece bitboard
            # otherwise the piece bitboard is shifted 1 to the left (append a 0 bit)
            for key in self.bitboards.keys():
                self.bitboards[key] <<= 1
                if self.board[pieceIndex] == key:
                    self.bitboards[key] |= 0b1
        self.bitboards["white"] = self.bitboards['B'] | self.bitboards['N'] | self.bitboards[
            'R'] | self.bitboards['Q'] | self.bitboards['P'] | self.bitboards['K']
        self.bitboards["black"] = self.bitboards['b'] | self.bitboards['n'] | self.bitboards[
            'r'] | self.bitboards['q'] | self.bitboards['p'] | self.bitboards['k']
        self.bitboards["whiteatk"] = self.attackedSquares("white")
        self.bitboards["blackatk"] = self.attackedSquares("black")

    def pawnMoves(self, index):
        # given index of a pawn check in front to see if it is blocked by a piece
        #   - do this using a mask for all pieces on the board and the bitboard representing the square in front of current pawn
        # then check to the left and right in front of the pawn to see if it can capture a piece
        #   - use mask of squares attacked by current pawn and mask of enemy pieces
        # if pawn is in the a or h file, then it cannot attack diagonally outside the board
        # does not have code from stopping a white pawn from going from 8th rank to 9th and similarly for black
        # use this to & a binary string and limit to only 64 bits
        uint64 = 18446744073709551615
        # create bitboards of the pawn and bitboard off all pieces on the board
        pawnBb = 0b1 << index
        pieceMask = self.bitboards["white"] | self.bitboards["black"]
        # first if block determines the color of the piece
        if self.board[index] == "P":
            # pawnForwardMask is mask of piece in front of a pawn. If the pawn is in the starting rank,
            # then it also contains another set bit two spaces in front of the pawn
            pawnForwardMask = pawnBb << 8
            enemyMask = self.bitboards["black"]
            # there are three cases for pawn attacks. If it is in the a file, then we will not check the square to front left for enemy
            # if in the h file, then we will not check the square to the front right
            # otherwise, we check both front left and right for an enemy piece

            # general formula for generating pawn move and attack bitboard is as follows:
            # (mask contain any enemy pieces blocking pawn) XOR (mask of square in front of pawn and any enemies that can be attacked by pawn)
            if self.fileRank[index][1] == 2 and 0b1 << (index + 8) & pieceMask == 0:
                pawnForwardMask |= pawnBb << 16
            if index % 8 == 0:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb << 9 & enemyMask))) | (pawnBb << 9 & self.enpassant)) & uint64
            elif index % 8 == 7:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb << 7 & enemyMask))) | (pawnBb << 7 & self.enpassant)) & uint64
            return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb << 7 & enemyMask | pawnBb << 9 & enemyMask))) | ((pawnBb << 7 | pawnBb << 9) & self.enpassant)) & uint64
        elif self.board[index] == 'p':
            pawnForwardMask = pawnBb >> 8
            enemyMask = self.bitboards["white"]
            if self.fileRank[index][1] == 7 and 0b1 << (index - 8) & pieceMask == 0:
                pawnForwardMask |= pawnBb >> 16
            if index % 8 == 0:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb >> 7 & enemyMask))) | (pawnBb >> 7 & self.enpassant)) & uint64
            elif index % 8 == 7:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb >> 9 & enemyMask))) | (pawnBb >> 9 & self.enpassant)) & uint64
            return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb >> 7 & enemyMask | pawnBb >> 9 & enemyMask))) | ((pawnBb >> 7 | pawnBb >> 9) & self.enpassant)) & uint64
        # returns 0 if the index does not refer to a pawn
        print("Not a Pawn")
        return 0

    # used to generate knight moves bitboards for all squares (These values are stored in self.knightMoves)
    # we do not call this function, it was only used to generate bitboards
    def knightMovesGen(self, index):
        # use this to & a binary string and limit to only 64 bits
        uint64 = 18446744073709551615
        notGH = 4557430888798830399
        notAB = 18229723555195321596
        knightBb = 0b1 << index

        # knight moves generated by OR'ing together shifted copies of the knight bitboard
        knightBb = (knightBb << 6 | knightBb << 10 | knightBb << 15 | knightBb << 17 |
                    knightBb >> 6 | knightBb >> 10 | knightBb >> 15 | knightBb >> 17) & uint64

        # if block ensures that moves do not wrap from one edge of the board to the other
        if self.fileRank[index][0] == "a" or self.fileRank[index][0] == "b":
            return knightBb & notGH
        elif self.fileRank[index][0] == "g" or self.fileRank[index][0] == "h":
            return knightBb & notAB
        return knightBb

    # used to generate king moves bitboards for all squares (Values are stored in self.kingMoves)
    # we do not call this function, it was only used to generate bitboards
    def kingMovesGen(self, index):
        # use this to & a binary string and limit to only 64 bits
        uint64 = 18446744073709551615
        notGH = 4557430888798830399
        notAB = 18229723555195321596
        kingBb = 0b1 << index

        # King moves are generated by OR'ing together 8 shifted copies of the king bitboard
        kingBb = (kingBb << 9 | kingBb << 8 | kingBb << 7 | kingBb << 1 |
                  kingBb >> 1 | kingBb >> 7 | kingBb >> 8 | kingBb >> 9) & uint64

        # this if block is used to avoid king moves from wrapping around to the opposite side of the board
        if self.fileRank[index][0] == 'a':
            return kingBb & notGH
        elif self.fileRank[index][0] == 'h':
            return kingBb & notAB
        return kingBb

    # generates a bitboard of all possible moves a bishop could make at a given index (stored in self.bishopMoves)
    # ignores blockers
    # (DEPRECATED) use bishopAttack instead
    def bishopMovesGen(self, index):
        uint64 = 18446744073709551615
        bishopBb = 0b0
        rank = index//8
        file = index % 8
        atk_rank = rank + 1
        atk_file = file + 1
        while atk_rank < 8 and atk_file < 8:  # Northeast
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank += 1
            atk_file += 1
        atk_rank = rank + 1
        atk_file = file - 1
        while atk_rank < 8 and atk_file >= 0:  # Northwest
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank += 1
            atk_file -= 1
        atk_rank = rank - 1
        atk_file = file - 1
        while atk_rank >= 0 and atk_file >= 0:  # Southwest
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank -= 1
            atk_file -= 1
        atk_rank = rank - 1
        atk_file = file + 1
        while atk_rank >= 0 and atk_file < 8:  # Southeast
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank -= 1
            atk_file += 1
        return bishopBb

    # generates a bitboard of the northeast and southwest rays of a bishop
    # ignores blockers
    def bishopForeslashGen(self, index):
        uint64 = 18446744073709551615
        bishopBb = 0b0
        rank = index//8
        file = index % 8
        atk_rank = rank + 1
        atk_file = file + 1
        while atk_rank < 8 and atk_file < 8:  # Northeast
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank += 1
            atk_file += 1
        atk_rank = rank - 1
        atk_file = file - 1
        while atk_rank >= 0 and atk_file >= 0:  # Southwest
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank -= 1
            atk_file -= 1
        return bishopBb

    # generates a bitboard of the northwest and southeast rays of a bishop
    # ignores blockers
    def bishopBackslashGen(self, index):
        uint64 = 18446744073709551615
        bishopBb = 0b0
        rank = index//8
        file = index % 8
        atk_rank = rank + 1
        atk_file = file - 1
        while atk_rank < 8 and atk_file >= 0:  # Northwest
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank += 1
            atk_file -= 1
        atk_rank = rank - 1
        atk_file = file + 1
        while atk_rank >= 0 and atk_file < 8:  # Southeast
            bishopBb = (bishopBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_rank -= 1
            atk_file += 1
        return bishopBb

# Bishop and Rook attacks are calculated by using the propagation of carry bits in bitwise subtraction to find a blocker.
# (in little endian convention)
#   01000011 occupied pieces
# - 01000000 sliding piece
#   00000011 blocker pieces
# The sliding piece is cleard from the occupancy board to set up for carry bit propagation.
#
#   00000011 blocker pieces
# - 01000000 sliding piece
#   01111101 the carry bit is propagated until the bit before the blocker
#
#     01000011 occupied pieces
# xor 01111101 (blocker - sliding) piece
#     00111110 gets the possible moves of the slider in the positive horizontal direction (including capture)
#
# This method only works in the positive direction and can only detect the first blocker in its propagation.
# To get the negative direction moves, the bitboards involved have their endianess reversed with bitSwap() and the same calculations are made
# To get multiple blockers in each propagation, the method is ran multiple times with different piece masks
#   https://www.chessprogramming.org/Efficient_Generation_of_Sliding_Piece_Attacks#Sliding_Attacks_by_Calculation
#   https://www.chessprogramming.org/Subtracting_a_Rook_from_a_Blocking_Piece

    # Generates a bitboard of all possible moves of a bishop taking blockers into account
    # includes piece capture moves
    # does not check if the move leaves the king in check, making these pseudovalid moves.

    def bishopAttack(self, index, isBlack: bool):

        # foreslash (northeast and southwest)
        # bitboard of northeast and southwest rays
        atk_mask = self.bishopForeslash[index]
        pieceBb = 0b1 << index                      # position bitboard of current piece
        # bitboard of all the pieces on the board, (including the current one)
        occupancyBb = self.bitboards['white'] | self.bitboards['black']
        # bitboard to calculate northeast moves
        positiveRayBb = occupancyBb & atk_mask
        # Anding with the attack mask implicitly does the first subraction to clear the piece from the occupancy
        # Reversed bitboard to calculate southwest moves
        negativeRayBb = self.bitSwap(positiveRayBb)
        # Subtraction to propagate carry bit
        positiveRayBb = (positiveRayBb - pieceBb)
        negativeRayBb = negativeRayBb - self.bitSwap(pieceBb)
        # No need to xor with occupancy bitboard since the parts of each RayBb that were not affected by propagation are the same as occupancy.
        foreslashRays = positiveRayBb ^ self.bitSwap(negativeRayBb)
        foreslashRays = foreslashRays & atk_mask

        # backslash (northwest and southeast)
        atk_mask = self.bishopBackslash[index]
        pieceBb = 0b1 << index
        occupancyBb = self.bitboards['white'] | self.bitboards['black']
        positiveRayBb = occupancyBb & atk_mask
        negativeRayBb = self.bitSwap(positiveRayBb)
        positiveRayBb = (positiveRayBb - pieceBb)
        negativeRayBb = negativeRayBb - self.bitSwap(pieceBb)
        backslashRays = positiveRayBb ^ self.bitSwap(negativeRayBb)
        backslashRays = backslashRays & atk_mask

        color = 'white'
        if isBlack:
            color = 'black'

        rays = foreslashRays | backslashRays

        # to remove moves that capture ally blockers
        atkBb = (rays ^ self.bitboards[color]) & rays
        return atkBb

    # generates a bitboard of all possible moves a rook could make at a given index
    # ignores blockers

    def rookMovesGen(self, index):
        uint64 = 18446744073709551615
        rookBb = 0b0
        rank = index//8
        file = index % 8
        atk_rank = rank + 1
        while atk_rank < 8:  # North
            rookBb = (rookBb | (0b1 << (atk_rank*8 + file))) & uint64
            atk_rank += 1
        atk_rank = rank - 1
        while atk_rank >= 0:  # South
            rookBb = (rookBb | (0b1 << (atk_rank*8 + file))) & uint64
            atk_rank -= 1
        atk_file = file + 1
        while atk_file < 8:  # East
            rookBb = (rookBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_file += 1
        atk_file = file - 1
        while atk_file >= 0:  # West
            rookBb = (rookBb | (0b1 << (atk_rank*8 + atk_file))) & uint64
            atk_file -= 1
        return rookBb

    # Generates a bitboard of all possible moves of a rook taking blockers into account
    # includes piece capture moves
    # does not check if the move leaves the king in check, making these pseudovalid moves.
    def rookAttack(self, index, isBlack: bool):

        file = index % 8
        # Vertical Rays
        atk_mask = self.fileMasks[file]
        pieceBb = 0b1 << index
        occupancyBb = self.bitboards['white'] | self.bitboards['black']
        # need to perform additional subtraction since atk_mask doesn't clear position bit of the piece
        upRay = occupancyBb & atk_mask - pieceBb
        downRay = self.bitSwap(upRay)
        upRay = (upRay - pieceBb)
        downRay = downRay - self.bitSwap(pieceBb)
        verticalRays = upRay ^ self.bitSwap(downRay)
        verticalRays = verticalRays & atk_mask

        rank = index//8
        # Horizontal Rays (northweast and southeast)
        atk_mask = self.rankMasks[rank]
        pieceBb = 0b1 << index
        occupancyBb = self.bitboards['white'] | self.bitboards['black']
        rightRay = occupancyBb & atk_mask - pieceBb
        leftRay = self.bitSwap(rightRay)
        rightRay = (rightRay - pieceBb)
        leftRay = leftRay - self.bitSwap(pieceBb)
        horizontalRays = rightRay ^ self.bitSwap(leftRay)
        horizontalRays = horizontalRays & atk_mask

        color = 'white'
        if isBlack:
            color = 'black'

        rays = verticalRays | horizontalRays

        atkBb = (rays ^ self.bitboards[color]) & rays
        return atkBb

    # generates a bitboard of all possible moves a queen could make at a given index
    # bitwise or of rook and bishop moves
    # ignores blockers
    def queenMovesGen(self, index):
        return self.rookMovesGen(index) | self.bishopMovesGen(index)

    # given a starting index, ending index and color of piece, this function checks to see if the move is valid
    # if it is valid, then the move is made by making the appropriate updates to self.board and self.bitboards
    # returns True if the move is successfully executed, false otherwise

    def makeMove(self, start, end, lookingForward=False):
        if lookingForward or 0b1 << end & self.legalMoves(start):
            if 0b1 << start & self.bitboards['p']:
                if start // 8 == 6 and end // 8 == 4:
                    self.enpassant = 0b1 << (end + 8)
                elif 0b1 << end & self.enpassant:
                    self.bitboards[self.board[end + 8]] = self.toggleBit(self.bitboards[self.board[end + 8]], end + 8)
                    print()
                    self.printBitboard(self.bitboards[self.board[end+8]])
                    self.board[end + 8] = "."
                    self.enpassant = 0
                else:
                    self.enpassant = 0
            elif 0b1 << start & self.bitboards['P']:
                if start // 8 == 1 and end // 8 == 3:
                    self.enpassant = 0b1 << (end - 8)
                elif 0b1 << end & self.enpassant:
                    self.bitboards[self.board[end - 8]] = self.toggleBit(self.bitboards[self.board[end - 8]], end - 8)
                    print()
                    self.printBitboard(self.bitboards[self.board[end-8]])
                    self.board[end - 8] = "."
                    self.enpassant = 0
                else:
                    self.enpassant = 0
            else:
                self.enpassant = 0
            
            # if a piece is taken, then the bit corresponding to that index in the taken piece's bitboard is cleared
            if self.board[end] != ".":
                self.bitboards[self.board[end]] = self.toggleBit(
                    self.bitboards[self.board[end]], end)

            # update the bitboard of the moved piece
            self.bitboards[self.board[start]] = self.toggleBit(
                self.toggleBit(self.bitboards[self.board[start]], start), end)

            # update the board to represent to move
            self.board[end], self.board[start] = self.board[start], "."

            # update the bitboards of white and black pieces
            self.bitboards["white"] = self.bitboards['B'] | self.bitboards['N'] | self.bitboards[
                'R'] | self.bitboards['Q'] | self.bitboards['P'] | self.bitboards["K"]
            self.bitboards["black"] = self.bitboards['b'] | self.bitboards['n'] | self.bitboards[
                'r'] | self.bitboards['q'] | self.bitboards['p'] | self.bitboards['k']
            return True
        else:
            print("Not a valid move")
            return False

   

    # Generates a bitboard of all possible moves of a queen taking blockers into account
    # includes piece capture moves
    # bitwise or of the rookAttack and bishopAttack
    # does not check if the move leaves the king in check, making these pseudovalid moves.
    def queenAttack(self, index, isBlack: bool):
        return self.rookAttack(index, isBlack) | self.bishopAttack(index, isBlack)

    # Calls makeMove on every possible pseudovalid moves of the piece at the given index.
    # If the king is in check after the pseudovalid move, that move bit is toggled off
    # returns a bitboard of all the legal moves
    def legalMoves(self, index):
        legalBb = self.pseudovalidMoves(index)
        tempBb = legalBb #temporary bitboard used to iterate all the bits on a bitboard.
        enemyatk = 'white'
        king = 'k'
        if (self.board[index].isupper()):
            enemyatk = 'black'
            king = 'K'

        while tempBb > 0:
            end = self.bitboard2Index(tempBb)
            self.printBitboard(tempBb)
            print(bin(tempBb))
            print(bin(18446744073709551615))
            print(tempBb)
            print(index, end)
            prevBoardStart, prevBoardEnd = self.board[index], self.board[end]           #Storing initial board and piece bitboards
            prevStartBb = self.bitboards[self.board[index]]
            prevEndPiece = self.board[end]
            prevWhiteBb = self.bitboards["white"]
            prevBlackBb = self.bitboards["black"]
            prevEnpassant = self.enpassant
            didEnpassant = 0 # 0 for no, 1 for white, -1 for black
            
            # if the move is enpassant, then we store the enemy bitboard?

            if 0b1 << end & self.enpassant:
                if 0b1 << index & self.bitboards['p']:
                    prevBoardEnd = self.board[end+8]
                    prevEndPieceBb = self.bitboards[prevBoardEnd]
                    didEnpassant = -1
                elif 0b1 << index & self.bitboards['P']:
                    prevBoardEnd = self.board[end-8]
                    prevEndPieceBb = self.bitboards[prevBoardEnd]
                    didEnpassant = 1
            elif prevEndPiece != ".":
                prevEndPieceBb = self.bitboards[self.board[end]]

            self.makeMove(index, end, True)

            enemyatkBb = self.attackedSquares(enemyatk)

            if(self.bitboards[king] & enemyatkBb):        #Checks if king is in check
                legalBb = self.toggleBit(legalBb, end)

            self.board[index] = prevBoardStart         # restoring board and piece bitboards to initial positions
            self.bitboards[self.board[index]]  = prevStartBb
            if didEnpassant < 0:
                self.board[end] = '.'
                self.board[end + 8] = prevBoardEnd
                self.bitboards[prevBoardEnd] = prevEndPieceBb
            elif didEnpassant > 0:
                self.board[end] = '.'
                self.board[end - 8] = prevBoardEnd
                self.bitboards[prevBoardEnd] = prevEndPieceBb
            elif prevEndPiece != ".":
                self.board[end] = prevBoardEnd
                self.bitboards[prevBoardEnd] = prevEndPieceBb
            else:
                self.board[end] = '.'
                self.bitboards[end] = 0
            self.bitboards["white"] = prevWhiteBb
            self.bitboards["black"] = prevBlackBb
            self.enpassant = prevEnpassant
            tempBb = self.toggleBit(tempBb, end)
        return legalBb

    # Returns a bitboard of the pseudovalid moves a piece could make at the given index.
    # wrapper function for all the move bitboard generators
    def pseudovalidMoves(self, index):
        temp = self.board[index]
        if temp == "p":
            return self.pawnMoves(index)
        elif temp == "n":
            return self.validKnightMoves(index, True)
        elif temp == "q":
            return self.queenAttack(index, True)
        elif temp == "b":
            return self.bishopAttack(index, True)
        elif temp == "r":
            return self.rookAttack(index, True)
        elif temp == "k":
            return self.validKingMoves(index, True)
        elif temp == "P":
            return self.pawnMoves(index)
        elif temp == "N":
            return self.validKnightMoves(index, False)
        elif temp == "Q":
            return self.queenAttack(index, False)
        elif temp == "B":
            return self.bishopAttack(index, False)
        elif temp == "R":
            return self.rookAttack(index, False)
        elif temp == "K":
            return self.validKingMoves(index, False)
        else:
            return 0

    # TODO: make king unable to move to attacked squares
    # returns bitboard of all legal squares the king can move to
    def validKingMoves(self, index, isBlack):
        if isBlack:
            return (self.kingMoves[index] & (self.bitboards["whiteatk"] | self.bitboards["black"])) ^ self.kingMoves[index]
        return (self.kingMoves[index] & (self.bitboards["blackatk"] | self.bitboards["white"])) ^ self.kingMoves[index]

    # TODO: does not currently return value if in check
    # the function returns the status of the game (Checkmate, stalemate, check, or nothing)
    def check(self, index, isBlack):
        moves = self.legalMoves(index)
        if isBlack:
            print("isBlack is True,")
            king = self.bitboards["k"]
            oppAtk = self.attackedSquares("white")
        else:
            print("isBlack is false")
            king = self.bitboards["K"]
            oppAtk = self.attackedSquares("black")
        # Checkmate not working right, need to ensure that oppatk & King bitboard > 1 for checkmate

        if moves == 0 and king & oppAtk > 0:
            if isBlack:
                for key in ('p', 'q', 'r', 'b', 'n'):
                    tempBb = self.bitboards[key]
                    while tempBb > 0:
                        i = self.bitboard2Index(tempBb)
                        if self.legalMoves(i) > 0:
                            print('Check')
                            return -2
                        tempBb = self.toggleBit(tempBb, i)
            else:
                for key in ('P', 'Q', 'R', 'B', 'N'):
                    tempBb = self.bitboards[key]
                    while tempBb > 0:
                        i = self.bitboard2Index(tempBb)
                        if self.legalMoves(i) > 0:
                            print('Check')
                            return -2
                        tempBb = self.toggleBit(tempBb, i)
            print("Checkmate")
            return -1
        elif king & oppAtk > 0:
            print('Check')
            return -2
        elif moves == 0b1 << index:
            print("Stalemate")
            return 0
        print("Not in Check")
        return 1

    # returns an integer that has its bit order reversed, endianess is reversed.

    def bitSwap(self, n):
        # return 18446744073709551615 - n (one's complement)
        result = 0
        for i in range(64):
            result <<= 1
            result |= n & 1
            n >>= 1
        return result

    # first AND knight moves and friendly team pieces to get overlap
    # then XOR knight moves with overlap to get valid knight moves
    def validKnightMoves(self, index, isBlack):
        if isBlack:
            friendlyColor = self.bitboards["black"]
        else:
            friendlyColor = self.bitboards["white"]
        overlap = self.knightMoves[index] & friendlyColor
        return self.knightMoves[index] ^ overlap

    # toggles a bit
    def toggleBit(self, bitboard, index):
        return bitboard ^ 0b1 << index

    # returns bitboard that has a 1 on each square that has a piece on it
    # deprecated (use self.bitboards["(white/black)"]) instead
    def pieceMask(self):
        pieceMask = 0b0
        for key in self.bitboards.keys():
            if key in ("R", "N", "B", "Q", "K", "P", "r", "n", "b", "q", "k", "p"):
                pieceMask |= self.bitboards[key]
        return pieceMask

    # given a boolean isBlack, if true, then generates bitboard mask of all white pieces
    # otherwise generates bitboard mask for black pieces
    def enemyMask(self, isBlack):
        enemyMask = 0b0
        if isBlack:
            for key in self.bitboards.keys():
                if key.isupper():
                    enemyMask |= self.bitboards[key]
        else:
            for key in self.bitboards.keys():
                if key.islower():
                    enemyMask |= self.bitboards[key]
        return enemyMask

    def attackedSquares(self, color):
        pieceBb = self.bitboards[color]
        attacked = 0b0
        while pieceBb > 0:
            index = self.bitboard2Index(pieceBb)
            pieceBb = self.toggleBit(pieceBb, index)
            if 0b1 << index & self.bitboards['P']:
                if index % 8 == 0:
                    attacked |= 0b1 << (index + 9)
                elif index % 8 == 7:
                    attacked |= 0b1 << (index + 7)
                else:
                    attacked |= 0b1 << (index + 7) | 0b1 << (index + 9)
            elif 0b1 << index & self.bitboards['p']:
                if index // 8 == 0:
                    continue
                elif index % 8 == 0:
                    attacked |= 0b1 << (index - 7)
                elif index % 8 == 7:
                    attacked |= 0b1 << (index - 9)
                else:
                    attacked |= 0b1 << (index - 7) | 0b1 << (index - 9)
            else:
                attacked |= self.pseudovalidMoves(index)
        return attacked

    # returns the board index of the smallest set bit given a bitboard
    # for instance index2Bitboard(0b111000000) returns 6
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
brd.board2Bitboard()