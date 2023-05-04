import chessboard as cb

class AI:

    def __init__(self):

        self.boardObj = cb.Board()
        self.boardObj.board2Bitboard()
        self.legalMoves = []


    def evaluate(self, start, end, isBlack):
        boardCopy = self.boardObj.board.copy()
        bitboardsCopy = self.boardObj.bitboards.copy()
        self.boardObj.makeMove(start, end)
        
        ai.boardObj.printBoard()
        selfMaterial, enemyMaterial, selfMobility, enemyMobility = 0, 0, 0, 0

        if isBlack:
            selfMaterial, enemyMaterial = self.countMaterial()
            print('black')
        else:
            enemyMaterial, selfMaterial = self.countMaterial()
            print("white")
        
        print(selfMaterial, enemyMaterial)
        

        self.boardObj.board = boardCopy
        self.boardObj.bitboards = bitboardsCopy
        return
    
    
    def countMaterial(self):
        black, white = 0, 0
        for type in ('p', 'n', 'b', 'r', 'q', 'k'):
            pieces = self.boardObj.bitboards[type]
            while pieces > 0:
                if type == 'p':
                    black += 1
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'n':
                    black += 3
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'b':
                    black += 3
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'r':
                    black += 5
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'q':
                    black += 9
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                else:
                    black += 200
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
        for type in ('P', 'N', 'B', 'R', 'Q', 'K'):
            pieces = self.boardObj.bitboards[type]
            while pieces > 0:
                if type == 'P':
                    white += 1
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'N':
                    white += 3
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'B':
                    white += 3
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'R':
                    white += 5
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                elif type == 'Q':
                    white += 9
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
                else:
                    white += 200
                    pieces ^= 0b1 << self.boardObj.bitboard2Index(pieces)
        return black, white
    

    def getMoves(self):
        pieces = self.boardObj.bitboards['white'] | self.boardObj.bitboards['black']
        while pieces > 0:
            index = self.boardObj.bitboard2Index(pieces)
            possibleMoves = self.boardObj.legalMoves(index)
            while possibleMoves > 0:
                move = self.boardObj.bitboard2Index(possibleMoves)
                self.legalMoves.append((index, move))
                possibleMoves ^= 0b1 << move
            pieces ^= 0b1 << index

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
ai.evaluate(1, 16, False)
ai.boardObj.printBoard()
