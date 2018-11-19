import pygame
import random
import math
from settings import *
from sprites import *
from os import path



class Game:
        def __init__(self):
                #initialise game window, clock and the font for any text on screen
                pygame.init()
                pygame.mixer.init()
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption(TITLE)
                self.clock = pygame.time.Clock()
                self.running = True
                self.font_name = pygame.font.match_font(FONT_NAME)
                self.load_data()
                

        def load_data(self):
                self.dir = path.dirname(__file__)
                with open(path.join(self.dir, HS_FILE), 'w') as f:
                        #try and except runs some code and if an error becomes present it runs some other code to run
                        try:
                                self.highscore = int(f.read())
                        except:
                                self.highscore = 0
                                


        def new(self):
                # Sets the score at the start and defines the players and platforns importing their classes
                #from the sprite file.
                self.score = 0 
                self.all_sprites = pygame.sprite.Group()
                self.platforms = pygame.sprite.Group()
                self.player = Player(self,Purple,30,40,30)
                self.all_sprites.add(self.player)
                for plat in PLATFORM_LIST:
                        p = Platform(*plat)
                        self.all_sprites.add(p)
                        self.platforms.add(p)
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
                #Updates including when the player collides with a platform etc
                 self.all_sprites.update()
                 if self.player.vel.y > 0:
                         hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
                         if hits:
                                self.player.pos.y = hits[0].rect.top
                                self.player.vel.y = 0

                # if the player reaches the top 1/4 of the screen platforms start to disappear and points can be
                # gained this way
                 if self.player.rect.top <= HEIGHT / 4:
                         self.player.pos.y += abs(self.player.vel.y)
                         for plat in self.platforms:
                                 plat.rect.y += abs(self.player.vel.y)
                                 if plat.rect.top >= HEIGHT:
                                         plat.kill()
                                         self.score += 10


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
                         p = Platform(random.randrange(0, WIDTH - width),
                                              random.randrange(-75, - 30),
                                              width, 25)
                         self.platforms.add(p)
                         self.all_sprites.add(p)
                         
               
               

        def events(self):
                #Game loop - events
                 for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                if self.playing:
                                        self.playing = False
                                self.running = False
                        if event.type ==pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                        self.player.jump()
               

        def draw(self):
                #Game loop - draw
                self. screen.fill(Ivory)
                self.all_sprites.draw(self.screen)
                self.draw_text(str(self.score), 22, Black, WIDTH / 2, 15)

                pygame.display.flip()
                
               
        def show_start_screen(self):
                self.screen.fill(Ivory)
                self.draw_text(TITLE, 48, Black, WIDTH / 2, HEIGHT / 4)
                self.draw_text("Arrows to move, Space to jump", 22, Black, WIDTH / 2, HEIGHT / 2)
                self.draw_text("Press a key to play", 22, Black, WIDTH / 2, HEIGHT * 3/4)
                self.draw_text("High Score: " + str(self.highscore, 22, Black, WIDTH / 2, 15))
                pygame.display.flip()
                self.wait_for_key()
                
                
                

        def show_go_screen(self):
                 if not self.running:
                         return
                 self.screen.fill(Ivory)
                 self.draw_text("Game Over", 48, Black, WIDTH / 2, HEIGHT / 4)
                 self.draw_text("Score: " + str(self.score), 22, Black, WIDTH / 2, HEIGHT / 2)
                 self.draw_text("Press a key to play again", 22, Black, WIDTH / 2, HEIGHT * 3/4)
                 if self.score > self.highscore:
                         self.highscore. self.score
                         self.draw_text("NEW HIGH SCORE!", 22, Black, WIDTH / 2, HEIGHT / 2 + 40)
                         with open(path.join(self.dir, HS_FILE), 'w') as f:
                                 f.write(str(self.score))
                 else:
                        self.draw_text("High Score: " + str(self.highscore, 22, Black, WIDTH / 2, HEIGHT / 2 + 40))
                   
                 pygame.display.flip()
                 self.wait_for_key()
                 
                 

        def wait_for_key(self):
                 waiting = True
                 while waiting:
                         self.clock.tick(FPS)
                         for event in pygame.event.get():
                                 if event.type == pygame.QUIT:
                                         waiting = False
                                         self.running = False
                                 if event.type == pygame.KEYUP:
                                          waiting = False

        def draw_text(self, text, size, color, x, y):
                 font = pygame.font.Font(self.font_name, size)
                 text_surface = font.render(text, True, color)
                 text_rect = text_surface.get_rect()
                 text_rect.midtop = (x, y)
                 self.screen.blit(text_surface, text_rect)
                 



g = Game()
g.show_start_screen()
while g.running:
        g.new()
        g.show_go_screen()

pygame.quit()




                        


       

