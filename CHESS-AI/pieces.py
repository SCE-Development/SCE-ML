

class Piece:

    # Piece initializes with a variable to store the piece's position
    # and a tuple that determines all possible moves the piece can make
    def __init__(self, position, moves):
        
        self.position = position
        self.moves = moves

    def getValidMoves(self):

        # CODE TO BE IMPLEMENTED
        asdf


class Pawn(Piece):

    def __init__(self, position):
        moves = (8)
        super().__init__(self, position, moves)

class Bishop(Piece):

    def __init__(self, position):
        moves = (8)
        super().__init__(self, position, moves)

class Knight(Piece):

    def __init__(self, position):
        moves = (8)
        super().__init__(self, position, moves)

class Rook(Piece):

    def __init__(self, position):
        moves = (8)
        super().__init__(self, position, moves)

class Queen(Piece):

    def __init__(self, position):
        moves = (8)
        super().__init__(self, position, moves)

class King(Piece):

    def __init__(self, position):
        moves = (8)
        super().__init__(self, position, moves)
