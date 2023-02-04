import chessboard as cb
import os
import pygame


pygame.init()

WIDTH, HEIGHT = 1024, 1024
FPS = 60
BK_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'bK.png'))
BQ_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'bQ.png'))
BB_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'bB.png'))
BN_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'bN.png'))
BR_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'bR.png'))
BP_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'bP.png'))
WK_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'wK.png'))
WQ_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'wQ.png'))
WB_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'wB.png'))
WN_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'wN.png'))
WR_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'wR.png'))
WP_IMAGE = pygame.image.load(os.path.join('CHESS-AI\Assets', 'wP.png'))

bitkey_image = {
    'k': BK_IMAGE,
    'q': BQ_IMAGE,
    'b': BB_IMAGE,
    'n': BN_IMAGE,
    'r': BR_IMAGE,
    'p': BP_IMAGE,
    'K': WK_IMAGE,
    'Q': WQ_IMAGE,
    'B': WB_IMAGE,
    'N': WN_IMAGE,
    'R': WR_IMAGE,
    'P': WP_IMAGE
}


STARTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
board = [0 for i in range(64)]
DARK_TILE = (89, 81, 4)
LIGHT_TILE = (235, 225, 138)


def draw_background():
    for col in range(8):
        for row in range(8):
            sqColor = LIGHT_TILE
            if (col + row) % 2 != 0:
                sqColor = DARK_TILE
            x = (WIDTH/8) * col
            y = (HEIGHT/8) * row
            tile = pygame.Rect(x, y, WIDTH/8, HEIGHT/8)
            pygame.draw.rect(window, sqColor, tile)
    pygame.display.update()

# draws the pieces by each bitboard onto the chessboard


def drawBoard(board: cb.Board):
    draw_background()
    for key in board.bitboards.keys():
        bit = format(board.bitboards[key], "064b")
        pos = 0
        for sq in bit:
            if sq == '1':
                x = pos % 8
                y = int(pos/8)
                window.blit(bitkey_image[key], (x*WIDTH/8, y*HEIGHT/8))
            pos += 1
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    running = True
    draw_background()
    brd = cb.Board()
    brd.board2Bitboard()
    drawBoard(brd)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
