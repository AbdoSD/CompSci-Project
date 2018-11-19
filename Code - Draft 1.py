import pygame as pg
import random
import math
from settings import *
from sprites import *
from os import path



class Game:
        def __init__(self):
                #initialise game window, clock and the font for any text on screen
                pg.init()
                pg.mixer.init()
                self.screen = pg.display.set_mode((WIDTH, HEIGHT))
                pg.display.set_caption(TITLE)
                self.clock = pg.time.Clock()
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
                for plat in PLATFORM_LIST:
                       Platform(self, *plat)
                self.enemy_timer = 0
                for i in range (6):
                        s = Star(self)
                        s.rect.y += 500
                self.run()
                
                
                

        def run(self):
                #game loop
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
                if now - self.enemy_timer > 2500 + random.choice([-1000, -500, 0, 500, 1000]):
                        self.enemy_timer = now
                        Enemy(self)
                # hit enemies
                enemy_hits = pg.sprite.spritecollide(self.player, self.enemies, False)
                if enemy_hits:
                        self.playing = False
                # check if player hits a platform - only if falling
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

                # check to see if a fireball hit an enemy
                hits = pg.sprite.groupcollide(self.enemies, self.fireballs, True, True)
                if hits:
                        self.score +=5

                # if the player reaches the top 1/3 of the screen platforms start to disappear and points can be
                # gained this way
                if self.player.rect.top <= HEIGHT / 3:
                        if random.randrange(100) < 15:
                                Star(self)
                        self.player.pos.y += max(abs(self.player.vel.y), 2)
                        for star in self.stars:
                                star.rect.y += max(abs(self.player.vel.y / 2), 2)
                        for enemy in self.enemies:
                                 enemy.rect.y += max(abs(self.player.vel.y),2)
                        for plat in self.platforms:
                                 plat.rect.y += max(abs(self.player.vel.y), 2)
                                 if plat.rect.top >= HEIGHT:
                                         plat.kill()
                                         self.score += 20

                # If player hits a powerup
                power_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
                for power in power_hits:
                         if power.type == 'boost' :
                                 self.player.vel.y = -BOOST_POWER
                                 self.player.jumping = False

                # If player hits a meteorite
               


                #Die
                if self.player.rect.bottom > HEIGHT:
                         for sprite in self.all_sprites:
                                 sprite.rect.y -= max(self.player.vel.y, 10)
                                 if sprite.rect.bottom < 0:
                                         sprite.kill()
                if len(self.platforms) == 0:
                         self.playing = False

                       
                                 
                # spawn new platforms to keep average number
                while len(self.platforms) < 6:
                         width = random.randrange(50, 100)
                         Platform(self,random.randrange(0, WIDTH - width),
                                              random.randrange(-75, - 30),
                                              width, 25)
                         
                         
        def events(self):
                #Game loop - events
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
                self. screen.fill(Blue)
                self.all_sprites.draw(self.screen)
                self.draw_text(str(self.score), 22, White, WIDTH / 2, 15)
        
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
               



                 

g = Game()
g.show_start_screen()
while g.running:
        g.new()
        g.show_go_screen()

pg.quit()




                        


       

