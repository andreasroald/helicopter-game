# Cavecopter by Coregame
# https://github.com/coregameHD/Cavecopter
# Forked from andreasroald/helicopter-game
import pygame

# player helicopter
helicopter_1 = pygame.image.load('images/helicopter_1.png')
helicopter_2 = pygame.image.load('images/helicopter_2.png')
helicopter_crash_1 = pygame.image.load('images/helicopter_crash_1.png')
helicopter_crash_2 = pygame.image.load('images/helicopter_crash_2.png')
helicopter_crash_3 = pygame.image.load('images/helicopter_crash_3.png')
helicopter_crash_4 = pygame.image.load('images/helicopter_crash_4.png')
helicopter_damaged_1 = pygame.image.load('images/helicopter_damaged_1.png')
helicopter_damaged_2 = pygame.image.load('images/helicopter_damaged_2.png')

# enemy helicopter
enemy_helicopter_1 = pygame.image.load('images/enemy_helicopter_1.png')
enemy_helicopter_2 = pygame.image.load('images/enemy_helicopter_2.png')

# heart
red_heart = pygame.image.load('images/red_heart.png')

# missile
missile = pygame.image.load('images/missile.png')

# game systems
icon = pygame.image.load('images/icon.png')
mainmenu_background = pygame.image.load('images/background.png')
mainmenu_helicopter = pygame.image.load('images/helicopter_mainmenu.png')
spikes = pygame.image.load('images/spikestrans.gif')

# game scrollable background
background_image = 'images/bg.png'
bg1 = pygame.image.load(background_image)
bg2 = pygame.image.load(background_image)

# list
helicopter_list = [helicopter_1, helicopter_2]
damaged_helicopter_list = [helicopter_damaged_1, helicopter_damaged_2]
enemy_helicopter_list = [enemy_helicopter_1, enemy_helicopter_2]
all_sprites = [helicopter_1, helicopter_2, helicopter_damaged_1, helicopter_damaged_2,
               enemy_helicopter_1, enemy_helicopter_2, helicopter_crash_1,
               helicopter_crash_2, helicopter_crash_3, helicopter_crash_4,
               red_heart, missile, icon, mainmenu_background, mainmenu_helicopter,
               spikes, bg1, bg2]


