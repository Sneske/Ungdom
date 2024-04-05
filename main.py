import pygame 




Width = 800
Height = 420

win = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 16)



while running: 
    all_sprites.draw(win)
    pygame.display.flip()

pygame.quit()