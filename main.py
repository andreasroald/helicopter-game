# Cavecopter by Coregame
# https://github.com/coregameHD/Cavecopter
# Forked from andreasroald/helicopter-game
import pygame, random
from pygame.locals import *
import helicopter, enemy_heli, sprites

# pygame __init__
pygame.init()

# game display settings
pygame.display.set_icon(sprites.icon)
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

# fonts
TITLEFONT = 'fonts/2015_DuangDao.ttf'
MAINFONT = 'fonts/rd_chulajaruek.ttf'
MENUFONT = 'fonts/Sansation_Regular.ttf'
ALERTFONT = 'fonts/8-Bit-Madness.ttf'

# text rendering function (** Thanks : andreasroald **)
def message_to_screen(message, textfont, size, color):
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)
    
    return my_message

# colors setting
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
YELLOW     = (255, 255,   0)
RED        = (255,   0,   0)
GRAY       = ( 50,  50,  50)

# framerate variables
FPSCLOCK = pygame.time.Clock()
FPS = 30

# background variables
background_width = 1920

# red_heart variables
red_heart_x = 800
red_heart_y = random.randint(0, 400)

# main menu helicopter (for decoration only)
heli_main_x = 800
heli_main_y = random.randint(0, 400)

# player variables
player = helicopter.Helicopter(100, HALF_WINHEIGHT-40)
moving = True

# score variables
score = 0
hard_mode = 1800
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read()) #high score in integer

# enemy helicopter variables
enemy_heli = enemy_heli.EnemyHeli(-100, HALF_WINHEIGHT-40)
enemy_heli_alive = False

# missile variables
missile_x = 800
missile_y = player.y
missile_alive = False
missile_hit_player = False
warning_once = True
warning = False
warning_counter = 0
warning_message = message_to_screen("!", ALERTFONT, 200, RED)

# sounds
alert = pygame.mixer.Sound('sounds/alert.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')
heal = pygame.mixer.Sound('sounds/heal.wav')
select = pygame.mixer.Sound('sounds/select.wav')
whoosh = pygame.mixer.Sound('sounds/whoosh.wav')

# main menu
def main_menu():
    global heli_main_x
    global heli_main_y

    # choice
    '''
    1. PLAY
    2. QUIT
    '''
    menu = True
    selected = "play"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = "play"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = "quit"
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select)
                    if selected == "play":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()
                        
        # main menu background
        DISPLAYSURF.blit(sprites.mainmenu_background, (0, 0))

        # random helicopter (for decoration only)
        DISPLAYSURF.blit(sprites.mainmenu_helicopter, (heli_main_x, heli_main_y))
        if heli_main_x <= 800 - 1000:
            heli_main_x = 800
            heli_main_y = random.randint(0, 500)
        else:
            heli_main_x -= 10

        # message
        title = message_to_screen("CAVECOPTER", TITLEFONT, 66, YELLOW)
        controls_1 = message_to_screen("Click and hold left mouse to go up.", MAINFONT, 20, WHITE)
        controls_2 = message_to_screen("Release to go down. Avoid hitting spikes or obstacles.", MAINFONT, 20, WHITE)
        controls_3 = message_to_screen("Collect red heart for +1 Life", MAINFONT, 20, WHITE)
        credit = message_to_screen("https://github.com/coregameHD/Cavecopter", MAINFONT, 16, WHITE)
        if selected == "play":
            play = message_to_screen("PLAY", MENUFONT, 36, WHITE)
        else:
            play = message_to_screen("PLAY", MENUFONT, 36, BLACK)
        if selected == "quit":
            game_quit = message_to_screen("QUIT", MENUFONT, 36, WHITE)
        else:
            game_quit = message_to_screen("QUIT", MENUFONT, 36, BLACK)

        title_rect = title.get_rect()
        controls_1_rect = controls_1.get_rect()
        controls_2_rect = controls_2.get_rect()
        controls_3_rect = controls_3.get_rect()
        play_rect = play.get_rect()
        quit_rect = game_quit.get_rect()
        credit_rect = credit.get_rect()

        # drawing text
        DISPLAYSURF.blit(title, (HALF_WINWIDTH - (title_rect[2]/2), 0))
        DISPLAYSURF.blit(controls_1, (HALF_WINWIDTH - (controls_1_rect[2]/2), 170))
        DISPLAYSURF.blit(controls_2, (HALF_WINWIDTH - (controls_2_rect[2]/2), 195))
        DISPLAYSURF.blit(controls_3, (HALF_WINWIDTH - (controls_3_rect[2]/2), 220))
        DISPLAYSURF.blit(play, (HALF_WINWIDTH - (play_rect[2]/2), 300))
        DISPLAYSURF.blit(game_quit, (HALF_WINWIDTH - (quit_rect[2]/2), 360))
        DISPLAYSURF.blit(credit, (HALF_WINWIDTH - (credit_rect[2]/2), 570))

        #pygame.mixer.Sound.play(intro_sound)
        pygame.display.update()
        pygame.display.set_caption("Cavecopter (" + str(int(FPSCLOCK.get_fps())) + " FPS)")
        FPSCLOCK.tick(FPS)

