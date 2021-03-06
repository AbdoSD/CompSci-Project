import pygame as pg
import random
import math
from settings import *
from sprites import *
from os import path



class Game:
        def __init__(self):
                #initialise game window, clock and the font for any text on screen. Screen sn clock are
                # assigned
                pg.init()
                pg.mixer.init()
                self.screen = pg.display.set_mode((WIDTH, HEIGHT))
                pg.display.set_caption(TITLE)
                self.clock = pg.time.Clock()

                #Controls whether loop at the bottom is running, (whether the game is running)
                self.running = True

                self.font_name = pg.font.match_font(FONT_NAME)
                self.load_data()
                self.player = None
                

        def load_data(self):
                self.dir = path.dirname(__file__)
               
                with open(path.join(self.dir, HS_FILE), 'r') as f:
                        #try and except runs some code and if an error becomes present it runs some other code to run
                        try:
                                self.highscore = int(f.read())
                        except:
                                self.highscore = 0
                
               

        def new(self):
                # Sets the score at the start and defines the players and platforns importing their classes
                #from the sprite file.
                self.score = 0 
                self.all_sprites = pg.sprite.LayeredUpdates()
                self.platforms = pg.sprite.Group()
                self.powerups = pg.sprite.Group()
                self.meteorites = pg.sprite.Group()
                self.fireballs = pg.sprite.Group()
                self.enemies = pg.sprite.Group()
                self.stars = pg.sprite.Group()
                self.player = Player(self)
                #loop that imports the fixed platforms at the start of the screen from the settings page with their
                # 4 attributes of length, width, height, 
                for platforms in PLATFORM_LIST:
                         Platform(self, platforms[0], platforms[1], platforms[2], platforms[3])
                # keeps track of last time enemy was spawned to signal a new enemy needs to be spawned
                self.enemy_timer = 0
                for i in range (6):
                        s = Star(self)
                        s.rect.y += 500
                #whenever new game starts, it should run itself.
                self.run()
                
                
                

        def run(self):
                #game loop. The loop ticks the clock. While the game is being played, the events can happen
                # the updates occurs and any drawings made appear
                self.playing = True
                while self.playing:
                        self.clock.tick(FPS)
                        self.events()
                        self.update()
                        self.draw()
                       
               

        def update(self):
                 #Updates including when the player jumps above and lands on a platform
                self.all_sprites.update()
                #spawn an enemy
                now = pg.time.get_ticks()
                #spwans enemy every 2.5seconds + or - the random choice times to vary times of spawning enemy
                if now - self.enemy_timer > 2500 + random.choice([-1000, -500, 0, 500, 1000]):
                        #enemy will now spawn in this loop
                        self.enemy_timer = now
                        Enemy(self)
                # hit enemies
                enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False)
                if enemy_hits:
                        self.playing = False
                # check if player hits a platform - only if falling. If the bottom half of the player hits the platform it will stop
                # moving . Velocity at the end set to 0 to make sure the player doesnt fall through the platform and
                #can move on it.
                if self.player.vel.y > 0:
                         hits = pg.sprite.spritecollide(self.player, self.platforms, False)
                         if hits:
                                 lowest = hits[0]
                                 for hit in hits:
                                         if hit.rect.bottom > lowest.rect.bottom:
                                                 lowest = hit
                                 if self.player.pos.x < lowest.rect.right + 10 and \
                                    self.player.pos.x > lowest.rect.left - 10:
                                         if self.player.pos.y < lowest.rect.bottom:
                                                 self.player.pos.y = lowest.rect.top
                                                 self.player.vel.y = 0
                                                 self.player.jumping = False

                # check to see if a fireball hit an enemy. The score will update
                hits = pg.sprite.groupcollide(self.enemies, self.fireballs, True, True)
                if hits:
                        self.score +=5

                # if the player reaches the top 1/3 of the screen platforms start to disappear and points can be
                # gained this way
                if self.player.rect.top <= HEIGHT / 3:
                        if random.randrange(100) < 15:
                                Star(self)
                        #Scrolling speed matches with the player,star, enemy, and platform veclocity.
                        self.player.pos.y += max(abs(self.player.vel.y), 2)
                        for star in self.stars:
                                star.rect.y += max(abs(self.player.vel.y / 2), 2)
                        for enemy in self.enemies:
                                 enemy.rect.y += max(abs(self.player.vel.y),2)
                        for platforms in self.platforms:
                                 platforms.rect.y += max(abs(self.player.vel.y), 2)
                                 if platforms.rect.top >= HEIGHT:
                                         platforms.kill()
                                         self.score += 20

                # If player hits a powerup. The velocity upwards of player is equaivalent to
                # BOOST POWER in settings
                power_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
                for power in power_hits:
                         if power.type == 'boost' :
                                 self.player.vel.y = -BOOST_POWER
                                 self.player.jumping = False
                                 

                # If player hits a meteorite
               


                #Die. Player falls of and reaches bottom of the screen then player dies. The platforms are
                #non existent so game ends
                if self.player.rect.bottom > HEIGHT:
                         for sprite in self.all_sprites:
                                 sprite.rect.y -= max(self.player.vel.y, 10)
                                 if sprite.rect.bottom < 0:
                                         sprite.kill()
                if len(self.platforms) == 0:
                         self.playing = False

                       
                                 
                # spawn new platforms to keep average number. Every time the number of platforms on screen
                # goes below 6, random platform spawns, cooridnates are also random but made sure they are
                #on screen
                while len(self.platforms) < 6:
                         width = random.randrange(50, 100)
                         Platform(self,random.randrange(0, WIDTH - width),
                                              random.randrange(-75, - 30),
                                              width, 25)
                         
                         
        def events(self):
                #Game loop - events. When you quit, the game is stopped being played and the
                #program stops running. The varaibles become false.
                 for event in pg.event.get():
                        if event.type == pg.QUIT:
                                if self.playing:
                                        self.playing = False
                                self.running = False
                        if event.type ==pg.KEYDOWN:
                                if event.key == pg.K_SPACE:
                                        self.player.jump()
                        if event.type ==pg.KEYUP:
                                if event.key == pg.K_SPACE:
                                        self.player.jump_cut()
                        if event.type == pg.KEYDOWN:
                                if event.key == pg.K_UP:
                                        self.player.shoot()
                        if event.type == pg.KEYDOWN:
                                if event.key == pg.K_DOWN:
                                        self.player.shoot()

        def draw(self):
                #Game loop - draw
                self.screen.fill(Blue)
                self.all_sprites.draw(self.screen)
                self.draw_text(str(self.score), 22, White, WIDTH / 2, 15)
                #after drawing everything, flip the display
                pg.display.flip()
                
                
               
        def show_start_screen(self):
                self.screen.fill(Blue)
                self.draw_text(TITLE, 48, White, WIDTH / 2, HEIGHT / 4)
                self.draw_text("Left and Right arrows to move", 22, White, WIDTH / 2, HEIGHT / 2)
                self.draw_text("Up and down arrows to shoot", 22, White, WIDTH / 2, HEIGHT * 55/100)
                self.draw_text("Space to jump", 22, White, WIDTH / 2, HEIGHT * 3/5)
                self.draw_text("Press a key to play", 22, White, WIDTH / 2, HEIGHT * 3/4)
                self.draw_text("High Score: " + str(self.highscore), 22, White, WIDTH / 2, 15)
                pg.display.flip()
                self.wait_for_key( )
                
                
                

        def show_go_screen(self):
                # game over or continue
                 if not self.running:
                         return
                 self.screen.fill(Blue)
                 self.draw_text("Game Over", 48, White, WIDTH / 2, HEIGHT / 4)
                 self.draw_text("Score: " + str(self.score), 22, White, WIDTH / 2, HEIGHT / 2)
                 self.draw_text("Press a key to play again", 22, White, WIDTH / 2, HEIGHT * 3/4)
                 if self.score > self.highscore:
                         self.highscore =  self.score
                         self.draw_text("NEW HIGH SCORE!", 22, White, WIDTH / 2, HEIGHT / 2 + 40)
                         with open(path.join(self.dir, HS_FILE), 'w') as f:
                                 f.write(str(self.score))
                 else:
                        self.draw_text("High Score: " + str(self.highscore), 22, White, WIDTH / 2, HEIGHT / 2 + 40)
                   
                 pg.display.flip()
                 self.wait_for_key()
                 
                 

         # function that will pause waiting for player to press keys to start and restart game
         # checks the events: if the person quits the game and closes the window, it should do as such
         # if the person presses any key on board it will load the next part of the game and the program
         #will not stop running.
        def wait_for_key(self):
                 waiting = True
                 while waiting:
                         self.clock.tick(FPS)
                         for event in pg.event.get():
                                 if event.type == pg.QUIT:
                                         waiting = False
                                         self.running = False
                                 if event.type == pg.KEYUP: 
                                          waiting = False

        def draw_text(self, text, size, color, x, y):
                 font = pg.font.Font(self.font_name, size)
                 text_surface = font.render(text, True, color)
                 text_rect = text_surface.get_rect()
                 text_rect.midtop = (x, y)
                 self.screen.blit(text_surface, text_rect)
               



                 
#Instance of the game
g = Game()
g.show_start_screen()
#Starts new game - when game ends, game should go to game over screen
while g.running:
        g.new()
        g.show_go_screen()
#If the loop above ends, it quits 
pg.quit()




                        


       

