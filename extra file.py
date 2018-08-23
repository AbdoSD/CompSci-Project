  self.pos = vec(WIDTH / 2, HEIGHT / 2)
           self.vel = vec(0,0)
                 self.acc = vec(0,0)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.acc.y = -0.5
                if keys[pygame.K_DOWN]:
                    self.acc.y = 0.5

                
                self.vel += self.acc
                self.pos += self.vel + 0.5 * self.acc

                self.rect.center = self.pos
