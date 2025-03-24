import pygame
import app 
import math 
from bullet import Bullet
import sys

class Player:
    def __init__(self, x, y, assets, shoot_delay):
        self.x = x
        self.y = y

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 2 #threshold to level up
        self.shoot_delay = shoot_delay

        self.speed = app.PLAYER_SPEED
        self.animations = assets["player"]
        self.state = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.facing_left = False

        self.health = 5
        self.level_up = False #the key for the level up system to appear

        self.bullet_speed = 10
        self.bullet_damage = 1
        self.bullet_size = 10
        self.bullet_count = 1
        self.shoot_cooldown = 20
        self.shoot_timer = 0
        self.bullets = []

        self.font_small = pygame.font.Font(None, 36) #Used to render in the words on the screen
        self.font_large = pygame.font.Font(None, 50)
       
        self.xp_to_next_level = 2


    
    def handle_input(self):
        keys = pygame.key.get_pressed()

        vel_x, vel_y = 0, 0
 
       
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vel_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vel_y += self.speed

        self.x += vel_x
        self.y += vel_y


        self.x = max(0, min(self.x, app.WIDTH))
        self.y = max(0, min(self.y, app.HEIGHT))
        self.rect.center = (self.x, self.y)

       
        if vel_x != 0 or vel_y != 0:
            self.state = "run"
        else:
            self.state = "idle"

        if vel_x < 0:
            self.facing_left = True
        elif vel_x > 0:
            self.facing_left = False  

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.y < 0 or bullet.y > app.HEIGHT or bullet.x < 0 or bullet.x > app.WIDTH:
                self.bullets.remove(bullet) # this deals with bullets flying off the screen to not use use space.

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self.animations[self.state]
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

    def draw(self, surface):
        if self.facing_left:
                flipped_img = pygame.transform.flip(self.image, True, False)
                surface.blit(flipped_img, self.rect)
        else:
                surface.blit(self.image, self.rect)

        for bullet in self.bullets:
            bullet.draw(surface)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
    
    def shoot_toward_position(self, tx, ty):
        if self.shoot_timer >= self.shoot_cooldown: #so there is an interval of firing
            return

        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return

        vx = (dx / dist) * self.bullet_speed
        vy = (dy / dist) * self.bullet_speed

        angle_spread = 5
        base_angle = math.atan2(vy, vx)
        mid = (self.bullet_count - 1) / 2

        for i in range(self.bullet_count):
            offset = i - mid
            spread_radians = math.radians(angle_spread * offset)
            angle = base_angle + spread_radians

            final_vx = math.cos(angle) * self.bullet_speed
            final_vy = math.sin(angle) * self.bullet_speed

            bullet = Bullet(self.x, self.y, final_vx, final_vy, self.bullet_size)
            self.bullets.append(bullet)
        self.shoot_timer = 0

    def shoot_toward_mouse(self, pos):
        mx, my = pos 
        self.shoot_toward_position(mx, my)

    def shoot_toward_enemy(self, enemy):
        self.shoot_toward_position(enemy.x, enemy.y)
    
    def check_level_up_menu(self, screen): # to define what is the system is updating
        if self.xp >= self.xp_to_next_level:
            self.level_up = True
            self.level_up_menu(screen)
            
    
    def level_up_menu(self, screen):
        if self.level_up:
            overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA) #sets within the whole screen
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            level_up_surf = self.font_large.render("You leveled up!", True, (200, 100, 00)) #the apperence of the level up
            screen.blit(level_up_surf, (app.WIDTH // 2 - level_up_surf.get_width() // 2, 100))

            options = [ #these are the things that are going to pop up
            "Press either 1, 2 or 3",
            "1. Increase bullet count",

            "2. Increase bullet size",

            "3. Increase bullet speed",

            "4.Increase Bullet damage by 1",

            "5. Decrease Bullet delay",

            "6. Increase Health",


        ]
            for i, option in enumerate(options):
                level_up_surf = self.font_small.render(option, True, (100, 240, 20)) #colour and size
                screen.blit(level_up_surf, (app.WIDTH // 2 - level_up_surf.get_width() // 2, 200 + i * 30)) #covering the whole screen
#able to stop game so player can choose
                pygame.display.update()

            choosing = True
            while choosing:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1: #if 1 is pressed and so on
                            self.bullet_count += 1
                            choosing = False # unpauses the game
                        elif event.key == pygame.K_2:
                            self.bullet_size += 1
                            choosing = False
                        elif event.key == pygame.K_3:
                            self.bullet_speed += 1
                            choosing = False
                        elif event.key == pygame.K_4:
                            self.bullet_damage += 1
                            choosing = False
                        elif event.key == pygame.K_5:
                            self.shoot_delay -= 10
                            choosing = False
                        elif event.key == pygame.K_6:
                            self.health += 1
                            choosing = False
                
                pygame.display.update()

        
            self.level_up = False #stops the process
            self.xp -= self.xp_to_next_level # resets the xp back to 0
            self.level += 1 #shows the player where they are at
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5) #increase difficutly in reaching level

   
        

