import pygame, sys
import time
from pygame.locals import *
from settings import *
from Characters import Player
from class_platform import Platform
from shoots import *
from class_sprite import Blue
from class_enemy import BotEnemy
from class_item import SurvivalKit, Hearts, Moon
import json


class LevelTwo():
    def __init__(self):
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SpaceLost")
        self.icon = pygame.transform.scale(pygame.image.load(ICONMENU_BACKGROUND).convert_alpha(), SIZE_ICON)
        pygame.display.set_icon(self.icon)
        self.background = pygame.image.load(LEVEL2_BACKGROUND).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.platform_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.shoots_group = pygame.sprite.Group()  # Grupo de disparos
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.survival_kits_group = pygame.sprite.Group()  # Grupo de kits de supervivencia
        self.hearts_group = pygame.sprite.Group()
        self.moon_group = pygame.sprite.Group()
        self.lives = 3
        self.lives_im = pygame.transform.scale(pygame.image.load(LIVES_ITEM).convert_alpha(), (20, 20))
        self.game_over = False
        self.enemy_collisions = 0
        self.time_accumulator = 0  # Acumulador de tiempo
        self.score = 0
        self.sound_colision_bot = pygame.mixer.Sound("assets/sounds/shoot/botpunch.wav")
        self.sound_ground = pygame.mixer.Sound("assets/sounds/shoot/MIX_CAD_BANE_EXPLOSION_ASHES.wav")
        self.sound_item = pygame.mixer.Sound("assets/sounds/Dixie Hurt.WAV")
        self.sound_fire_bot =  pygame.mixer.Sound("assets/sounds/shoot/BoomerExplosionDistant03_2.ogg")
        self.sound_goodbye = pygame.mixer.Sound("assets/sounds/voices/playerdead.OGG")
        self.game_data2_file = "game_data2.json" 
      

        # Crear una lista de coordenadas de plataformas
        platform_coordinates = [(850, 620), (650, 550), (450, 620), (200, 600), (50, 480), (280, 400), (500, 420), (800, 360), (700, 360), (100, 600), (20, 100), (200, 150), (280,150), (500, 100), (850, 130), (550, 220), (450, 220), (750, 130), (20, 350)]

        for coord in platform_coordinates:
            x, y = coord
            platform = Platform(x, y, TWO_PLATFORM)
            self.platform_group.add(platform)
        
        self.player.rect.x = 850  # Ajustar la posición inicial en el borde izquierdo
        self.player.rect.y = 620  # Ajustar la posición inicial en la esquina inferior izquierda

        self.blue = pygame.sprite.Group() 
        x = 0  # Variable para controlar la posición horizontal de los sprites azules
        blue_w = Blue().rect.width  # Ancho de los sprites azules
        for _ in range(WIDTH // blue_w):  # Crear sprites a lo largo de la pantalla
            blue_sprite = Blue()  # Crear una instancia de la clase Blue
            blue_sprite.rect.left = x
            self.blue.add(blue_sprite)  # Agregar la instancia al grupo
            x += blue_w
    
        positions = [(300, 550), (700, 330), (750, 80), (380, 60), (100, 280)]
        for position in positions:
            enemy = BotEnemy(self.player.rect, x=position[0], y=position[1], platform_group=self.platform_group)
            self.enemies_group.add(enemy)

        self.generate_survival_kits()
    def generate_survival_kits(self):
        platform_positions = [  (200, 580), (430, 340), (750, 320), (260, 120),  (520, 180), (790, 100), (100, 300)]
        for x, y in platform_positions:
            survival_kit = SurvivalKit(x, y)
            self.survival_kits_group.add(survival_kit)
        
        self.generate_hearts()
    def generate_hearts(self):
        platform_positions = [(150, 270), (350, 470), (720, 380), (600, 100)]

        for x, y in platform_positions:
            hearts = Hearts(x, y)
            self.hearts_group.add(hearts)

        self.generate_moons()
    def generate_moons(self):
        platform_positions = [(40, 60), (80, 60), (60, 40)]

        for x, y in platform_positions:
            Moon_t = Moon(x, y)
            self.moon_group.add(Moon_t)

    def subtract_life(self):
        self.lives -= 1

        if self.lives <= 0:
            self.game_over = True

        self.player.rect.x = 850
        self.player.rect.y = 620
        self.sound_colision_bot.play()

    def restore_life(self):
        self.lives += 1

    def get_lives(self):
        return self.lives

    def draw_lives(self, screen):
        live_x = 880
        live_y = 10

        for _ in range(self.lives):
            screen.blit(self.lives_im, (live_x, live_y))
            live_x += 13 + 13

    def handle_shoot_hit(self, shoot):
        # Verificar colisiones entre disparos y enemigos
        pygame.sprite.groupcollide(self.shoots_group, self.enemies_group, True, True)
    
    def save_game_data2(self, game_data2):
        try:
            with open(self.game_data2_file, "r") as file:
                all_data = json.load(file)
        except FileNotFoundError:
            all_data = []

        all_data.append(game_data2)

        with open(self.game_data2_file, "w") as file:
            json.dump(all_data, file)

 #-------------------------------------------------------------------------------------------------------------------------------------

    def run(self):
        self.start_time = time.time()
        while not self.game_over:
            self.clock.tick(FPS)
            current_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            self.player.update()  # Actualizar el jugador
            self.player.handle_move()
            self.player.shoots_group.update()

            self.screen.blit(self.background, ORIGIN)
            self.platform_group.update()
            self.platform_group.draw(self.screen)
            # Verificar si el jugador está colisionando con alguna plataforma
            on_platform = False
            for platform in self.platform_group:
                if self.player.rect.colliderect(platform.rect):
                    # Verificar si el jugador está por encima de la plataforma
                    if self.player.rect.bottom > platform.rect.top and self.player.rect.top < platform.rect.centery:
                        # El jugador está colisionando con la plataforma desde arriba
                        self.player.rect.bottom = platform.rect.top
                        self.player.jumping = False
                        on_platform = True
                    elif self.player.rect.top < platform.rect.bottom and self.player.rect.bottom > platform.rect.centery:
                        # El jugador está colisionando con la plataforma desde abajo
                        self.player.rect.top = platform.rect.bottom
                        self.player.jumping = True
                        on_platform = True
                    break

            if not on_platform:
                self.player.jumping = True

            self.screen.blit(self.background, ORIGIN)
            self.platform_group.update()
            self.platform_group.draw(self.screen)


            self.blue.update()
            self.blue.draw(self.screen)
            self.enemies_group.update()
            self.enemies_group.draw(self.screen)
            self.shoots_group.update()  # Actualizar disparos
            self.player.shoots_group.draw(self.screen)  # Dibujar los disparos
            self.survival_kits_group.update(self.player)
            self.survival_kits_group.draw(self.screen)  # Dibujar los kits de supervivencia
            self.hearts_group.update(self.player) # Actualizar
            self.hearts_group.draw(self.screen)
            self.moon_group.update(self.player) # Actualizar
            self.moon_group.draw(self.screen)
            self.draw_lives(self.screen)
            self.player.draw(self.screen)  # Agregar esta línea

            if pygame.sprite.spritecollide(self.player, self.moon_group, False):
                self.game_over = True
                self.sound_item.play()
                self.screen.fill(BLACK)  # Clear the screen

                # Mostrar mensaje de victoria
                font = pygame.font.Font(SPACE, 50)
                victory_text = font.render("Congratulations", True, WHITE)
                self.screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))

                # Mostrar puntaje acumulado
                score_text = font.render("Score: " + str(self.score), True, WHITE)
                self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + score_text.get_height()))


            if pygame.sprite.spritecollide(self.player, self.blue, False):
                self.game_over = True
                self.sound_ground.play()

            if pygame.sprite.spritecollide(self.player, self.all_sprites,  False):
                self.subtract_life
                self.sound_fire_bot.play()
            

            if current_time - self.start_time > 10:
                for enemy in BotEnemy.enemiesBot:
                    enemy.update()
                for bullet in BotEnemy.enemiesBot :
                    bullet.update()
                self.all_sprites.add(BotEnemy.enemiesBot)


                self.all_sprites.draw(self.screen)
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
                    self.sound_colision_bot.play()

            if pygame.sprite.spritecollide(self.player, self.hearts_group, True):
                self.restore_life()
                self.time_accumulator += 10  # Suma 10 al tiempo acumulador al recoger un corazón

            self.time_accumulator += 1  # Incrementa el tiempo acumulador en 1 en cada iteración

            score_increment = 0  # Variable para almacenar el incremento de puntaje

            # Check collision with survival kits
            survival_kit_collisions = pygame.sprite.spritecollide(self.player, self.survival_kits_group, True)
            score_increment = len(survival_kit_collisions) * 100  # Aumentar el puntaje según la cantidad de kits recolectados
            self.score += score_increment
            if score_increment > 0:
                self.sound_item.play()

            # Muestra el tiempo en pantalla
            font = pygame.font.Font(SPACEMAN, 18)
            time_text = font.render("Time: " + str(self.time_accumulator), True, WHITE)
            self.screen.blit(time_text, (860, 40))

            score_text = font.render("Score: " + str(self.score), True, WHITE)
            self.screen.blit(score_text, (640, 10))

        
            pygame.display.flip()

            if self.game_over:
                self.screen.fill(BLACK)  # Clear the screen
                font = pygame.font.Font(SPACE, 50)
                game_over_text = font.render("END GAME", True, WHITE)
                game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 400))
                self.screen.blit(game_over_text, game_over_rect)
                self.sound_goodbye.play()

            
                game_data2 = {
                    "score": self.score,
                    "time": self.time_accumulator
                }
                self.save_game_data2(game_data2)


        pygame.time.wait(2000)
   