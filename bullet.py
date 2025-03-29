import app

class Bullet:
    def __init__(self, x, y, vx, vy, size): #determines the instance variables/attributes
        self.x = x #assigns according variables
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size

        self.image = app.pygame.Surface((self.size, self.size), app.pygame.SRCALPHA)
        self.image.fill((255, 255, 255))#the white colour
        self.rect = self.image.get_rect(center=(self.x, self.y)) #where bullet is 
        #posioned and placed on the grid of the game
        
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        
    
    def draw(self, surface):
        surface.blit(self.image, self.rect) #summons onto the screen
