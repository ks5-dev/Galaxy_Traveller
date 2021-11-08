import pygame, sys ,model5
from handle_score import receive_score

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((800, 600),0,32)
 
font = pygame.font.Font("futura.ttf", 64)
font2 = pygame.font.Font("futura.ttf", 32) 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False
 
def main_menu():
    while True:
        screen.fill((30, 30, 30))
        draw_text('Welcome to Arena Shooter', font, (255, 255, 255), screen, 100, 100)
        received = receive_score()
        draw_text('highest score : '+received[0]+" last game : "+received[1], font2, (255, 255, 255), screen, 175, 225)
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(275, 300, 250, 100)
        draw_text('Play', font2, (255, 255, 255), screen, 300, 325)
        if button_1.collidepoint((mx, my)):
            if click:
                new_game()

        pygame.draw.rect(screen, (63, 112, 77), button_1)
        click = False        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        draw_text('Play', font2, (255, 255, 255), screen, 365, 325)
        pygame.display.update()
        mainClock.tick(60)
 
def new_game():
    model5.game()

main_menu()