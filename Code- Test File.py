import pygame 

import math

import random







#colours to be used in game

Green = (50,205 ,50)

Ivory = (255,255,240)

Blue = (0,0,255)

Red = (255,0,0)

Purple = (255,0,255)

Grey = (190,190,190)

Black = (0,0,0)

White = (255, 255, 255)

Yellow = (255, 255, 0)

Orange = (255, 165, 0)



#screen width and height 

WIDTH = 540

HEIGHT = 720

class Player(pygame.sprite.Sprite):


 
        def __init__(self, all_platforms_group):


 
        def __init__(self, all_platforms_group, enemy_group):


 
                super().__init__()


 
                #set height and width as local variables, fill the colour of the image.


 
                width = 50


 
                height = 50


 
                self.image =  pygame.Surface([width,height])


 
                self.image.fill(Green)


 
                self.rect = self.image.get_rect()


 
                ()


 
                 #speed of the player. Change in its x direction or change


 
                #speed of the player. Change in its x direction or change


 
                # in its  y direction


 
                self.change_x = 0


 
                self.change_y = 0


 
                # gains the platform as an attribute so it can gain the platforms attributes and methods


 
                self.platforms_group = all_platforms_group


 
                self.enemy_group = enemy_group


 
                self.health= 100


 


        def update(self):


 



 
                #Gravity, defined below


 
                self.gravity()


 
               #To move left or right
 
@@ -60,8 +80,15 @@ def update(self):


 
                                if self.rect.y < collides[0].rect.bottom:


 
                                        self.rect.bottom = collides[0].rect.top


 
                                        self.change_y = 0


 



 
                #wraps around the top and bottom of screen


 



 
                # If an enemy collides with the player


 
                enemycollision = pygame.sprite.spritecollide(self, self.enemy_group, False)


 
                if enemycollision:


 
                    self.health = self.health - 20


 



 



 



 
                 #wraps around the top and bottom of screen


 
                if self.rect.x > WIDTH:


 
                        self.rect.x= 0


 
                if self.rect.x < 0:
 
@@ -76,13 +103,26 @@ def update(self):


 
                                platforms.rect.y += abs(self.change_y)


 
                                if platforms.rect.top >= HEIGHT:


 
                                        platforms.kill()


 
                        for enemies in self.enemy_group:


 
                                enemies.rect.y += abs(self.change_y)


 
                                if enemies.rect.top >= HEIGHT:


 
                                        enemies.kill()


 



 



 



 
                # When there are 5 platforms on screen, spawn a random platform as defined below.


 
                while len(self.platforms_group) == 5:


 
                        PLATFORMS = Platform(random.randrange(0, WIDTH -100), random.randrange(-45,-40), 120, 80)


 
                        all_platforms_group.add(PLATFORMS)


 
                        all_sprites_list.add(PLATFORMS)


 




 



 



 



 
 def gravity(self):


 
                #Effects of gravity
 
@@ -114,19 +154,21 @@ def stop(self):


 
        def die(self):


 
                if self.rect.bottom > HEIGHT:


 
                        self.kill()


 
                        done = True


 



 
                # if there are no platforms on screen game loop ends


 
                if len(self.platforms_group) == 0:


 
                        done = True


 
                        self.kill()


 



 



 
        # for player to shoot, variable called fireball spawns fireball that comes from the center of the player


 
         # and comes out from the top


 
        def shoot(self):


 
                fireball = Fireball(player, self.rect.x,self.rect.y)


 
                fireball = Fireball(player, enemy_group, self.rect.x,self.rect.y)


 
                all_sprites_list.add(fireball)


 



 



 



 



 



 
class Platform(pygame.sprite.Sprite):


 
        def __init__(self,x,y,w,h):


 
                super().__init__()
 
