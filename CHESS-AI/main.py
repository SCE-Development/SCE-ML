import chessboard as cb

play = True
color = True                # True = White | False = Black
validMove = False
move, start, end = "", "", ""

brd = cb.Board()
brd.board2Bitboard()
brd.printBoard()
print()
while play:
    move = ""
    if color:
        print("Turn for White")
        while not validMove:
            move = input()
            # Valid move inputs look like "b2b3" where the first two characters of the string of length 4
            # specify the starting square and the last two characters specify the ending square.
            if len(move) < 4 or len(move) > 4 or move[0:2] not in brd.fileRank2index or move[2:4] not in brd.fileRank2index or brd.board[brd.fileRank2index[move[0:2]]].islower():
                print("PLEASE ENTER A VALID MOVE")
            else:
                start, end = brd.fileRank2index[move[0:2]], brd.fileRank2index[move[2:4]]
                if brd.makeMove(start, end):
                    validMove = True
        brd.printBoard()
        color = False
        validMove = False
    else:
        print("Turn for Black")
        while not validMove:
            move = input()
            # Valid move inputs look like "b2b3" where the first two characters of the string of length 4
            # specify the starting square and the last two characters specify the ending square.
            if len(move) < 4 or len(move) > 4 or move[0:2] not in brd.fileRank2index or move[2:4] not in brd.fileRank2index or brd.board[brd.fileRank2index[move[0:2]]].isupper():
                print("PLEASE ENTER A VALID MOVE")
            else:
                start, end = brd.fileRank2index[move[0:2]], brd.fileRank2index[move[2:4]]
                validMove = brd.makeMove(start, end)
        brd.printBoard()
        color = True
        validMove = False