import pygame

class GUI:
    def __init__(self):
        self.SCREENWIDTH, self.SCREENHEIGHT = 1024, 1024
        pygame.init()
        self.WIN = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        pygame.display.set_caption("SCE Chess Bot")
        self.pieceImages = {
            "R": self.pieceToImg("wR"),
            "N": self.pieceToImg("wN"),
            "B": self.pieceToImg("wB"),
            "K": self.pieceToImg("wK"),
            "Q": self.pieceToImg("wQ"),
            "P": self.pieceToImg("wP"),
            "r": self.pieceToImg("bR"),
            "n": self.pieceToImg("bN"),
            "b": self.pieceToImg("bB"),
            "k": self.pieceToImg("bK"),
            "q": self.pieceToImg("bQ"),
            "p": self.pieceToImg("bP")
        }




    def main(self):
        clock = pygame.time.Clock()
        run = True
        self.checkerPattern()                   # creates checkerboard pattern for board
        self.renderTest()                       # not permanent, just here to test display
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # exit button on top right
                    run = False

    def pieceToImg(self, piece):    # given char representation, return a scaled image of the piece (e.g. b -> white bishop PNG)
        return pygame.transform.scale(pygame.image.load(f"./Assets/{piece}.png"), (self.SCREENHEIGHT >> 3, self.SCREENHEIGHT >> 3))

    def renderTest(self):                               # test board to print the starting condition of the board
        testBoard = [
            "R", "N", "B", "K", "Q", "B", "N", "R",
            "P", "P", "P", "P", "P", "P", "P", "P",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            ".", ".", ".", ".", ".", ".", ".", ".",
            "p", "p", "p", "p", "p", "p", "p", "p",
            "r", "n", "b", "k", "q", "b", "n", "r"
        ]
        self.renderPieces(testBoard)

    def renderPieces(self, boardList):                  # goes through 1D board array and renders pieces found
        TILESIZE = min(self.SCREENWIDTH, self.SCREENHEIGHT) >> 3
        for i, piece in enumerate(boardList):
            if piece == ".":                            # "." denotes an empty square
                continue
            x = (i % 8) * TILESIZE
            y = (7 - (i >> 3)) * TILESIZE
            if piece not in self.pieceImages:           # should never happen unless there's a bug in the board's code
                print("board invalid")
                return
            self.WIN.blit(self.pieceImages[piece], (x, y))
        pygame.display.update()


    def checkerPattern(self):
        TILESIZE = min(self.SCREENWIDTH, self.SCREENHEIGHT) >> 3
        LIGHTCOLOR = (240, 217, 181)                    # color of light square
        DARKCOLOR = (181, 136, 99)                      # color of dark square
        colors = [LIGHTCOLOR, DARKCOLOR]                # put in list to easily alternate with modulo
        for col in range(8):
            for row in range(8):
                tile = pygame.Rect(row * TILESIZE, col * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(self.WIN, colors[(col + row) % 2], tile)
        pygame.display.update()


if __name__ == "__main__":
    gui = GUI()
    gui.main()