@@ -138,20 +180,23 @@ def __init__(self,x,y,w,h):


 



 



 
class Fireball(pygame.sprite.Sprite):


 
        def __init__(self,player,x,y):


 
        def __init__(self,player,enemy_group,x,y):


 
                super().__init__()


 
                self.image = pygame.Surface([25,25])


 
                self.image.fill(Red)


 
                self.rect = self.image.get_rect()


 
                self.player = player


 
                self.enemy_group = enemy_group


 
                self.rect.x = self.player.rect.centerx


 
                self.rect.y = self.player.rect.y


 
                self.change_y = -10 


 
                self.change_y = -10


 



 
        def update(self):


 
                self.rect.y += self.change_y


 
                if self.rect.bottom < 0:


 
                        self.kill()


 
                fireball_hits = pygame.sprite.spritecollide(self, self.enemy_group, True)


 



 



 



 
class Enemy(pygame.sprite.Sprite):
 
@@ -160,15 +205,21 @@ def __init__(self,x,y,width,height):


 
                self.image = pygame.Surface([30,30])


 
                self.image.fill(Orange)


 
                self.rect = self.image.get_rect()


 
                self.rect.x = x


 
                self.rect.y = y


 
                self.change_x = 0


 
                self.change_y = 0


 



 



 
        def update(self):


 
                self.rect.x += self.change_x


 
                self.rect.y += self.change_y


 
                if self.rect.x == 0:


 
                        self.change_x = 3


 
                if self.rect.x == WIDTH -30:


 
                        self.change_x = -3


 



 



 



 



 
#initilaise pygame


 
pygame.init()


 

 
@@ -197,22 +248,40 @@ def update(self):


 
all_sprites_list.add(newplatform)


 
all_platforms_group.add(newplatform)


 
newplatform = Platform(330, HEIGHT -  600, 120, 80)


 
all_sprites_list.add(newplatform)


 
all_sprites_list.add(newplatform) 


 
all_platforms_group.add(newplatform)


 
PLATFORMS = Platform(random.randrange(0, WIDTH -100), random.randrange(-50, -30), 120, 80)


 
all_platforms_group.add(PLATFORMS)


 
all_sprites_list.add(PLATFORMS)


 



 
player = Player(all_platforms_group)


 



 
enemy_group = pygame.sprite.Group()


 
newenemy = Enemy(0, HEIGHT - 380, 30, 30)


 
all_sprites_list.add(newenemy)


 
enemy_group.add(newenemy)


 
newenemy = Enemy(WIDTH - 30, HEIGHT - 530, 30, 30)


 
all_sprites_list.add(newenemy)


 
enemy_group.add(newenemy)


 
ENEMIES = Enemy(0 or WIDTH - 30, random.randrange(-60, -40), 30, 30)


 
all_sprites_list.add(ENEMIES)


 
enemy_group.add(ENEMIES)


 



 



 



 



 



 
#sets the player postion x and y cooridnates and adds it to sprite list


 
player = Player(all_platforms_group, enemy_group)


 
player.rect.x = 300


 
player.rect.y = HEIGHT - 100


 
all_sprites_list.add(player)


 



 



 



 
#loop until the player clicks the close button


 
done = False


 
playing = True


 



 
#manage how fast the screen updates


 
clock = pygame.time.Clock()


 

 
@@ -243,16 +312,20 @@ def update(self):


 
        #DRAW TEXT CODE


 
        screen.fill(Blue)


 
        all_sprites_list.draw(screen)


 
        # screen blit allows the player image to be on top of everything else so when it passes somwthing


 
        draw_health(screen, Green,10, 10, player.health)


 



 
         # screen blit allows the player image to be on top of everything else so when it passes somwthing


 
        # it doesnt disappear behind it.


 
        screen.blit(player.image, player.rect)


 



 
         #Update the player


 
          #Update the player


 
        all_sprites_list.update()


 
        all_platforms_group.update()


 



 
        enemy_group.update()


 



 
         #limit to 60 frames per second of screen update


 
        clock.tick(60)


 



 
        #updates the screen with any changes


 
        pygame.display.flip()








                

  
