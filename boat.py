import sprites
import random
import pygame


class Boat(object):

    shoot_counter = 0
    bullets = []

    boat_hit_player = False

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def movement(self):
        if self.x > -110:
            self.x -= 2
        else:
            self.boat_hit_player = False

    def shoot(self):

            self.shoot_counter += 1

            if self.shoot_counter >= 50:
                self.bullets.append([self.x, self.y])
                self.shoot_counter = 0

    def init(self):
        self.movement()
        self.shoot()
