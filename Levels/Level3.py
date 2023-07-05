import pygame, sys
from pygame.locals import *
from settings import *
from Characters import Player
from class_platform import Platform
from shoots import *
from class_sprite import *
from class_enemy import FishEnemy, EnemyHsea
from class_item import Stars, Hearts, Starship
import json

class LevelThree():
    def __init__(self):
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SpaceLost")
        self.icon = pygame.transform.scale(pygame.image.load(ICONMENU_BACKGROUND).convert_alpha(), SIZE_ICON)
        pygame.display.set_icon(self.icon)
        self.background = pygame.image.load(LEVEL3_BACKGROUND).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.platform_group = pygame.sprite.Group()
        self.player = Player()
        self.platforms = []
        self.enemies_group = pygame.sprite.Group()
        self.shoots_group = pygame.sprite.Group()  # Grupo de disparos
        self.enemySea = EnemyHsea(self.player)
        self.wall = pygame.transform.scale(pygame.image.load(WALL).convert_alpha(), (15, 600))
        self.image = self.wall
        self.rect = self.image.get_rect()
        self.rect.topleft = (820, 100)  # Ajustar la posición inicial en el piso
        self.stars_group = pygame.sprite.Group()  # Grupo de kits de supervivencia
        self.hearts_group = pygame.sprite.Group()
        self.starship_group = pygame.sprite.Group()
        self.lives = 3
        self.lives_im = pygame.transform.scale(pygame.image.load(LIVES_ITEM).convert_alpha(), (20, 20))
        self.game_over = False
        self.enemy_collisions = 0
        self.time_accumulator = 0  # Acumulador de tiempo
        self.score = 0
        self.sound_colision_fish = pygame.mixer.Sound("assets/sounds/movement/step_acolyte1bmetal2.wav")
        self.sound_fire_dos = pygame.mixer.Sound("assets/sounds/shoot/EVENT_BRIDGE_COLLAPSE.wav")
        self.sound_item = pygame.mixer.Sound("assets/sounds/Dixie Hurt.WAV")
        self.sound_fire_rain =  pygame.mixer.Sound("assets/sounds/endship.wav")
        self.sound_enemyhorse =  pygame.mixer.Sound("assets/sounds/shoot/punchplayer.wav")
        self.sound_goodbye = pygame.mixer.Sound("assets/sounds/voices/goodbye.OGG")
        self.game_data3_file = "game_data3.json" 
      

        
        # Crear una lista de coordenadas de plataformas
        platform_coordinates = [(20, 620), (200, 580), (250, 580), (465, 620), (650, 580), (700, 580), (520, 420), (450, 420), (250, 380), (20, 450), (80, 450), (50, 280), (250, 200), (320, 200), (480, 250), (670, 270), (610, 120), (920, 190), (840, 450), (890, 450)]

        for coord in platform_coordinates:
            x, y = coord
            platform = Platform(x, y, ROCK_PLATFORM)
            self.platform_group.add(platform)

        self.player = Player()
        self.player.rect.x = 0  # Ajustar la posición inicial en el borde izquierdo
        self.player.rect.y = 600  # Ajustar la posición inicial en la esquina inferior izquierda

        self.Three = pygame.sprite.Group()
        x = 0  # Variable para controlar la posición horizontal de los sprites de Level3
        Three_w = Level3().rect.width  # Ancho de los sprites de Level3
        for _ in range(WIDTH // Three_w):  # Crear sprites a lo largo de la pantalla
            LevelT = Level3()  # Crear una instancia de la clase Level3
            LevelT.rect.left = x
            LevelT.rect.bottom = HEIGHT
            self.Three.add(LevelT)  # Agregar la instancia al grupo
            x += Three_w
        
        """if pygame.sprite.collide_rect(self.player, self):
            if self.player.rect.left < self.rect.right:
                self.player.rect.left = self.rect.right
            elif self.player.rect.right > self.rect.left:
                self.player.rect.right = self.rect.left"""
                
        positions = [(300, 20),  (380, 50), (700, 40), (620, 60), (500, 30)]
        for position in positions:
            enemy = FishEnemy(self.player.rect, x=position[0], y=position[1], platform_group=self.platform_group)
            self.enemies_group.add(enemy)

        enemy1 = EnemyHsea(self.player)
        enemy1.rect.x = 300
        enemy1.rect.y = 160
        EnemyHsea.enemiesHsea.append(enemy1)  # Agregar al grupo de enemigos

        # Crear la segunda instancia de EnemyHsea
        enemy2 = EnemyHsea(self.player)
        enemy2.rect.x = 500  # Ajustar la posición para evitar superposición
        enemy2.rect.y = 360
        EnemyHsea.enemiesHsea.append(enemy2) 

        
        self.generate_stars()
    def generate_stars(self):
        platform_positions = [ (700, 520), (520, 380), (60, 400), (90, 220), (320, 150), (620, 200), (750, 100), (920, 150)]
        for x, y in platform_positions:
            Stars_t = Stars(x, y)
            self.stars_group.add(Stars_t)
        
        self.generate_hearts()
    def generate_hearts(self):
        platform_positions = [(150, 270), (350, 530), (720, 380), (600,150)]

        for x, y in platform_positions:
            hearts = Hearts(x, y)
            self.hearts_group.add(hearts)

        self.generate_starships()
    def generate_starships(self):
        platform_positions = [(850, 400), (920, 400), (885, 360)]

        for x, y in platform_positions:
            Starship_t = Starship(x, y)
            self.starship_group.add(Starship_t)

    def subtract_life(self):
        self.lives -= 1

        if self.lives <= 0:
            self.game_over = True

        self.player.rect.x = 0
        self.player.rect.y = 600
        self.sound_colision_fish.play()

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

    def update_wall(self):
        self.rect.x = 820  # Ajusta la posición horizontal de la pared
        self.rect.y = 100  # Ajusta la posición vertical de la pared


    def handle_shoot_hit(self, shoot):
        pygame.sprite.groupcollide(self.shoots_group, self.enemies_group, True, True)
    
    def save_game_data3(self, game_data3):
        try:
            with open(self.game_data3_file, "r") as file:
                all_data = json.load(file)
        except FileNotFoundError:
            all_data = []

        all_data.append(game_data3)

        with open(self.game_data3_file, "w") as file:
            json.dump(all_data, file)


    def run(self):
        while not self.game_over:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update()  # Actualizar el jugador
            self.player.handle_move()
            self.player.shoots_group.update()

            self.screen.blit(self.background, ORIGIN)
            self.player.draw(self.screen)
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
            self.screen.blit(self.image, self.rect)
            self.update_wall()  # Actualiza la posición de la pared

            self.Three.update()
            self.Three.draw(self.screen)
            self.shoots_group.update()  # Actualizar disparos
            self.player.shoots_group.draw(self.screen)  # Dibujar los disparos
            self.enemies_group.update()
            self.enemies_group.draw(self.screen)
            self.stars_group.update(self.player)
            self.stars_group.draw(self.screen)  # Dibujar los kits de supervivencia
            self.hearts_group.update(self.player) # Actualizar
            self.hearts_group.draw(self.screen)
            self.starship_group.update(self.player) # Actualizar
            self.starship_group.draw(self.screen)
            self.draw_lives(self.screen)
            self.player.draw(self.screen)  # Agregar esta línea

            if pygame.sprite.spritecollide(self.player, self.starship_group, False):
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

            
            if pygame.sprite.spritecollide(self.player, self.Three, False):
                self.game_over = True
                self.sound_fire_dos.play()
            
            if pygame.sprite.spritecollide(self.player, EnemyHsea.enemiesHsea, False):
                self.subtract_life()
                self.sound_enemyhorse.play()
            
            if pygame.sprite.spritecollide(self.player, self.hearts_group, True):
                self.restore_life()
                self.sound_item.play()
            
        
            for enemy in self.enemies_group:
                enemy.fire_rain_group.update()
                enemy.fire_rain_group.draw(self.screen)

                if pygame.sprite.spritecollide(self.player, enemy.fire_rain_group, False):
                        self.subtract_life()
                        self.sound_fire_rain.play()


            for enemy in EnemyHsea.enemiesHsea:
                enemy.update()  # Actualizar cada instancia de EnemyHsea
                enemy.draw(self.screen)  # Dibujar cada instancia de EnemyHse

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
                    self.sound_colision_fish.play()

            wall_group = pygame.sprite.GroupSingle(pygame.sprite.Sprite())
            wall_group.sprite.rect = self.rect

            if pygame.sprite.spritecollide(self.player, wall_group, False):
                self.player.rect.x = 0
                self.player.rect.y = 600




            score_increment = 0  # Variable para almacenar el incremento de puntaje

            # Check collision with survival kits
            survival_kit_collisions = pygame.sprite.spritecollide(self.player, self.stars_group, True)
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
                

                game_data3 = {
                    "score": self.score,
                    "time": self.time_accumulator
                }
                self.save_game_data3(game_data3)

        pygame.time.wait(2000)
