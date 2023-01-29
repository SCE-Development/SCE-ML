

class Piece:

    # Piece initializes with a variable to store the piece's position
    # and a tuple that determines all possible moves the piece can make
    def __init__(self, position, moves):
        
        self.position = position
        self.moves = moves