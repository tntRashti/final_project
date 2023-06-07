import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()

pygame.init()
#screen resulution
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter")


clock = pygame.time.Clock()
FPS = 165
#colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
#The warrior 
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
#The wizard
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET= [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load muzic and sounds
pygame.mixer.music.load("modern-war-129016.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1, 0.0, 5000)

#The warrior attack sound
sword_fx = pygame.mixer.Sound("sword.wav")
sword_fx.set_volume(0.45)
#The wizard attack sound
magic_fx = pygame.mixer.Sound("magic.wav")
magic_fx.set_volume(0.75)




#Backgrouns 
bg_image = pygame.image.load("backround.jpg")
""" this part inculeded all the images of the charakters in the game"""
warrior_sheet = pygame.image.load("warrior.png")
wizard_sheet = pygame.image.load("wizard.png")

victory_img = pygame.image.load("victory.png")



WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]



count_font = pygame.font.Font("turok (1).ttf", 160)
score_font = pygame.font.Font("turok (1).ttf", 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



def draw_bg():
    screen.blit(bg_image, (0, 0))



def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x  - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#the players
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#main
"""everything that incluse the game """
run = True
while run:
    
    clock.tick(FPS)

    draw_bg()

    #SHOW player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)


#Timer to start the round or the game
    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            



    


    fighter_1.update()
    fighter_2.update()


    fighter_1.draw(screen)
    fighter_2.draw(screen)

#this part show us what append when round over and someone win the round
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        
    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#when we close the game the game will close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 


    pygame.display.update()






pygame.quit()
