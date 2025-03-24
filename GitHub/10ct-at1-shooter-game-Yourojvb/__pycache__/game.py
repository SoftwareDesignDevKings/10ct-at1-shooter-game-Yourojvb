# game.py
import pygame
import random
import os

import app
from player import Player
from enemy import Enemy
import math
from coin import Coin


class Game:
    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((app.WIDTH, app.HEIGHT))
        pygame.display.set_caption("Dungeon")
        self.clock = pygame.time.Clock()
       
        self.assets = app.load_assets()

        font_path = os.path.join("assets", "PressStart2P.ttf")
        self.font_small = pygame.font.Font(font_path , 18)
        self.font_large = pygame.font.Font(font_path , 32)

        self.space_held = False 

        pygame.mixer.init()
  
        soundtrack_path = os.path.join("assets", "doom.mp3" ) # Replace with your actual file path
        pygame.mixer.music.load(soundtrack_path) #play music
        pygame.mixer.music.play(-1)  
        pygame.mixer.music.set_volume(0.5)
        


        self.xp_to_next_level = 3
        self.level_up_menu = False
        self.last_shot_time = 0 
        self.shoot_delay = 500 # for auto shooting
        
        self.player = Player(x=100, y=100, assets= self.assets, shoot_delay = self.shoot_delay)

        self.checkpoint = 5 # Increase difficulty every 5 levels
        #self.xp = 0


        self.background = self.create_random_background(
        app.WIDTH, app.HEIGHT, self.assets["floor_tiles"]
    )
        self.running = True
        self.game_over = False

        self.coins = []

        self.enemies = []
        self.enemy_spawn_timer = 1
        self.enemy_spawn_interval = 60
        self.enemies_per_spawn = 1

        self.reset_game()


    def reset_game(self):
        self.player = Player(app.WIDTH // 2, app.HEIGHT // 2, self.assets, shoot_delay=self.shoot_delay)
        self.enemies = []
        self.enemy_spawn_timer = 60
        self.enemies_per_spawn = 1
        self.coins = []
        self.player.checkpoint = 2
        
        self.bullet_speed = 10
        self.bullet_size = 10
        self.bullet_count = 1

        self.game_over = False
        self.level_up_menu = False
        self.space_held = False

        soundtrack_path = os.path.join("assets", "doom.mp3" ) 
        pygame.mixer.music.load(soundtrack_path)
        pygame.mixer.music.play(-1)  
        pygame.mixer.music.set_volume(0.5)
        

    def create_random_background(self, width, height, floor_tiles):
        bg = pygame.Surface((width, height))
        tile_w = floor_tiles[0].get_width()
        tile_h = floor_tiles[0].get_height()

        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                bg.blit(tile, (x, y))

        return bg
    
    def run(self):
        while self.running:
            self.clock.tick(app.FPS)
            self.handle_events()

            if not self.game_over:
                self.update()

            self.draw()

        pygame.quit()
  

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    if event.key == pygame.K_SPACE:
                        nearest_enemy = self.find_nearest_enemy()
                        if nearest_enemy:
                            self.player.shoot_toward_enemy(nearest_enemy)
                        if not self.space_held:  # Start tracking when the space key is held
                            self.space_held = True
                            self.space_held_start_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_held = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    self.player.shoot_toward_mouse(event.pos)
                
            
    
    def update(self):
        self.player.handle_input()
        self.player.update()

        for enemy in self.enemies:
            enemy.update(self.player)
        
          

        self.check_player_enemy_collisions()
        self.check_bullet_enemy_collisions()
        self.check_player_coin_collisions()
        self.increase_difficulty()
        #self.check_shoot_delay()
        current_time = pygame.time.get_ticks()
        if self.space_held and current_time - self.space_held_start_time >= self.shoot_delay:
            if current_time - self.last_shot_time >= self.shoot_delay:
                nearest_enemy = self.find_nearest_enemy()
                if nearest_enemy:
                    self.player.shoot_toward_enemy(nearest_enemy)
                self.last_shot_time = current_time
                

        if self.player.health <= 0:
            self.game_over = True
        
        self.spawn_enemies()
        self.player.check_level_up_menu(self.screen)
         
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for coin in self.coins:
            coin.draw(self.screen)

        if not self.game_over:
            self.player.draw(self.screen) 

        for enemy in self.enemies:
            enemy.draw(self.screen)
    
        hp = max(0, min(self.player.health, 5))
        health_img = self.assets["health"][hp]
        self.screen.blit(health_img, (10, 10))

        xp_text_surf = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
        self.screen.blit(xp_text_surf, (10, 70)) #blit to summon it onto the screen

        level_up_surf = self.font_small.render(f"Lvl: {self.player.level}", True , (200, 100, 50))
        self.screen.blit(level_up_surf, (10, 50))

        level_up_rect = self.font_small.render(f"Req Lvl: {self.player.xp_to_next_level}", True, (50, 100,150))
        self.screen.blit(level_up_rect, (10, 90))

        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)  # Draw health bar for each enemy
        

        if self.game_over:
            self.draw_game_over_screen()
            #soundtrack_path1 = os.path.join("undertale.mp3")
            #pygame.mixer.music.stop()  # Stop the current music
            #pygame.mixer.music.load("undertale.mp3")  # Load a new track
            #pygame.mixer.music.play(-1)

        pygame.display.flip()
       
    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 1

            for _ in range(self.enemies_per_spawn):
                side = random.choice(["top", "bottom", "left", "right"])
                if side == "top":
                    x = random.randint(0, app.WIDTH)
                    y = -app.SPAWN_MARGIN
                elif side == "bottom":
                    x = random.randint(0, app.WIDTH)
                    y = app.HEIGHT + app.SPAWN_MARGIN
                elif side == "left":
                    x = -app.SPAWN_MARGIN
                    y = random.randint(0, app.HEIGHT)
                else:
                    x = app.WIDTH + app.SPAWN_MARGIN
                    y = random.randint(0, app.HEIGHT)

                enemy_type = random.choice(list(self.assets["enemies"].keys()))
                enemy = Enemy(x, y, enemy_type, self.assets["enemies"])
            
                self.enemies.append(enemy)

    def check_player_enemy_collisions(self):
        collided = False
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                collided = True
                break

        if collided:
            self.player.take_damage(1)
            px, py = self.player.x, self.player.y
            for enemy in self.enemies:
                enemy.set_knockback(px, py, app.PUSHBACK_DISTANCE)
    
    def draw_game_over_screen(self):
        
        # Dark overlay
        overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_surf = self.font_large.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)

        # Prompt to restart or quit
        prompt_surf = self.font_small.render("Press R to Play Again or ESC to Quit", True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 + 20))
        self.screen.blit(prompt_surf, prompt_rect)
        
    
    def find_nearest_enemy(self):
        if not self.enemies:
            return None
        nearest = None
        min_dist = float('inf')
        px, py = self.player.x, self.player.y
        for enemy in self.enemies:
            dist = math.sqrt((enemy.x - px)**2 + (enemy.y - py)**2)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest

        
    def check_bullet_enemy_collisions(self):
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hp -= self.player.bullet_damage  # Decrease enemy's health
                    if enemy.hp <= 0:  # Remove enemy if health is zero
                        self.enemies.remove(enemy)
                        new_coin = Coin(enemy.x, enemy.y)
                        self.coins.append(new_coin)
                    if bullet in self.player.bullets:  # Remove bullet after collision
                        self.player.bullets.remove(bullet)
                        
                   
                   
        
    def check_player_coin_collisions(self):
        coins_collected = []
        for coin in self.coins:
            if coin.rect.colliderect(self.player.rect):
                coins_collected.append(coin)
                self.player.xp += 1

        for c in coins_collected:
            if c in self.coins:
                self.coins.remove(c) 
    
    def increase_difficulty(self):
        if self.player.level == self.checkpoint: # if level reaches threshold
            self.enemies_per_spawn += 1
            self.checkpoint += 3
            self.enemy_spawn_interval = max(1, self.enemy_spawn_interval - 1)
            enemy._max_hp += 1  # Increase max_hp for existing enemies
            enemy_hp = enemy.max_hp
                

            
        