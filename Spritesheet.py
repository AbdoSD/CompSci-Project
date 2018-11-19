 img_dir = path.join(self.dir, 'img')
  self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
SPRITESHEET = "spritesheet_jumper.png"

class Spritesheet:
        #utitlity class for loading and posting spriesheets
        def _init__(self, filename):
                self.spritehseet = pg.image.load(filename).convert()

        def get_image(self, x, y, width, height):
                #grab an image out of a larger spritesheet
                image = pg.Surface((width, height))
                image.blit(self.spritesheet, (0, 0), (x, y, width, height))
                return image


