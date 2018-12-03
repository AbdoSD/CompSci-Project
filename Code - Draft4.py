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
                super().__init__()
                #set height and width as local variables, fill the colour of the image.
                width = 50
                height = 50
                self.image = pygame.image.load("img/test2.png")
                self.rect = self.image.get_rect()
                 #speed of the player. Change in its x direction or change
                # in its  y direction
                self.change_x = 0
                self.change_y = 0
                # gains the platform as an attribute so it can gain the platforms attributes and methods
                self.platforms_group = all_platforms_group
                

                
        def update(self):

                #Gravity, defined below
                self.gravity()
               #To move left or right
                self.rect.x += self.change_x
                #To move up or down
                self.rect.y += self.change_y
                #Check to see if player collides with something
                #Resets player position based on the top or bottom of the object
                if self.change_y > 0:
                        collides= pygame.sprite.spritecollide(self, self.platforms_group, False)
                        #If player hits something take the players y coordinate and set it to the top
                        # of the object it has collided with
                        #set y velocity to 0 so the player stops moving
                        if collides:
                                if self.rect.y < collides[0].rect.bottom:
                                        self.rect.bottom = collides[0].rect.top
                                        self.change_y = 0
                                
                #wraps around the top and bottom of screen
                if self.rect.x > WIDTH:
                        self.rect.x= 0
                if self.rect.x < 0:
                        self.rect.x = WIDTH
                #When the top of the player reaches the top third of the screen, everthing should move down.
                #Take the players y postion and move it upwards, use the absolute value since player velocity is
                #negative moving upwards. Take the y position of the platforms and add the y velocity of the
                #player. For each platform, it moves down at the speed of the player
                if self.rect.top <= HEIGHT / 3:
                        self.rect.y += abs(self.change_y)
                        for platforms in self.platforms_group:
                                platforms.rect.y += abs(self.change_y)
                                if platforms.rect.top >= HEIGHT:
                                        platforms.kill()

                # When there are 5 platforms on screen, spawn a random platform as defined below.
                while len(self.platforms_group) == 5:
                        PLATFORMS = Platform(random.randrange(0, WIDTH -100), random.randrange(-20, -10), 120, 80)
                        all_platforms_group.add(PLATFORMS)
                        all_sprites_list.add(PLATFORMS)


        def gravity(self):
                #Effects of gravity
                if self.change_y == 0:
                        self.change_y = 1
                else:
                        self.change_y += 0.25

        def jump(self):
                #check below to see if there is anything to jump from then shift back up 
                self.rect.y +=2
                collides= pygame.sprite.spritecollide(self, self.platforms_group, False)
                self.rect.y -=2
                #Set the speed upwards if its ok to jump
                if collides:
                        self.change_y = -8
                        
        #Player controlled movement
        def move_left(self):
                 self.change_x = -7

        def move_right(self):
                 self.change_x = 7

        def stop(self):
                self.change_x = 0

        #Die. If player hits the bottom of the screen, 
        def die(self):
                if self.rect.bottom > HEIGHT:
                        self.kill()
                        done = True
                # if there are no platforms on screen game loop ends
                if len(self.platforms_group) == 0:
                        done = True

        # for player to shoot, variable called fireball spawns fireball that comes from the center of the player
         # and comes out from the top
        def shoot(self):
                fireball = Fireball(player, self.rect.x,self.rect.y)
                all_sprites_list.add(fireball)

                

class Platform(pygame.sprite.Sprite):
        def __init__(self,x,y,w,h):
                super().__init__()
                self.image = pygame.Surface([100, 25])
                self.image.fill(White)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y


class Fireball(pygame.sprite.Sprite):
        def __init__(self,player,x,y):
                super().__init__()
                self.image = pygame.Surface([25,25])
                self.image.fill(Red)
                self.rect = self.image.get_rect()
                self.player = player
                self.rect.x = self.player.rect.centerx
                self.rect.y = self.player.rect.y
                self.change_y = -10 or 10

        def update(self):
                self.rect.y += self.change_y
                if self.rect.bottom < 0:
                        self.kill()
                

class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y,width,height):
                super().__init__()
                self.image = pygame.Surface([30,30])
                self.image.fill(Orange)
                self.rect = self.image.get_rect()
                self.change_x = 0
                self.change_y = 0
                 

        def update(self):
                self.rect.x += self.change_x
                self.rect.y += self.change_y


#initilaise pygame
pygame.init()

size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)


#set title of the window
pygame.display.set_caption('Space Hopper')

#list to hold the spritrs
all_sprites_list = pygame.sprite.Group()
#create the sprites
#platform = Platform()
all_platforms_group = pygame.sprite.Group()
p1 = Platform(300, HEIGHT - 100, 120,80)
all_sprites_list.add(p1)
all_platforms_group.add(p1)
p2 = Platform(180, HEIGHT -  220, 120, 80)
all_sprites_list.add(p2)
all_platforms_group.add(p2)
p3 = Platform(380, HEIGHT -  350, 120, 80)
all_sprites_list.add(p3)
all_platforms_group.add(p3)
p4 = Platform(200, HEIGHT -  450, 120, 80)
all_sprites_list.add(p4)
all_platforms_group.add(p4)
p5 = Platform(330, HEIGHT -  600, 120, 80)
all_sprites_list.add(p5)
all_platforms_group.add(p5)
PLATFORMS = Platform(random.randrange(0, WIDTH -100), random.randrange(-50, -30), 120, 80)
all_platforms_group.add(PLATFORMS)
all_sprites_list.add(PLATFORMS)

player = Player(all_platforms_group)

#sets the player postion x and y cooridnates and adds it to sprite list
player.rect.x = 300
player.rect.y = HEIGHT - 100
all_sprites_list.add(player)


#loop until the player clicks the close button
done = False
#manage how fast the screen updates
clock = pygame.time.Clock()


#-------MAIN PROGRAM LOOP--------#
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                # When holding down a key      
                keys = pygame.key.get_pressed()
                if keys [pygame.K_LEFT]:
                        player.move_left()
                if keys [pygame.K_RIGHT]:
                        player.move_right()
                if keys [pygame.K_SPACE]:
                        player.jump()
                if keys[pygame.K_UP]:
                        player.shoot()
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT and player.change_x < 0:
                                player.stop()
                        if event .key == pygame.K_RIGHT and player .change_x >0:
                                player.stop()

               

        #DRAW TEXT CODE
        screen.fill(Blue)
        all_sprites_list.draw(screen)
        # screen blit allows the player image to be on top of everything else so when it passes somwthing
        # it doesnt disappear behind it.
        screen.blit(player.image, player.rect)

         #Update the player
        all_sprites_list.update()
        all_platforms_group.update()
         
         #limit to 60 frames per second of screen update
        clock.tick(60)
        #updates the screen with any changes
        pygame.display.flip()

pygame.quit()


