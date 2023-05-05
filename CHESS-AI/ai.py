import chessboard as cb
import cProfile
import pstats
import timeit
import time
class AI:

    def __init__(self):

        self.boardObj = cb.Board()
        self.boardObj.board2Bitboard()
        self.legalMoves = []


    def evaluate(self, start, end, isBlack):
        boardCopy = self.boardObj.board.copy()
        bitboardsCopy = self.boardObj.bitboards.copy()
        self.boardObj.makeMove(start, end)
        
        selfMaterial, enemyMaterial, selfMobility, enemyMobility = 0, 0, 0, 0

        if isBlack:
            selfMaterial, enemyMaterial, selfMobility, enemyMobility = self.countMaterial()
        else:
            enemyMaterial, selfMaterial, enemyMobility, selfMobility = self.countMaterial()
        self.boardObj.board = boardCopy
        self.boardObj.bitboards = bitboardsCopy

        return selfMaterial - enemyMaterial + (selfMobility - enemyMobility)
    
    
    def countMaterial(self):
        blackMaterial, whiteMaterial, blackMobility, whiteMobility = 0, 0, 0, 0
        for type in ('p', 'n', 'b', 'r', 'q', 'k'):
            pieces = self.boardObj.bitboards[type]
            while pieces > 0:

                index = self.boardObj.bitboard2Index(pieces)

                possibleMoves = self.boardObj.legalMoves(index)
                while possibleMoves > 0:
                    blackMobility += 1
                    possibleMoves &= possibleMoves - 1

                if type == 'p':
                    blackMaterial += 1
                elif type == 'n':
                    blackMaterial += 3
                elif type == 'b':
                    blackMaterial += 3
                elif type == 'r':
                    blackMaterial += 5
                elif type == 'q':
                    blackMaterial += 9
                else:
                    blackMaterial += 200
                pieces &= pieces - 1
                
        for type in ('P', 'N', 'B', 'R', 'Q', 'K'):
            pieces = self.boardObj.bitboards[type]
            while pieces > 0:

                index = self.boardObj.bitboard2Index(pieces)

                possibleMoves = self.boardObj.legalMoves(index)
                while possibleMoves > 0:
                    whiteMobility += 1
                    possibleMoves ^= 0b1 << self.boardObj.bitboard2Index(possibleMoves)

                if type == 'P':
                    whiteMaterial += 1
                elif type == 'N':
                    whiteMaterial += 3
                elif type == 'B':
                    whiteMaterial += 3
                elif type == 'R':
                    whiteMaterial += 5
                elif type == 'Q':
                    whiteMaterial += 9
                else:
                    whiteMaterial += 200
                pieces &= pieces - 1

        return blackMaterial, whiteMaterial, blackMobility, whiteMobility
    

    def getMoves(self):
        pieces = self.boardObj.bitboards['white'] | self.boardObj.bitboards['black']
        while pieces > 0:
            index = self.boardObj.bitboard2Index(pieces)
            possibleMoves = self.boardObj.legalMoves(index)
            while possibleMoves > 0:
                self.legalMoves.append((index, self.boardObj.bitboard2Index(possibleMoves)))
                possibleMoves &= possibleMoves - 1
            pieces &= pieces - 1

    # Check all legal moves for their score using Minimax, and return the best score
    #def minimax():
        #bestMove = -1  # bestMove is the index on the board that is the best move to make.
        #bestScore = -math.inf  # bestScore is the score of the best move found so far
        # Go over all possible moves and evaluate them using minimax
        #for moves:  # Iterate through moves
        #    if move is available:  # If the move is available, then check its value
        #        newMove = bitboard of new move
        #        score = value(newMove)
        #        if score > bestScore:
        #            bestScore = score
        #            bestMove = move
        #return bestMove


    # Return the score if the game is over, or returns either the min/max move based on which player went last
    #def value():
        # If a player is in checkmate, return the score.
        #if checkWin()
        #    return win state
        # Recursively use minimax.
        #elif aiWentLast:
        #    return min()
        #elif not aiWentLast:
        #    return max()


    # Calculates the min continuation of the game using Minimax
    #def min():
    #    best = math.inf  # best is the best score found so far
    #    for moves:  # Iterate through moves
    #        if move is available:  # If the move is available, then check its value
    #            newMove = bitboard of new move
    #            score = value(newMove)
    #            best = max(best, score)
    #    return best


    # Calculates the max continuation of the game using Minimax
    #def max():
    #    best = -math.inf  # best is the best score found so far
    #    for moves:  # Iterate through moves
    #        if move is available:  # If the move is available, then check its value
    #            newMove = bitboard of new move
    #            score = value(newMove)
    #            best = max(best, score)
    #    return best

ai = AI()

def func(x):
    return "%.7f" % x

pstats.f8 = func
cProfile.run("ai.evaluate(12, 28, False)")

cProfile.run("ai.getMoves()")


'''ai.boardObj.printBitboard(0x007E010101010100)
print("      *")
ai.boardObj.printBitboard(0x48FFFE99FECFAA00)
print("      =")
num = 0x007E010101010100*0x48FFFE99FECFAA00
print(num >> 54)
ai.boardObj.printBitboard((num >> 54))'''

