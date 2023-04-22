import pygame
import chessboard as cb
import math


class GUI:
    def __init__(self, whitePOV):
        self.BOARDSIZE = 512
        self.SCREENWIDTH, self.SCREENHEIGHT = self.BOARDSIZE, int(
            self.BOARDSIZE * 1.125)
        self.TILESIZE = self.SCREENWIDTH >> 3
        pygame.init()
        self.WIN = pygame.display.set_mode(
            (self.SCREENWIDTH, self.SCREENHEIGHT))
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

        self.whitePOV = whitePOV
        self.boardObj = cb.Board()
        self.boardObj.board2Bitboard()
        self.selected = None
        self.legalMoves = []
        self.whitesTurn = True

    def main(self):
        run = True
        self.makeCoordMap()
        self.updateScreen()
        self.renderGameInfo()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # exit button on top right
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    index = self.mousePosToIndex(pos)
                    if index is None:
                        self.updateScreen()
                        self.selected = None
                        self.legalMoves = None
                        continue
                    if self.isMakingMove(index):
                        self.makeMove(self.selected, index)
                        self.whitesTurn = not self.whitesTurn
                        self.renderGameInfo()
                    else:
                        self.selectTile(index)

    # given char representation, return a scaled image of the piece (e.g. b -> white bishop PNG)
    def pieceToImg(self, piece):
        return pygame.transform.scale(pygame.image.load(f"./Assets/pieces/{piece}.png"), (self.TILESIZE, self.TILESIZE))

    # def renderTest(self):  # test board to print the starting condition of the board
    #     testBoard = [
    #         "R", "N", "B", "K", "Q", "B", "N", "R",
    #         "P", "P", "P", "P", "P", "P", "P", "P",
    #         ".", ".", ".", ".", ".", ".", ".", ".",
    #         ".", ".", ".", ".", ".", ".", ".", ".",
    #         ".", ".", ".", ".", ".", ".", ".", ".",
    #         ".", ".", ".", ".", ".", ".", ".", ".",
    #         "p", "p", "p", "p", "p", "p", "p", "p",
    #         "r", "n", "b", "k", "q", "b", "n", "r"
    #     ]
    #     self.renderPieces(testBoard)

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
        # put in list to easily alternate with modulo
        colors = [LIGHTCOLOR, DARKCOLOR]
        for col in range(8):
            for row in range(8):
                tile = pygame.Rect(row * self.TILESIZE, col *
                                   self.TILESIZE, self.TILESIZE, self.TILESIZE)
                if self.whitePOV:
                    color = colors[(col + row) % 2]
                else:
                    color = colors[1 - ((col + row) % 2)]
                pygame.draw.rect(self.WIN, color, tile)
        pygame.display.update()

    def renderGameInfo(self):
        kingIndex = self.boardObj.bitboards["K"] if self.whitesTurn else self.boardObj.bitboards["k"]
        kingIndex = int(math.log2(kingIndex))
        checkmate = self.boardObj.check(kingIndex, not self.whitesTurn)
        y = self.BOARDSIZE
        infoBackground = pygame.Rect(0, y, self.BOARDSIZE, self.TILESIZE)
        pygame.draw.rect(self.WIN, (200, 200, 200), infoBackground)
        font = pygame.font.Font(pygame.font.get_default_font(), 25)
        if checkmate == -1:
            text = font.render("Checkmate", True, (0, 0, 0))
        else:
            turn = "White" if self.whitesTurn else "Black"
            text = font.render(f"{turn}'s turn", True, (0, 0, 0))
        text_rect = text.get_rect(
            center=(self.SCREENWIDTH / 2, (self.TILESIZE / 2) + self.BOARDSIZE))
        self.WIN.blit(text, text_rect)
        pygame.display.update()
        return True

    def updateScreen(self):
        self.checkerPattern()
        self.renderPieces()

    def isMakingMove(self, index):
        if self.selected is None:
            return False
        piece = self.boardObj.board[self.selected]
        # print(piece)
        if piece == ".":
            return False
        if (ord(piece) < 97) != self.whitesTurn:  # checks if piece is white and is white's turn
            return False
        return index in self.legalMoves

    def makeMove(self, start, dest):
        self.boardObj.makeMove(start, dest)
        self.updateScreen()
        pygame.display.update()

    def selectTile(self, index):
        DARKSELECT = (100, 111, 64)
        LIGHTSELECT = (130, 151, 105)
        self.updateScreen()
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
        self.legalMoves = self.bitBoardToIndexes(
            self.boardObj.legalMoves(index))
        self.selected = index

        for l in self.legalMoves:
            radius = self.TILESIZE // 6
            circleX, circleY = self.coords[l]
            circleX += (self.TILESIZE // 2)
            circleY += (self.TILESIZE // 2)
            pygame.draw.circle(self.WIN, DARKSELECT,
                               (circleX, circleY), radius)

        pygame.display.update()

    def mousePosToIndex(self, mousePos):
        if mousePos[0] > self.BOARDSIZE or mousePos[1] > self.BOARDSIZE:
            return None
        col = mousePos[0] // self.TILESIZE
        if self.whitePOV:
            row = 7 - mousePos[1] // self.TILESIZE
        else:
            row = mousePos[1] // self.TILESIZE
        return col + (8 * row)

    def bitBoardToIndexes(self, bitboard):
        ind = 1
        moves = []
        for i in range(64):
            if (ind << i) & bitboard:
                moves.append(i)
        return moves

    def indexToRankFile(self, index):
        return ("ABCDEFGH")[index % 8] + str((index // 8) + 1)


if __name__ == "__main__":
    playing = "?"
    while playing not in ("b", "w", "black", "white"):
        playing = input("Playing as Black or White? (B/W): ").lower()
    whitePOV = True
    if playing in ("black", "b"):
        whitePOV = False

    gui = GUI(whitePOV)
    gui.main()
