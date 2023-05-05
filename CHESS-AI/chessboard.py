import struct
import numpy as np
import json

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
        with open("./preloadedData.json", "r") as readFile:
            preloadedData = json.load(readFile)
        self.fileRank = preloadedData["fileRank"]
        self.fileRank2index = preloadedData["fileRank2index"]
        self.board = preloadedData["board"]
        self.bitboards = preloadedData["bitboards"]
        self.knightMoves = preloadedData["knightMoves"]
        self.kingMoves = preloadedData["kingMoves"]
        self.bishopMoves = preloadedData["bishopMoves"]
        self.bishopForeslash = preloadedData["bishopForeslash"]
        self.bishopBackslash = preloadedData["bishopBackslash"]
        self.rookMoves = preloadedData["rookMoves"]
        self.queenMoves = preloadedData["queenMoves"]

        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

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

        self.blackEnpassant = 0
        self.whiteEnpassant = 0

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
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb << 9 & enemyMask))) | (pawnBb << 9 & self.blackEnpassant)) & uint64
            elif index % 8 == 7:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb << 7 & enemyMask))) | (pawnBb << 7 & self.blackEnpassant)) & uint64
            return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb << 7 & enemyMask | pawnBb << 9 & enemyMask))) | ((pawnBb << 7 | pawnBb << 9) & self.blackEnpassant)) & uint64
        elif self.board[index] == 'p':
            pawnForwardMask = pawnBb >> 8
            enemyMask = self.bitboards["white"]
            if self.fileRank[index][1] == 7 and 0b1 << (index - 8) & pieceMask == 0:
                pawnForwardMask |= pawnBb >> 16
            if index % 8 == 0:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb >> 7 & enemyMask))) | (pawnBb >> 7 & self.whiteEnpassant)) & uint64
            elif index % 8 == 7:
                return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb >> 9 & enemyMask))) | (pawnBb >> 9 & self.whiteEnpassant)) & uint64
            return (((pawnForwardMask & pieceMask) ^ (pawnForwardMask | (pawnBb >> 7 & enemyMask | pawnBb >> 9 & enemyMask))) | ((pawnBb >> 7 | pawnBb >> 9) & self.whiteEnpassant)) & uint64
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
                    self.blackEnpassant = 0b1 << (end + 8)
                elif 0b1 << end & self.whiteEnpassant:
                    self.bitboards[self.board[end + 8]] = self.toggleBit(self.bitboards[self.board[end + 8]], end + 8)
                    self.board[end + 8] = "."
                    self.blackEnpassant = 0
                else:
                    self.blackEnpassant = 0
            elif 0b1 << start & self.bitboards['P']:
                if start // 8 == 1 and end // 8 == 3:
                    self.whiteEnpassant = 0b1 << (end - 8)
                elif 0b1 << end & self.blackEnpassant:
                    self.bitboards[self.board[end - 8]] = self.toggleBit(self.bitboards[self.board[end - 8]], end - 8)
                    self.board[end - 8] = "."
                    self.whiteEnpassant = 0
                else:
                    self.whiteEnpassant = 0
            else:
                self.whiteEnpassant = 0
                self.blackEnpassant = 0
            
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
            prevBoardStart, prevBoardEnd = self.board[index], self.board[end]           #Storing initial board and piece bitboards
            prevStartBb = self.bitboards[self.board[index]]
            prevEndPiece = self.board[end]
            prevWhiteBb = self.bitboards["white"]
            prevBlackBb = self.bitboards["black"]
            prevBlackEnpassant = self.blackEnpassant
            prevWhiteEnpassant = self.whiteEnpassant
            didEnpassant = 0 # 0 for no, 1 for white, -1 for black
            
            # if the move is enpassant, then we store the enemy bitboard?

            if 0b1 << end & (self.blackEnpassant | self.whiteEnpassant):
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
                legalBb ^= 0b1 << end

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
            self.blackEnpassant = prevBlackEnpassant
            self.whiteEnpassant = prevWhiteEnpassant
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
            # print("isBlack is True,")
            king = self.bitboards["k"]
            oppAtk = self.attackedSquares("white")
        else:
            # print("isBlack is false")
            king = self.bitboards["K"]
            oppAtk = self.attackedSquares("black")
        # brd.printBitboard(king)
        # print()
        # brd.printBitboard(oppAtk)
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
        # print("Not in Check")
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
            pieceBb ^= 0b1 << index
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