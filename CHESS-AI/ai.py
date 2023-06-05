import chessboard as cb
import random
import cProfile
import pstats
import timeit
import time
class AI:

    def __init__(self):

        self.boardObj = cb.Board()
        self.boardObj.board2Bitboard()
        self.isBlack = True


    def evaluate(self, isBlack):
        king = self.boardObj.bitboard2Index(self.boardObj.bitboards['k']) if isBlack else self.boardObj.bitboard2Index(self.boardObj.bitboards['K'])
        if self.boardObj.check(king, isBlack) == -1:
            return 1000
        
        selfMaterial, enemyMaterial, selfMobility, enemyMobility = 0, 0, 0, 0

        if isBlack:
            selfMaterial, enemyMaterial, selfMobility, enemyMobility = self.countMaterial()
        else:
            enemyMaterial, selfMaterial, enemyMobility, selfMobility = self.countMaterial()

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
    

    def getMoves(self, isBlack):
        moves = []
        pieces = self.boardObj.bitboards['black'] if isBlack else self.boardObj.bitboards['white']
        while pieces > 0:
            index = self.boardObj.bitboard2Index(pieces)
            possibleMoves = self.boardObj.legalMoves(index)
            while possibleMoves > 0:
                moves.append((index, self.boardObj.bitboard2Index(possibleMoves)))
                possibleMoves &= possibleMoves - 1
            pieces &= pieces - 1
        return moves

    # Check all legal moves for their score and return the best move and score
    def minimax(self, depth, aiTurn = True):
        bestMove = -1
        color = aiTurn and self.isBlack
        moves = self.getMoves(color)
        if depth == 0:
            return (None, self.evaluate(color))
        if aiTurn:
            print('aiTurn')
            bestScore = -float('inf')
            for move in moves:

                boardCopy = self.boardObj.board.copy()
                bitboardsCopy = self.boardObj.bitboards.copy()
                self.boardObj.makeMove(move[0], move[1])

                score = self.minimax(depth - 1, not aiTurn)
                if score[1] > bestScore:
                    bestScore = score[1]
                    bestMove = move
                elif score[1] == bestScore:
                    bestMove = random.choice((bestMove, move))

                self.boardObj.board = boardCopy
                self.boardObj.bitboards = bitboardsCopy
        else:
            print("not")

            bestScore = float('inf')
            for move in moves:  # Iterate through moves# If the move is available, then check its value
                # newMove = bitboard of new move

                boardCopy = self.boardObj.board.copy()
                bitboardsCopy = self.boardObj.bitboards.copy()
                self.boardObj.makeMove(move[0], move[1])

                score = self.minimax(depth - 1, not aiTurn)
                if score[1] < bestScore:
                    bestScore = score[1]
                    bestMove = move
                elif score[1] == bestScore:
                    bestMove = random.choice((bestMove, move))

                self.boardObj.board = boardCopy
                self.boardObj.bitboards = bitboardsCopy
        return (bestMove, bestScore)

ai = AI()

def func(x):
    return "%.7f" % x

pstats.f8 = func
#cProfile.run("ai.evaluate(12, 28, False)")

#cProfile.run("ai.getMoves()")

