#Sprite classes for platform games

import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
        #Sprite for the player
        def __init__(self, game):
                self._layer = PLAYER_LAYER
                self.groups = game.all_sprites
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.walking = False
                self.jumping = False
                self.fireballs = False
                self.image = pg.image.load("img/test2.png").convert_alpha()
                
                self.rect = self.image.get_rect()
                self.rect.center = (WIDTH / 2 , HEIGHT - 25)
                self.pos = vec(WIDTH / 2, HEIGHT -25)
                self.vel = vec(0,0)
                self.acc = vec(0,0)
                

        def jump_cut(self):
                if self.jumping:
                        if self.vel.y < -3:
                                self.vel.y = -3


        def jump(self):
                #jumps upwards if only standing on a platform
                self.rect.y += 2
                hits = pg.sprite.spritecollide(self, self.game.platforms, False)
                self.rect.y -= 2
                if hits and not self.jumping:
                        self.jumping = True
                        self.vel.y = - 20

        def update (self):
                self.acc = vec(0, PLAYER_GRAV)
                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT]:
                    self.acc.x = -PLAYER_ACC
                if keys[pg.K_RIGHT]:
                    self.acc.x = PLAYER_ACC

                #apply friction
                self.acc.x += self.vel.x* PLAYER_FRICTION
                #equations of motion
                self.vel += self.acc
                if abs(self.vel.x) < 0.1:
                        self.vel.x = 0 
                self.pos += self.vel + 0.5 * self.acc
                #wraps around the top and bottom of screen
                if self.pos.x > WIDTH:
                        self.pos.x= 0
                if self.pos.x < 0:
                        self.pos.x = WIDTH
                
                self.rect.midbottom = self.pos

                

        def shoot(self):
                fireball = Fireball(self.game, self.rect.centerx, self.rect.top or self.rect.bottom)
                self.game.all_sprites.add(fireball)
                self.game.fireballs.add(fireball)



        


class Platform(pg.sprite.Sprite):
        def __init__(self, game, x, y, w, h):
                self.groups = game.all_sprites, game.platforms
                pg.sprite.Sprite. __init__(self, self.groups)
                self.game = game
                self.image = pg.Surface([w, h])
                self.image.fill(White)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                if randrange(100) < POWER_SPAWN_PCT:
                        Power(self.game, self)

class Star(pg.sprite.Sprite):
        def __init__(self, game):
                self._layer = STAR_LAYER
                self.groups = game.all_sprites, game.stars
                #super. __init__(self, self.groups)
                pg.sprite.Sprite. __init__(self, self.groups)
                self.game = game
                self.image = pg.image.load("img/saturn.png")
                self.rect = self.image.get_rect()
                self.rect.x = randrange(WIDTH - self.rect.width)
                self.rect.y = randrange(-500, -50)

        def update(self):
                if self.rect.top > HEIGHT:
                        self.kill()

class Power(pg.sprite.Sprite):
        def __init__(self, game, plat):
                self._layer = POWER_LAYER
                self.groups = game.all_sprites, game.powerups
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.plat = plat
                self.type = choice (['boost'])
                self.image = pg.image.load("img/assroids.png")
                self.rect = self.image .get_rect()
                self.rect.centerx = self.plat.rect.centerx
                self.rect.bottom = self.plat.rect.top - 5

        def update(self):
                self.rect.bottom = self.plat.rect.top - 5
                if not self.game.platforms.has(self.plat):
                        self.kill()

class Enemy(pg.sprite.Sprite):
        def __init__(self, game):
                self._layer = ENEMY_LAYER
                self.groups = game.all_sprites, game.enemies
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.image = pg.image.load("img/greenie.png")
                self.rect = self.image .get_rect()
                self.rect.centerx = choice([-100, WIDTH + 100])
                self.vx = randrange(3, 6)
                if self.rect.centerx > WIDTH:
                        self.vx *= -1
                self.rect.y = randrange(HEIGHT / 2)
                self.vy = 0
                self.dy = 0.5

        def update(self):
                self.rect.x += self.vx
                self.vy += self.dy
                if self.vy > 3 or self.vy < -3:
                        self.dy *= -1
                center = self.rect.center
                self.rect = self.image .get_rect()
                self.rect.center = center
                self.rect.y += self.vy
                if self.rect.left > WIDTH + 100 or self.rect.right < -100:
                        self.kill()

class Meteorite(pg.sprite.Sprite):
        def __init__(self, game, plat):
                self._layer = METEORITE_LAYER
                self.groups = game.all_sprites, game.meteorites
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.plat = plat
                self.type = choice(['fireballs'])
                self.image = pg.Surface([20, 20])
                self.image.fill(Ivory)
                self.rect = self.image .get_rect()
                self.rect.centerx = self.plat.rect.centerx
                self.rect.bottom = self.plat.rect.top - 5

        def update(self):
                self.rect.bottom = self.plat.rect.top - 5
                if not self.game.platforms.has(self.plat):
                        self.kill()

class Fireball(pg.sprite.Sprite):
        def __init__(self,game,x,y):
                self._layer = FIREBALL_LAYER
                self.groups = game.all_sprites, game.fireballs
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.image = pg.image.load("img/fireball.png")
                
                self.rect = self.image.get_rect()
                self.rect.bottom = y 
                self.rect.top = y
                self.rect.centerx = x
                self.speedy = -10 or 10

        def update(self):
                self.rect.y += self.speedy
                #kill if it moves off the top of the screen
                if self.rect.bottom < 0:
                        self.kill()
                if self.rect.top > HEIGHT:
                        self.kill()
                
        
                
 


         
                  




