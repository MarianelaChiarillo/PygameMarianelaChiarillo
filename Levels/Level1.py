import pygame, sys
from pygame.locals import *
from settings import *
from Characters import Player
from class_platform import Platform
from class_sprite import FireSprite
from class_enemy import EnemyBird
from shoots import *
from class_item import SurvivalKit, Hearts, Stars
import json



class LevelOne:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SpaceLost")
        self.icon = pygame.transform.scale(pygame.image.load(ICONMENU_BACKGROUND).convert_alpha(), SIZE_ICON)
        pygame.display.set_icon(self.icon)
        self.background = pygame.image.load(LEVEL1_BACKGROUND).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.sound_colision_bird = pygame.mixer.Sound("assets/sounds/colorado-bird-crow-03.wav")
        self.sound_fire = pygame.mixer.Sound("assets/sounds/shoot/FIREIGNITELRG.WAV")
        self.sound_item = pygame.mixer.Sound("assets/sounds/Dixie Hurt.WAV")
        self.sound_goodbye = pygame.mixer.Sound("assets/sounds/voices/playerdead.OGG")
        self.volume_level = 0.5  # Valor inicial del volumen
        self.platform_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.player = Player()
        self.enemy = EnemyBird(self.player.rect, x=0, y=200)
        self.shoots_group = pygame.sprite.Group()
        self.survival_kits_group = pygame.sprite.Group()
        self.hearts_group = pygame.sprite.Group()
        self.stars_group = pygame.sprite.Group()
        self.lives = 3
        self.lives_im = pygame.transform.scale(pygame.image.load(LIVES_ITEM).convert_alpha(), (20, 20))
        self.game_over = False
        self.enemy_collisions = 0
        self.time_accumulator = 0  # Acumulador de tiempo
        self.score = 0
        self.game_data_file = "game1_data.json"
        


      
        self.platform_coordinates = [(0, 600), (80, 600), (180, 340), (250, 340), (570, 430), (500, 430), (300, 200),
                                     (300, 550), (600, 600), (650, 600), (790, 380), (610, 220), (800, 80), (870, 80),
                                     (80, 150), (470, 80), (400, 80)]

        for coord in self.platform_coordinates:
            x, y = coord
            platform = Platform(x, y, SKY_PLATFORM)
            self.platform_group.add(platform)

        self.player.rect.x = 0
        self.player.rect.y = 600

        self.fire_sprites = pygame.sprite.Group()
        x = 0
        fire_width = FireSprite().rect.width
        for _ in range(WIDTH // fire_width):
            fire_sprite = FireSprite()
            fire_sprite.rect.left = x
            self.fire_sprites.add(fire_sprite)
            x += fire_width
    
        positions = [(300, 500), (300, 700), (500, 300), (600, 100), (500, 300), (700, 300), (300, 500), (100, 600)]
        for position in positions:
            enemy = EnemyBird(self.player.rect, x=position[0], y=position[1])
            self.enemies_group.add(enemy)
           
        self.generate_survival_kits()

    def generate_survival_kits(self):
        platform_positions = [(560, 410), (370, 180), (670, 580), (660, 170), (20, 170), (470, 40)]
        for x, y in platform_positions:
            survival_kit = SurvivalKit(x, y)
            self.survival_kits_group.add(survival_kit)

        self.generate_hearts()

    def generate_hearts(self):
        platform_positions = [(150, 270), (350, 470), (720, 380)]

        for x, y in platform_positions:
            hearts = Hearts(x, y)
            self.hearts_group.add(hearts)

        self.generate_stars()

    def generate_stars(self):
        platform_positions = [(850, 40), (890, 40), (870, 20)]

        for x, y in platform_positions:
            stars_t = Stars(x, y)
            self.stars_group.add(stars_t)

    def subtract_life(self):
        self.lives -= 1

        if self.lives <= 0:
            self.game_over = True

        self.player.rect.x = 0
        self.player.rect.y = 600
        self.sound_colision_bird.play()  # Reproducir sound de colisión

    def restore_life(self):
        self.lives += 1

    def get_lives(self):
        return self.lives

    def draw_lives(self, screen):
        live_x = 10
        live_y = 10

        for _ in range(self.lives):
            screen.blit(self.lives_im, (live_x, live_y))
            live_x += 13 + 13

    def handle_shoot_hit(self, shoot):
        # Verificar colisiones entre disparos y enemigos
        pygame.sprite.groupcollide(self.shoots_group, self.enemies_group, True, True)
    
    def save_game_data1(self, game_data):
        try:
            with open(self.game_data_file, "r") as file:
                all_data = json.load(file)
        except FileNotFoundError:
            all_data = []

        all_data.append(game_data)

        with open(self.game_data_file, "w") as file:
            json.dump(all_data, file)

#-------------------------------------------------------------------------------------------------------------------------------------
    
    def run(self):
        while not self.game_over:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if pygame.sprite.spritecollide(self.player, self.fire_sprites, False):
                self.game_over = True
                self.sound_fire.play()
                
            self.player.update()
            self.player.handle_move()
            self.player.shoots_group.update()

            on_platform = False
            for platform in self.platform_group:
                if self.player.rect.colliderect(platform.rect):
                    if self.player.rect.bottom > platform.rect.top and self.player.rect.top < platform.rect.centery:
                        self.player.rect.bottom = platform.rect.top
                        self.player.jumping = False
                        on_platform = True
                    elif self.player.rect.top < platform.rect.bottom and self.player.rect.bottom > platform.rect.centery:
                        self.player.rect.top = platform.rect.bottom
                        self.player.jumping = True
                        on_platform = True
                    break

            if not on_platform:
                self.player.jumping = True

            self.screen.blit(self.background, ORIGIN)
            self.platform_group.draw(self.screen)
            self.fire_sprites.draw(self.screen)
            self.enemy.check_player_distance()
            self.enemy.update()
            self.enemies_group.update()
            self.enemies_group.draw(self.screen)
            self.shoots_group.update()
            self.player.shoots_group.draw(self.screen)
            self.survival_kits_group.update(self.player)
            self.survival_kits_group.draw(self.screen)
            self.hearts_group.update(self.player)
            self.hearts_group.draw(self.screen)
            self.stars_group.update(self.player)
            self.stars_group.draw(self.screen)
            self.draw_lives(self.screen)
            self.player.draw(self.screen)


            for shoot in self.player.shoots_group:
                enemy_hit_list = pygame.sprite.spritecollide(shoot, self.enemies_group, True)
                if enemy_hit_list:
                    self.shoots_group.remove(shoot)

            if pygame.sprite.spritecollide(self.player, self.enemies_group, False):
                self.enemy_collisions += 1
                if self.enemy_collisions >= 1:
                    self.subtract_life()
                    self.enemy_collisions = 0
                else:
                    self.player.rect.x = 0
                    self.player.rect.y = 600
                    self.sound_colision_bird.p()

            if pygame.sprite.spritecollide(self.player, self.hearts_group, True):
                self.restore_life()
                self.time_accumulator += 10
                self.sound_item.play()


            score_increment = 0  # Variable para almacenar el incremento de puntaje

            # Check collision 
            survival_kit_collisions = pygame.sprite.spritecollide(self.player, self.survival_kits_group, True)
            score_increment = len(survival_kit_collisions) * 100  # Aumentar el puntaje según la cantidad de kits recolectados
            self.score += score_increment
            if score_increment > 0:
                self.sound_item.play()
          
            self.time_accumulator += 1
            
            font = pygame.font.Font(SPACEMAN, 15)
            time_text = font.render("Time: " + str(self.time_accumulator), True, WHITE)
            self.screen.blit(time_text, (130, 10))

            score_text = font.render("Score: " + str(self.score), True, WHITE)
            self.screen.blit(score_text, (10, 40))

            if pygame.sprite.spritecollide(self.player, self.stars_group, False):
                self.game_over = True
                self.sound_item.play()
                self.screen.fill(BLACK)  
                
                # Mostrar mensaje de victoria
                font = pygame.font.Font("assets/fonts/SPACE.TTF", 50)
                victory_text = font.render("Congratulations", True, WHITE)
                self.screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))

                # Mostrar puntaje acumulado
                score_text = font.render("Score: " + str(self.score), True, WHITE)
                self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + score_text.get_height()))

            pygame.display.flip()

            if self.game_over:
                self.screen.fill(BLACK)  # Limpiar la pantalla
                font = pygame.font.Font("assets/fonts/SPACE.TTF", 50)
                game_over_text = font.render("END GAME", True, WHITE)
                game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 400))
                self.screen.blit(game_over_text, game_over_rect)
                self.sound_goodbye.play()

                game_data1 = {
                    "score": self.score,
                    "time": self.time_accumulator
                }
                self.save_game_data1(game_data1)

        pygame.time.wait(2000)
       
       