# main game
def game_loop():
    global background_width

    global missile_x
    global missile_y
    global missile_alive
    global missile_hit_player
    global warning
    global warning_counter
    global warning_once

    global bullets
    global moving

    global red_heart_x
    global red_heart_y

    global highscore_file
    global highscore_int
    global score
    global hard_mode

    global cloud_x
    global cloud_y

    global enemy_heli_alive

    game_exit = False
    game_over = False
    game_over_selected = "play again"

    while not game_exit:
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > highscore_int:
                        highscore_file = open('highscore.dat', "w")
                        highscore_file.write(str(score))
                        highscore_file.close()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "play again"
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(select)
                        game_over_selected = "quit"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(select)
                        if game_over_selected == "play again":
                            player.moving_up = False
                            player.moving_down = False
                            if score > highscore_int:
                                highscore_file = open('highscore.dat', "w")
                                highscore_file.write(str(score))
                                highscore_file.close()
                            game_over = False

                            score = 0

                            red_heart_x = 800

                            enemy_heli.x = -100
                            enemy_heli_alive = False
                            enemy_heli.bullets = []

                            missile_x = 800
                            missile_alive = False
                            warning = False
                            warning_counter = 0
                            warning_counter = 0

                            player.wreck_start = False
                            player.y = HALF_WINWIDTH - 40
                            player.x = 100
                            player.wrecked = False
                            player.health = 3
                            bullets = []

                            game_loop()
                            
                        if game_over_selected == "quit":
                            pygame.quit()
                            quit()
                            
            # game over screen
            game_over_text = message_to_screen("GAME OVER", MAINFONT, 72, BLACK)
            game_over_caption = message_to_screen("TRY AGAIN?", MAINFONT, 36, BLACK)
            if game_over_selected == "play again":
                play_again = message_to_screen("YES, PLAY AGAIN", MENUFONT, 36, WHITE)
            else:
                play_again = message_to_screen("YES, PLAY AGAIN", MENUFONT, 36, BLACK)
            if game_over_selected == "quit":
                game_quit = message_to_screen("NO, QUIT", MENUFONT, 36, WHITE)
            else:
                game_quit = message_to_screen("NO, QUIT", MENUFONT, 36, BLACK)

            game_over_rect = game_over_text.get_rect()
            caption_rect = game_over_caption.get_rect()
            play_again_rect = play_again.get_rect()
            game_quit_rect = game_quit.get_rect()

            DISPLAYSURF.blit(game_over_text, (HALF_WINWIDTH - game_over_rect[2]/2, 80))
            DISPLAYSURF.blit(game_over_caption, (HALF_WINWIDTH - (caption_rect[2]/2+5), 160))
            DISPLAYSURF.blit(play_again, (HALF_WINWIDTH - play_again_rect[2]/2, 260))
            DISPLAYSURF.blit(game_quit, (HALF_WINWIDTH - game_quit_rect[2]/2, 320))

            pygame.display.update()
            pygame.display.set_caption("Cavecopter (" + str(int(FPSCLOCK.get_fps())) + " FPS)")
            FPSCLOCK.tick(10)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > highscore_int:
                    highscore_file = open('highscore.dat', "w")
                    highscore_file.write(str(score))
                    highscore_file.close()
                pygame.quit()
                quit()
                
            # player move
            '''
            1. click and hold left mouse to go up
            2. release to go down
            '''
            left_click = 1
            if moving:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == left_click:
                        player.moving_up = True
                    player.moving_down = False
                if event.type == pygame.MOUSEBUTTONUP:
                    player.moving_up = False
                    player.moving_down = True

        if player.health < 1:
            pygame.mixer.Sound.play(explosion)
            player.wreck()

        if player.wrecked:
            game_over = True
        
        # scrolling background
        DISPLAYSURF.blit(sprites.bg1, (background_width, 0))
        DISPLAYSURF.blit(sprites.bg2, (background_width - 1920, 0))
        if score > hard_mode:
            background_width -= 6
        elif score < hard_mode:
            background_width -= 2
            
        if background_width <= 0:
            background_width = 1920

        # drawing player
        DISPLAYSURF.blit(player.current, (player.x, player.y))

        # drawing enemy helicopter
        DISPLAYSURF.blit(enemy_heli.current, (enemy_heli.x, enemy_heli.y))

        # drawing missile
        DISPLAYSURF.blit(sprites.missile, (missile_x, missile_y))

        # enabling movement and animations
        player.player_init()
        enemy_heli.init()

        # rendering enemy bullets
        if not player.wreck_start and not player.wrecked and not game_over:
            for draw_bullet in enemy_heli.bullets:
                pygame.draw.rect(DISPLAYSURF, GRAY, (draw_bullet[0], draw_bullet[1]+40, 40, 10))
                pygame.draw.rect(DISPLAYSURF, RED, (draw_bullet[0]+30, draw_bullet[1]+40, 10, 10))
            for move_bullet in range(len(enemy_heli.bullets)):
                enemy_heli.bullets[move_bullet][0] -= 15
            for del_bullet in enemy_heli.bullets:
                if del_bullet[0] <= -40:
                    enemy_heli.bullets.remove(del_bullet)

        # spawn red heart randomly
        DISPLAYSURF.blit(sprites.red_heart, (red_heart_x, red_heart_y))
        magicnumber = random.randint(1, 1000)
        if player.health < 3:
            if magicnumber == 500: # 0.1% rate
                red_heart_x = 800
                red_heart_y = random.randint(0, 400)
            else:
                if not player.wreck_start:
                    red_heart_x -= 9
        elif player.health < 2:
            if magicnumber in range(490, 500): # 1% rate
                red_heart_x = 800
                red_heart_y = random.randint(0, 400)
            else:
                if not player.wreck_start:
                    red_heart_x -= 9

        # spawn missile randomly
        missile_spawn_num = random.randint(0, 100)
        if score > hard_mode:
            if not missile_alive: #continuous missile
                warning = True
        else:
            if missile_spawn_num == 50 and not missile_alive and score > 150:
                warning = True
                
        # show warning before missile spawning
        if warning:
            if warning_once:
                pygame.mixer.Sound.play(alert)
                warning_once = False
            DISPLAYSURF.blit(warning_message, (750, missile_y-15))
            if warning_counter > 45:
                pygame.mixer.Sound.play(whoosh)
                missile_alive = True
                warning_counter = 0
                warning = False
                warning_once = True
            else:
                warning_counter += 1

        # missile movement
        hardmode_missile_speed = random.randint(30, 60)
        if missile_alive:
            if score > hard_mode:
                missile_x -= hardmode_missile_speed
            else:
                missile_x -= 30 
        if missile_x < 0-100:
            missile_hit_player = False
            missile_alive = False
            missile_x = 800
            missile_y = player.y

        # spawn enemy helicopter randomly
        enemy_spawn_num = random.randint(0, 100)
        if not enemy_heli_alive and score > 650 and enemy_spawn_num == 50:
            enemy_heli_alive = True
            enemy_heli.x = 800
            enemy_heli.y = player.y
            counter = score
        if enemy_heli_alive == True:
            if score > hard_mode:
                if score > counter + 550:
                    enemy_heli.x = -100
                    enemy_heli_alive = False
                else:
                    enemy_heli.y = player.y
            else:
                if score > counter + 300:
                    enemy_heli.x = -100
                    enemy_heli_alive = False
                else:
                    enemy_heli.y = player.y

        # player-heart collision detection
        if red_heart_x < player.x < red_heart_x+70 or red_heart_x < player.x+100 < red_heart_x+70:
            if red_heart_y < player.y < red_heart_y+80 or red_heart_y < player.y+80 < red_heart_y+80:
                pygame.mixer.Sound.play(heal)
                if player.health < 3:
                    player.health += 1
                red_heart_x = 800-870
                
        # player-enemy helicopter collision detection
        for hit_player in enemy_heli.bullets:
            if player.x < hit_player[0] < player.x+100 or player.x < hit_player[0]+40 < player.x+100:
                if player.y < hit_player[1]+40 < player.y+80 or player.y < hit_player[1]+50 < player.y+80:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    enemy_heli.bullets.remove(hit_player)

        # player-missile collision detection
        if missile_x < player.x < missile_x+100 or missile_x < player.x+100 < missile_x+100:
            if missile_y < player.y < missile_y+88 or missile_y < player.y+80 < missile_y+88:
                if not missile_hit_player:
                    pygame.mixer.Sound.play(explosion)
                    player.damaged = True
                    player.health -= 1
                    missile_hit_player = True

        # draw score
        if score > hard_mode:
            DISPLAYSURF.blit(message_to_screen("SCORE: {0}".format(score), MAINFONT, 36, RED), (800-240, 0))
            hard_mode_message = message_to_screen("<HARD MODE>", MAINFONT, 36, RED)
            DISPLAYSURF.blit(hard_mode_message, (240, 0))
        else:
            DISPLAYSURF.blit(message_to_screen("SCORE: {0}".format(score), MAINFONT, 36, BLACK), (800-240, 0))

        # draw high score
        if score < highscore_int:
            hi_score_message = message_to_screen("HIGH SCORE: {0}".format(highscore_int), MAINFONT, 22, BLACK)
        else:
            highscore_file = open('highscore.dat', "w")
            highscore_file.write(str(score))
            highscore_file.close()
            highscore_file = open('highscore.dat', "r")
            highscore_int = int(highscore_file.read())
            highscore_file.close()
            hi_score_message = message_to_screen("HI-SCORE: {0}".format(highscore_int), MAINFONT, 22, RED)

        hi_score_message_rect = hi_score_message.get_rect()

        DISPLAYSURF.blit(hi_score_message, (800-220, 50))

        # draw health (maximum = 3)
        if player.health >= 1:
            DISPLAYSURF.blit(sprites.icon, (10 , 10))
            if player.health >= 2:
                DISPLAYSURF.blit(sprites.icon, (52, 10))
                if player.health >= 3:
                    DISPLAYSURF.blit(sprites.icon, (94, 10))
                    
        # draw spikes at the buttom of the screen
        DISPLAYSURF.blit(sprites.spikes, (0, 500))

        # score increase every second
        if score > hard_mode:
            score += 2 #default = 2
        else:
            score += 1 #default = 1

        # pygame systems
        pygame.display.update()
        pygame.display.flip() #smooth scrolling background
        pygame.display.set_caption("Cavecopter (" + str(int(FPSCLOCK.get_fps())) + " FPS)")
        FPSCLOCK.tick(FPS)

# game flows
pygame.mixer.music.load('sounds/tetrisc.mid')#bgm
pygame.mixer.music.play(-1, 0.0)#bgm
main_menu()
pygame.mixer.music.stop()#bgm
pygame.mixer.music.load('sounds/bgm.mp3')#bgm
pygame.mixer.music.play(-1, 0.0)#bgm
game_loop()
pygame.mixer.music.stop()#bgm
pygame.quit()
quit()
