import pygame
import math
import random
import sys

# colours to be used in game
Green = (50, 205, 50)
Ivory = (255, 255, 240)
Blue = (0, 0, 255)
Red = (255, 0, 0)
Purple = (255, 0, 255)
Grey = (190, 190, 190)
Black = (0, 0, 0)
White = (255, 255, 255)
Yellow = (255, 255, 0)
Orange = (255, 165, 0)

# screen width and height
WIDTH = 540
HEIGHT = 720


# Drwaing the healtbar for the player. Its attributes are the surface(the screen) its colour which is green,
# its x and y coordinates which are in the top left corner of the screen and a player_health value so it can
# decwhich can decrease.
def draw_health(screen, color, x, y, health):
    # widht and height local constant variables that never change. The player_health can change
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
    pygame.draw.rect(screen, color, [x, y, health, BAR_HEIGHT], 0)


# Draw the text on screen function. It has text, the string for what will be said. The
# size of the font, the colour of the text and the x and y cooridnates. The font obects is then
# defined to draw text. Text Surface renders the pixels of the text onto the screen.
# The true means whther the text will be anit-aliased or not. Anit-aliased gets rid of rough
# edges on corners of letters and makes the writing look smoother. Text rect will create
# a text box where the text will go in. The x and y of the actual text will go directly in the
# centre of the box.
def message_display(surface, text, size, color, x, y):
    font = pygame.font.SysFont('OCR A extended', size)
    titleFont = pygame.font.SysFont('OCR A extended', size)
    TextSurface = font.render(text, True, color)
    TextRect = TextSurface.get_rect()
    TextRect.center = (x, y)
    screen.blit(TextSurface, TextRect)


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms_group, enemy_group, powerups_group, all_sprites_list):
        super().__init__()
        # set height and width as local variables, fill the colour of the image.
        width = 50
        height = 50
        self.image = pygame.image.load("img/bluie.png").convert_alpha()

        self.rect = self.image.get_rect()
        # speed of the player. Change in its x direction or change
        # in its  y direction
        self.change_x = 0
        self.change_y = 0
        # gains the platform as an attribute so it can gain the platforms attributes and methods
        self.platforms_group = platforms_group
        self.enemy_group = enemy_group
        self.powerups_group = powerups_group
        self.all_sprites_list = all_sprites_list
        self.health = 100
        self.score = 0
        # The initialisation of a timer that will count from zero and time that amount of time that passes once an enemy
        # player collides with enemy and begins losing health
        self.time_since_last_hit = 0
        # A counter that will spawn enemies based on the screen scrolling upwards initially set at zero
        self.next_enemy_scroll_counter = 0
        # A counter that will spawn powwrups also based on the screen scrolling upwards
        self.next_powerup_scroll_counter = 100

        self.time_since_last_shot = 0

    def update(self):
        # Gravity, defined below
        self.gravity()
        # To move left or right
        self.rect.x += self.change_x
        # To move up or down
        self.rect.y += self.change_y
        # Return the amount of seconds or milleiseconds that have passed since the timer began
        self.time_since_last_hit += clock.get_time()

        self.time_since_last_shot += clock.get_time()

        # Check to see if player collides with something
        # Resets player position based on the top or bottom of the object
        if self.change_y > 0:
            collides = pygame.sprite.spritecollide(self, self.platforms_group, False)
            # If player hits something take the players y coordinate and set it to the top
            # of the object it has collided with
            # set y velocity to 0 so the player stops moving
            if collides:
                if self.rect.y < collides[0].rect.bottom:
                    self.rect.bottom = collides[0].rect.top
                    self.change_y = 0

        # Enemy collision with player: Every half a second the timer checks for collisions between the player and enemy
        # If there is a collision, ilast for half a second, reduces health by -20 and the timer resets to zero
        if self.time_since_last_hit > 1000:
            enemycollision = pygame.sprite.spritecollide(self, self.enemy_group, False)
            if enemycollision:
                self.health = self.health - 20
                self.time_since_last_hit = 0

        # collision for when player collides with powerup. If so then the powerup disappears and player should fly upwards at faster velocity
        powerupcollision = pygame.sprite.spritecollide(self, self.powerups_group, True)
        if powerupcollision:
            self.change_y = -25

        # wraps around the top and bottom of screen
        if self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = WIDTH
        # When the top of the player reaches the top third of the screen, everthing should move down.
        # Take the players y postion and move it upwards, use the absolute value since player velocity is
        # negative moving upwards. Take the y position of the platforms and add the y velocity of the
        # player. For each platform, it moves down at the speed of the player
        if self.rect.top <= HEIGHT / 3:
            self.rect.y += abs(self.change_y)
            for platforms in self.platforms_group:
                platforms.rect.y += abs(self.change_y)
                if platforms.rect.top >= HEIGHT:
                    self.score += 10
                    platforms.kill()
            for enemies in self.enemy_group:
                enemies.rect.y += abs(self.change_y)
                if enemies.rect.top >= HEIGHT:
                    enemies.kill()
            for powerups in self.powerups_group:
                powerups.rect.y += abs(self.change_y)
                if powerups.rect.top >= HEIGHT:
                    powerups.kill()
            self.next_enemy_scroll_counter -= abs(self.change_y)
            self.next_powerup_scroll_counter -= abs(self.change_y)

        # When there are 5 platforms on screen, spawn a random platform as defined below.
        while len(self.platforms_group) == 5:
            platform = Platform(random.randrange(0, WIDTH - 100), random.randrange(-45, -40), random.randrange(60, 100),
                                25)
            self.platforms_group.add(platform)
            self.all_sprites_list.add(platform)

        # To spawn random enemies, if there are less than 3 and the timer is zero..
        if len(self.enemy_group) < 3 and self.next_enemy_scroll_counter <= 0:
            # One line if statement that chooses one of two random x coordinates to spawn an enemy
            newenemyx = 0 if random.randint(0, 1) == 0 else WIDTH - 30
            # Random y cooridnate just above the screen
            newenemyy = random.randrange(-60, -30)
            enemy = Enemy(newenemyx, newenemyy, 30, 30)
            self.all_sprites_list.add(enemy)
            self.enemy_group.add(enemy)
            # spawn the enemy at the y cooridnate specified + a number of pixels to space it out
            self.next_enemy_scroll_counter = (newenemyy) + 200

        # if the counter is at zero, spawn a powerup and spawn it every 1200 to 2000 pixels
        if self.next_powerup_scroll_counter <= 0:
            newpowerupx = random.randint(0, WIDTH - 40)
            newpowerupy = -30
            powerup = Powerup(newpowerupx, newpowerupy, 25, 25)
            self.powerups_group.add(powerup)
            self.all_sprites_list.add(powerup)
            self.next_powerup_scroll_counter = random.randint(1500, 2000)

    def gravity(self):
        # Effects of gravity
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.5

    def jump(self):
        # check below to see if there is anything to jump from then shift back up
        self.rect.y += 2
        collides = pygame.sprite.spritecollide(self, self.platforms_group, False)
        self.rect.y -= 2
        # Set the speed upwards if its ok to jump
        if collides:
            self.change_y = -12

    def dead(self):
        return self.rect.top > HEIGHT or self.health <= 0

    # Player controlled movement
    def move_left(self):
        self.change_x = -7

    def move_right(self):
        self.change_x = 7

    def stop(self):
        self.change_x = 0

    # for player to shoot, variable called fireball spawns fireball that comes from the center of the player
    # and comes out from the top
    def shoot(self):
        if self.time_since_last_shot > 2000:
            fireball = Fireball(self, self.enemy_group, self.rect.x, self.rect.y)
            self.all_sprites_list.add(fireball)
            self.time_since_last_shot = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("img/platform.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Fireball(pygame.sprite.Sprite):
    def __init__(self, player, enemy_group, x, y):
        super().__init__()
        self.image = pygame.image.load("img/fireball.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.player = player
        self.enemy_group = enemy_group
        self.rect.x = self.player.rect.centerx
        self.rect.y = self.player.rect.y
        self.change_y = -8
        self.player.score = player.score

    def update(self):
        self.rect.y += self.change_y
        if self.rect.bottom < 0:
            self.kill()
        fireball_hits = pygame.sprite.spritecollide(self, self.enemy_group, True)
        if fireball_hits:
            self.player.score += 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("img/crabby.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.x == 0:
            self.change_x = 6
        if self.rect.x == WIDTH - 30:
            self.change_x = -6


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("img/ufo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 3

    def update(self):
        self.rect.y += self.vel_y


# initilaise pygame
pygame.init()

# manage how fast the screen updates
clock = pygame.time.Clock()

size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)

# set title of the window
pygame.display.set_caption('Space Hopper')


# this is the introduction function. it will load when the game runs. It will be filled
def intro():
    screen.fill(Blue)
    message_display(screen, "Space Hopper", 48, Green, WIDTH / 2, HEIGHT - 600)
    message_display(screen, "Left key to move left", 24, Yellow, WIDTH / 2, HEIGHT - 400)
    message_display(screen, "Right key to move Right", 24, Yellow, WIDTH / 2, HEIGHT - 350)
    message_display(screen, "Space Bar to jump", 24, Yellow, WIDTH / 2, HEIGHT - 300)
    message_display(screen, "Up arrow to shoot", 24, Yellow, WIDTH / 2, HEIGHT - 250)
    message_display(screen, "Press any key to play!", 24, Yellow, WIDTH / 2, HEIGHT - 100)
    pygame.display.flip()
    key_pressed = False
    while not key_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressed = True





def game():
    # list to hold the spritrs
    all_sprites_list = pygame.sprite.Group()
    # create the sprites
    # platform = Platform()
    platforms_group = pygame.sprite.Group()
    newplatform = Platform(300, HEIGHT - 100, 120, 25)
    all_sprites_list.add(newplatform)
    platforms_group.add(newplatform)
    newplatform = Platform(180, HEIGHT - 220, 120, 25)
    all_sprites_list.add(newplatform)
    platforms_group.add(newplatform)
    newplatform = Platform(380, HEIGHT - 350, 120, 25)
    all_sprites_list.add(newplatform)
    platforms_group.add(newplatform)
    newplatform = Platform(200, HEIGHT - 450, 120, 25)
    all_sprites_list.add(newplatform)
    platforms_group.add(newplatform)
    newplatform = Platform(330, HEIGHT - 600, 120, 25)
    all_sprites_list.add(newplatform)
    platforms_group.add(newplatform)
    platform = Platform(random.randrange(0, WIDTH - 100), random.randrange(-50, -30), random.randrange(60, 100), 25)
    platforms_group.add(platform)
    all_sprites_list.add(platform)

    enemy_group = pygame.sprite.Group()
    newenemy = Enemy(0, HEIGHT - 380, 30, 30)
    all_sprites_list.add(newenemy)
    enemy_group.add(newenemy)
    newenemy = Enemy(WIDTH - 30, HEIGHT - 530, 30, 30)
    all_sprites_list.add(newenemy)
    enemy_group.add(newenemy)

    powerups_group = pygame.sprite.Group()

    # sets the player postion x and y cooridnates and adds it to sprite list
    player = Player(platforms_group, enemy_group, powerups_group, all_sprites_list)
    player.rect.x = 300
    player.rect.y = HEIGHT - 100
    all_sprites_list.add(player)

    # -------MAIN PROGRAM LOOP--------#

    while not player.dead():
        # limit to 60 frames per second of screen update
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # When holding down a key
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if keys[pygame.K_SPACE]:
                player.jump()
            if keys[pygame.K_UP]:
                player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player
        all_sprites_list.update()

        # DRAW TEXT CODE
        screen.fill(Blue)
        all_sprites_list.draw(screen)
        draw_health(screen, Green, 10, 10, player.health)
        message_display(screen, "Score:" + str(player.score), 22, Yellow, WIDTH / 2, 15)

        # screen blit allows the player image to be on top of everything else so when it passes somwthing
        # it doesnt disappear behind it.
        screen.blit(player.image, player.rect)

        # updates the screen with any changes
        pygame.display.flip()



intro()
score = game()

pygame.quit()



                        


       

