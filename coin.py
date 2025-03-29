import app

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = app.pygame.Surface((15, 15), app.pygame.SRCALPHA) #Creates the box coin
        self.image.fill((255, 215, 0)) #colours in the coin
        self.rect = self.image.get_rect(center=(self.x, self.y)) # places the coin in 
        #the exact coordinates

    def draw(self, surface):
        surface.blit(self.image, self.rect) #summons the coin visually into the game

      