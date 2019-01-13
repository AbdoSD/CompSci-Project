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

# Drwaing the healtbar for the player. Its attributes are the surface(the screen) its colour which is green,
# its x and y coordinates which are in the top left corner of the screen and a player_health value so it can
#decwhich can decrease.
def draw_health(screen, color, x, y, health):
                #widht and height local constant variables that never change. The player_health can change
                BAR_HEIGHT = 20
                # Bar is a variable for a rectangle with x and y 1and then a widht of the amount filled calculated above
                # and height of the constant Bar height. Bar changes colour when player health reaches certain point
             #   bar = pygame.Rect(x,y, amount_filled, BAR_HEIGHT)
                if health > 75:
                        color = Green
                elif health > 30:
                        color = Yellow
                else:
                        color = Red
                if health < 0:
                    health = 0
                pygame.draw.rect(screen,color,[x,y,health,BAR_HEIGHT],0)



        

class Player(pygame.sprite.Sprite):
        def __init__(self, all_platforms_group, enemy_group):
                super().__init__()
                #set height and width as local variables, fill the colour of the image.
                width = 50
                height = 50
                self.image =  pygame.Surface([width,height])
                self.image.fill(Green)
                self.rect = self.image.get_rect()
                #speed of the player. Change in its x direction or change
                # in its  y direction
                self.change_x = 0
                self.change_y = 0
                # gains the platform as an attribute so it can gain the platforms attributes and methods
                self.platforms_group = all_platforms_group
                self.enemy_group = enemy_group
                self.health= 100
                #The initialisation of a timer that will count from zero and time that amount of time that passes once an enemy
              
                
                
                

                
        def update(self):
                #Gravity, defined below
                self.gravity()
               #To move left or right
                self.rect.x += self.change_x
                #To move up or down
                self.rect.y += self.change_y
                #Return the amount of seconds or milleiseconds that have passed since the timer began
                
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

                # Enemy collision with player: Every half a second the timer checks for collisions between the player and enemy
                #If there is a collision, ilast for half a second, reduces health by -20 and the timer resets to zero
                enemycollision = pygame.sprite.spritecollide(self, self.enemy_group, False)
                if enemycollision:
                    self.health = self.health - 20
                
                    
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
                        for enemies in self.enemy_group:
                                enemies.rect.y += abs(self.change_y)
                                if enemies.rect.top >= HEIGHT:
                                        enemies.kill()
                                     
                if self.rect.bottom > HEIGHT:
                        done = True
                       
                # if there are no platforms on screen game loop ends
                if len(self.platforms_group) == 0:
                        done = True
                                
        

                # When there are 5 platforms on screen, spawn a random platform as defined below.
                while len(self.platforms_group) == 5:
                        PLATFORMS = Platform(random.randrange(0, WIDTH -100), random.randrange(-45,-40), 120, 80)
                        all_platforms_group.add(PLATFORMS)
                        all_sprites_list.add(PLATFORMS)

                while len(self.enemy_group) == 2:
                    ENEMIES = Enemy(0 or WIDTH - 30, random.randrange(-80, -30), 30, 30)
                    all_sprites_list.add(ENEMIES)
                    enemy_group.add(ENEMIES)
                    
                
        def gravity(self):
                #Effects of gravity
                if self.change_y == 0:
                        self.change_y = 1
                else:
                        self.change_y += 0.45

        def jump(self):
                #check below to see if there is anything to jump from then shift back up 
                self.rect.y +=2
                collides= pygame.sprite.spritecollide(self, self.platforms_group, False)
                self.rect.y -=2
                #Set the speed upwards if its ok to jump
                if collides:
                        self.change_y = -10
                        
        #Player controlled movement
        def move_left(self):
                 self.change_x = -7

        def move_right(self):
                 self.change_x = 7

        def stop(self):
                self.change_x = 0

        #Die. If player hits the bottom of the screen, 
        
                        

        # for player to shoot, variable called fireball spawns fireball that comes from the center of the player
         # and comes out from the top
        def shoot(self):
                fireball = Fireball(player, enemy_group, self.rect.x,self.rect.y)
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
        def __init__(self,player,enemy_group,x,y):
                super().__init__()
                self.image = pygame.Surface([25,25])
                self.image.fill(Red)
                self.rect = self.image.get_rect()
                self.player = player
                self.enemy_group = enemy_group
                self.rect.x = self.player.rect.centerx
                self.rect.y = self.player.rect.y
                self.change_y = -8
                

        def update(self):
                self.rect.y += self.change_y
                if self.rect.bottom < 0:
                        self.kill()
                fireball_hits = pygame.sprite.spritecollide(self, self.enemy_group, True)
               
                    
      
class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y,width,height):
                super().__init__()
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

size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)
font= pygame.font.Font('freesansbold.ttf', 22)


#set title of the window
pygame.display.set_caption('Space Hopper')

#list to hold the spritrs
all_sprites_list = pygame.sprite.Group()
#create the sprites
#platform = Platform()
all_platforms_group = pygame.sprite.Group()
newplatform = Platform(300, HEIGHT - 100, 120,80)
all_sprites_list.add(newplatform)
all_platforms_group.add(newplatform)
newplatform = Platform(180, HEIGHT -  220, 120, 80)
all_sprites_list.add(newplatform)
all_platforms_group.add(newplatform)
newplatform = Platform(380, HEIGHT -  350, 120, 80)
all_sprites_list.add(newplatform)
all_platforms_group.add(newplatform)
newplatform= Platform(200, HEIGHT -  450, 120, 80)
all_sprites_list.add(newplatform)
all_platforms_group.add(newplatform)
newplatform = Platform(330, HEIGHT -  600, 120, 80)
all_sprites_list.add(newplatform) 
all_platforms_group.add(newplatform)
PLATFORMS = Platform(random.randrange(0, WIDTH -100), random.randrange(-50, -30), 120, 80)
all_platforms_group.add(PLATFORMS)
all_sprites_list.add(PLATFORMS)

enemy_group = pygame.sprite.Group()
newenemy = Enemy(0, HEIGHT - 380, 30, 30)
all_sprites_list.add(newenemy)
enemy_group.add(newenemy)
newenemy = Enemy(WIDTH - 30, HEIGHT - 530, 30, 30)
all_sprites_list.add(newenemy)
enemy_group.add(newenemy)
ENEMIES = Enemy(0 or WIDTH - 30, random.randrange(-80, -30), 30, 30)
all_sprites_list.add(ENEMIES)
enemy_group.add(ENEMIES)
                    


#sets the player postion x and y cooridnates and adds it to sprite list
player = Player(all_platforms_group, enemy_group)
player.rect.x = 300
player.rect.y = HEIGHT - 100
all_sprites_list.add(player)





#loop until the player clicks the close button
done = False

#manage how fast the screen updates
clock = pygame.time.Clock()




#-------MAIN PROGRAM LOOP--------#
while not done:
        #limit to 60 frames per second of screen update
        clock.tick(60)
        

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
        draw_health(screen, Green,10, 10, player.health)
        
         # screen blit allows the player image to be on top of everything else so when it passes somwthing
        # it doesnt disappear behind it.
        screen.blit(player.image, player.rect)
        

        #Update the player
        all_sprites_list.update()
        all_platforms_group.update()
        enemy_group.update()
        
        
        #updates the screen with any changes
        pygame.display.flip()

pygame.quit()


