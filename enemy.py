import pygame
import app
import math
import random
class Enemy:
    def __init__(self, x, y, enemy_type, enemy_assets, speed=app.DEFAULT_ENEMY_SPEED):
        self.x = x
        self.y = y
        self.speed = speed


        self.type = enemy_type
        self.speed = random.randint(1, 3) #adds speed
        max_hp = 1 #random.randint(1, 3) #differenciates the hp for enemies
        self.max_hp = max_hp
        self.hp = self.max_hp

        self.frames = enemy_assets[enemy_type]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.enemy_type = enemy_type 
        self.facing_left = False

        self.current_frame = 0
        self.frame_delay = 100 
        self.last_update = pygame.time.get_ticks()
        
        self.knockback_dist_remaining = 0
        self.knockback_dx = 0
        self.knockback_dy = 0
       

    def update(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        if self.knockback_dist_remaining > 0:
            self.apply_knockback()
        else:
            self.move_toward_player(player)
            self.animate()
   
    def move_toward_player(self, player):
        #Calculates direction vector toward player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        
        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        
        # Update enemy position
        self.facing_left = dx < 0
        

        self.rect.center = (self.x, self.y)
        

    def apply_knockback(self):
        step = min(app.ENEMY_KNOCKBACK_SPEED, self.knockback_dist_remaining)
        self.knockback_dist_remaining -= step

        self.x += self.knockback_dx * step
        self.y += self.knockback_dy * step

        if self.knockback_dx < 0:
            self.facing_left = True
        else:
            self.facing_left = False

        self.rect.center = (self.x, self.y)

        

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = center
        

    def draw(self, surface):
        frame = self.frames[self.current_frame]
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
     

  
    def set_knockback(self, px, py, dist):
        dx = self.x - px
        dy = self.y - py
        length = math.sqrt(dx*dx + dy*dy)
        if length != 0:
            self.knockback_dx = dx / length
            self.knockback_dy = dy / length
            self.knockback_dist_remaining = dist

    def draw_health_bar(self, surface):
        # Calculate dimensions
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.hp / self.max_hp
        health_bar_width = int(bar_width * health_ratio)

        # Define colors
        bar_background_color = (255, 0, 0)  # Red for the background
        bar_foreground_color = (0, 255, 0)  # Green for the current health

        # Draw the health bar background
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 1  # Position above the enemy
        pygame.draw.rect(surface, bar_background_color, (bar_x, bar_y, bar_width, bar_height))

        # Draw the current health bar
        pygame.draw.rect(surface, bar_foreground_color, (bar_x, bar_y, health_bar_width, bar_height))
    def max_hp(self):
        self.max_hp = random.randint(1,3)
        self.hp = self.max_hp
    def handle_event(self):
            self.max_hp += 2
            self.hp = self.max_hp
