import pygame
import chessboard as cb


class GUI:
    def __init__(self, whitePOV):
        self.SCREENWIDTH, self.SCREENHEIGHT = 1024,1024
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
        self.TILESIZE = min(self.SCREENWIDTH, self.SCREENHEIGHT) >> 3
        self.whitePOV = whitePOV
        self.boardObj = cb.Board()
        self.boardObj.board2Bitboard()

    def main(self):
        run = True
        self.makeCoordMap()
        self.checkerPattern()  # creates checkerboard pattern for board
        self.renderPieces()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # exit button on top right
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.selectTile(pos)


    def pieceToImg(self, piece):  # given char representation, return a scaled image of the piece (e.g. b -> white bishop PNG)
        return pygame.transform.scale(pygame.image.load(f"./Assets/pieces/{piece}.png"), (self.SCREENHEIGHT >> 3, self.SCREENHEIGHT >> 3))

    def renderTest(self):  # test board to print the starting condition of the board
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

    def makeCoordMap(self):
        self.coords = {}
        for i in range(64):
            x = (i % 8) * self.TILESIZE
            if self.whitePOV:
                y = (7 - (i >> 3)) * self.TILESIZE
            else:
                y = (i >> 3) * self.TILESIZE
            self.coords[i] = (x, y)

    def renderPieces(self):  # goes through 1D board array and renders pieces found
        boardList = self.boardObj.board
        for i, piece in enumerate(boardList):
            if piece == ".":  # "." denotes an empty square
                continue
            (x, y) = self.coords[i]
            if piece not in self.pieceImages:  # should never happen unless there's a bug in the board's code
                print("board invalid")
                return
            self.WIN.blit(self.pieceImages[piece], (x, y))
        pygame.display.update()

    def checkerPattern(self):
        LIGHTCOLOR = (240, 217, 181)  # color of light square
        DARKCOLOR = (181, 136, 99)  # color of dark square
        colors = [LIGHTCOLOR, DARKCOLOR]  # put in list to easily alternate with modulo
        for col in range(8):
            for row in range(8):
                tile = pygame.Rect(row * self.TILESIZE, col * self.TILESIZE, self.TILESIZE, self.TILESIZE)
                if self.whitePOV:
                    color = colors[(col + row) % 2]
                else:
                    color = colors[1 - ((col + row) % 2)]
                pygame.draw.rect(self.WIN, color, tile)
        pygame.display.update()

    def selectTile(self, mousePos):
        DARKSELECT = (100,111,64)
        LIGHTSELECT = (130,151,105)
        self.checkerPattern()
        self.renderPieces()
        col = mousePos[0] // self.TILESIZE
        if self.whitePOV:
            row = 7 - mousePos[1] // self.TILESIZE
        else:
            row = mousePos[1] // self.TILESIZE
        index = col + (8 * row)
        x, y = self.coords[index]
        tile = pygame.Rect(x, y, self.TILESIZE, self.TILESIZE)
        if index % 2:
            color = DARKSELECT
        else:
            color = LIGHTSELECT
        pygame.draw.rect(self.WIN, color, tile)
        piece = self.boardObj.board[index]
        if piece != ".":
            self.WIN.blit(self.pieceImages[piece], (x, y))
        pygame.display.update()



if __name__ == "__main__":
    playing = "?"
    while playing not in ("b", "w", "black", "white"):
        playing = input("Playing as Black or White? (B/W): ").lower()
    whitePOV = True
    if playing in ("black", "b"):
        whitePOV = False

    gui = GUI(whitePOV)
    gui.main()

