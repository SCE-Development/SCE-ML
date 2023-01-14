import pygame

pygame.init()

WIDTH, HEIGHT = 1024, 1024

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        

