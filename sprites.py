#Sprite classes for platform games

import pygame
from settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
        #Sprite for the player
        def __init__(self, game, color, width, height, speed):
                pygame.sprite.Sprite.__init__(self)
                self.game = game
                self.image = pygame.Surface([30, 40])   
                self.image.fill(Purple)
                self.rect = self.image.get_rect()
                self.rect.center = (WIDTH / 2 , HEIGHT - 25)
                self.pos = vec(WIDTH / 2, HEIGHT -25)
                self.vel = vec(0,0)
                self.acc = vec(0,0)

        def jump(self):
                #jumps upwards if only standing on a platform
                self.rect.x += 1
                hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
                self.rect.x -= 1
                if hits:
                        self.vel.y = - 20

        def update (self):
                self.acc = vec(0, PLAYER_GRAV)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.acc.x = -PLAYER_ACC
                if keys[pygame.K_RIGHT]:
                    self.acc.x = PLAYER_ACC

                #apply friction
                self.acc.x += self.vel.x* PLAYER_FRICTION
                #equations of motion
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc
                #wraps around the top and bottom of screen
                if self.pos.x > WIDTH:
                        self.pos.x= 0
                if self.pos.x < 0:
                        self.pos.x = WIDTH
                
                self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, w, h):
                pygame.sprite.Sprite. __init__(self)
                self.image = pygame.Surface([w, h])
                self.image.fill(Blue)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
 


         
                  




