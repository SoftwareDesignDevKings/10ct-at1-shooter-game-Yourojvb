import app
import sys
from player import Player

class Level_up:
    def __init__(self,player,):
        self.player = player
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 1
    
    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level_up()
            self.level_up_menu()
            return
        
        #xp_text_surf = self.font_small.render(f"Leveled up! New level: {self.level}, True, (200, 200, 200))
    #level_up_surf = Button(300, 250, 200, 50, "Increase bullet count", player.level_up)

    def level_up(self):
        selecting = True
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.health += 1
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        player.bullet_count += 1
                        selecting = False

    def level_up_menu(prompt_surf,self,screen):
        if level_up_menu == True:
            while True:
                overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))
                level_up_surf = self.font_large.render("You leveled up!", True , (300,0,0))
                level_up_surf = self.font_small.render("Press either 1, 2 or 3", True , (250,0,0))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            Player.bullet_size + 1
                            in_level_up_menu = False
                        elif event.key == pygame.K_2:
                            Player.bullet_speed + 1
                            in_level_up_menu = False
