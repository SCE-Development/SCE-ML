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
