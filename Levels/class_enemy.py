import pygame
from settings import *
from Characters import *
from shoots import *



class EnemyBird(pygame.sprite.Sprite):
    enemies = []  # Atributo de clase para almacenar los enemigos

    def __init__(self, player_rect, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.player_rect = player_rect
        self.animations = {
            "Bird_Left": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/BirdL1/leftb/FlyEnemie (8).png").convert_alpha(), (60, 60)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/BirdL1/leftb/FlyEnemied.png").convert_alpha(), (60, 60)),
            ],
           
            "Bird_Right": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/BirdL1/rightb/FlyEnemie (8).png").convert_alpha(), (60, 60)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/BirdL1/rightb/FlyEnemie (9).png").convert_alpha(), (60, 60)),
            ]
        }
        
        self.animation_state = "Bird_Left"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.direction = 1
        self.speed = 6
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 0
        self.player = Player()
        self.animation_timer = 0
        self.animation_speed = 7
        self.shots_count = 0
        

    def update(self):
        self.move()
        self.animate()
        self.check_player_distance()
        self.check_collision()
    
    def move(self):
        self.rect.x += self.direction * self.speed

        if self.rect.right >= WIDTH:
            self.direction = -1
            self.animation_state = "Bird_Left"
        elif self.rect.left <= 0:
            self.direction = 1
            self.animation_state = "Bird_Right"

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_index += 1
            self.animation_timer = 0

            if self.animation_index >= len(self.animations[self.animation_state]):
                self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)


    def check_player_distance(self):
        dx = self.player_rect.x - self.rect.x
        dy = self.player_rect.y - self.rect.y
        distance_squared = dx ** 2 + dy ** 2

        if distance_squared < 100 ** 2:
            if self.rect.x < self.player_rect.x:
                self.direction = 1
                self.animation_state = "Bird_Right"
            elif self.rect.x > self.player_rect.x:
                self.direction = -1
                self.animation_state = "Bird_Left"
        else:
            if self.direction == 1:
                self.animation_state = "Bird_Right"
            else:
                self.animation_state = "Bird_Left"

    def check_collision(self):
        if self.rect.colliderect(self.player_rect):
            self.direction = 0  # Detener el movimiento del bot al colisionar

    def handle_shoot_hit(self):
        # Incrementar el contador de disparos
        self.shots_count += 1
        if self.shots_count >= 5:
            self.kill()  # Eliminar el enemigo si ha recibido 5 disp
            

#---------------------------------------------------------------------------------------------------------------------------------------------

class BotEnemy(pygame.sprite.Sprite):
    enemiesBot = []  # Atributo de clase para almacenar los enemigos

    def __init__(self, player_rect, x=0, y=0, platform_group=None, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.player_rect = player_rect
        self.player = player
        self.animations = {
            "BotLeft": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/RobotL2/104.png").convert_alpha(), (65, 60)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/RobotL2/105.png").convert_alpha(), (80, 60)),
            ],
            "Shoot_left": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/RobotL2/107.png").convert_alpha(), (90, 60)),
            ],
            "BotRight": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/RobotL2/104R.png").convert_alpha(), (65, 60)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/RobotL2/105r.png").convert_alpha(), (80, 60)),
            ],
            "Shoot_Right": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/RobotL2/107r.png").convert_alpha(), (90, 60)),
            ],
        }
        
        self.animation_state = "BotLeft"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.direction = 1
        self.speed = 6
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 0
        self.player = Player()
        self.animation_timer = 0
        self.animation_speed = 20  # Ajusta este valor para cambiar la velocidad de la animación
        self.platform_group = platform_group  # Agregar referencia al grupo de plataformas
        self.shoot_timer = 0
        self.shoot_interval = 25  # Intervalo de tiempo entre disparos (en fotogramas)


    
    def update(self):
        self.move()
        self.animate()
        self.check_player_distance()
        self.check_collision()
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot()
            self.shoot_timer = 0
        for bullet in self.enemiesBot:
            bullet.update()  # Actualizar la posición de los bots generados


    def move(self):
        if self.direction == 1 and self.rect.right >= WIDTH - 10:
            self.direction = -1
        elif self.direction == -1 and self.rect.left <= 10:
            self.direction = 1

        self.rect.x += self.direction * self.speed

        # Verificar colisiones con las plataformas
        for platform in self.platform_group:
            if self.rect.colliderect(platform.rect):
                if self.direction == 1:
                    # El bot está moviéndose hacia la derecha y colisiona con una plataforma
                    self.rect.right = platform.rect.left
                elif self.direction == -1:
                    # El bot está moviéndose hacia la izquierda y colisiona con una plataforma
                    self.rect.left = platform.rect.right

        # Continuar moviéndose en la dirección actual
        self.rect.y += self.y_speed

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_index += 1
            if self.animation_index >= len(self.animations[self.animation_state]):
                self.animation_index = 0
            self.animation_timer = 0

        # Verificar si el índice aún está dentro del rango válido
        if self.animation_index < len(self.animations[self.animation_state]):
            self.image = self.animations[self.animation_state][self.animation_index]
        else:
            # Si el índice está fuera del rango, establecer la imagen predeterminada
            self.image = self.animations[self.animation_state][0]

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def check_player_distance(self):
        dx = self.player_rect.x - self.rect.x
        dy = self.player_rect.y - self.rect.y
        distance_squared = dx ** 2 + dy ** 2

        if distance_squared < 100 ** 2:  # Cambia el valor 200 según tus necesidades
            if self.rect.x < self.player_rect.x:
                self.direction = 1
                self.animation_state = "BotRight"
            elif self.rect.x > self.player_rect.x:
                self.direction = -1
                self.animation_state = "BotLeft"
            else:
                self.direction = 0
                self.animation_state = "BotLeft"
        else:
            if self.direction == 1:
                self.animation_state = "BotRight"
            else:
                self.animation_state = "BotLeft"

    def check_collision(self):
        if self.rect.colliderect(self.player_rect):
            self.direction = 0  # Detener el movimiento del bot al colisionar

    def shoot(self):
        dx = self.player_rect.x - self.rect.x
        dy = self.player_rect.y - self.rect.y
        distance_squared = dx ** 2 + dy ** 2

        if distance_squared < 120 ** 2:  # Cambia el valor 100 según tus necesidades
            direction = -1 if self.direction == -1 else 1
            bullet_x = self.rect.centerx + direction * (self.rect.width // 2)
            bullet_y = self.rect.centery
            bullet = Shootbot(bullet_x, bullet_y, direction)
            self.enemiesBot.append(bullet)

            if self.direction == 1:
                self.animation_state = "Shoot_Right"
            else:
                self.animation_state = "Shoot_left"

            self.animation_timer = 0  # Reiniciar el contador de frames
            self.animation_speed = 60  # Velocidad de animación más rápida durante la transición

            # Establecer el estado de animación anterior después de 10 frames
            if self.animation_timer >= 10:
                if self.direction == 1:
                    self.animation_state = "BotRight"
                else:
                    self.animation_state = "BotLeft"

            self.shoot_timer = -20  # Esperar un poco antes de disparar nuevamente


#--------------------------------------------------------------------------------------------------------------------------------------------

class FishEnemy(pygame.sprite.Sprite):
    enemiesFish = []  # Atributo de clase para almacenar los enemigos

    def __init__(self, player_rect, x=0, y=0, platform_group=None):
        pygame.sprite.Sprite.__init__(self)
        self.player_rect = player_rect
        self.animations = {
            "FishLeft": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/1.png").convert_alpha(), (60, 30)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/2.png").convert_alpha(), (60, 30)),
            ],

            "FishShoot_left": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/10.png").convert_alpha(), (50, 50)),
            ],
            "FishRight": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/fR (1).png").convert_alpha(), (60, 30)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/fR (7).png").convert_alpha(), (60, 30)),
            ],

            "FishShoot_Right_": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/fR (6).png").convert_alpha(), (50, 50)),
            ],
            "FireLeft": [
            pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/22.png").convert_alpha(), (30, 30)),
            ],

            "FireRight": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Fish3/fR (2).png").convert_alpha(), (30, 30)),
            ],
        }

        self.animation_state = "FishLeft"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.direction = 1
        self.speed = 7
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 0
        self.player = Player()
        self.animation_timer = 0
        self.animation_speed = 7  # Ajusta este valor para cambiar la velocidad de la animación
        self.platform_group = platform_group  # Agregar referencia al grupo de plataformas
        self.shoot_timer = 0
        self.shoot_interval = 60  # Intervalo de tiempo entre disparos (en fotogramas)
        self.fire_rain_group = pygame.sprite.Group()  # Grupo para almacenar las bolas de fuego
        self.spawn_timer = 0  # Agregar el temporizador de aparición
        self.spawn_delay = 100  # Retraso de 10 segundos (600 fotogramas)

    def update(self):
        self.move()
        self.animate()
        self.check_player_distance()
        self.check_collision()
        self.spawn_timer += 1  # Incrementar el temporizador en cada fotograma
        if self.spawn_timer >= self.spawn_delay:  # Verificar si ha pasado el retraso
            self.shoot()  # Comenzar a disparar
            self.spawn_timer = 0  # Reiniciar el temporizador después de disparar

        self.fire_rain_group.update()  # Actualizar las bolas de fueg

    def move(self):
        if self.direction == 1 and self.rect.right >= WIDTH - 10:
            self.direction = -1
        elif self.direction == -1 and self.rect.left <= 10:
            self.direction = 1

        self.rect.x += self.direction * self.speed

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_index += 1
            self.animation_timer = 0

            if self.animation_index >= len(self.animations[self.animation_state]):
                self.animation_index = 0

        self.image = self.animations[self.animation_state][self.animation_index]

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def check_player_distance(self):
        dx = self.player_rect.x - self.rect.x
        dy = self.player_rect.y - self.rect.y
        distance_squared = dx ** 2 + dy ** 2

        if distance_squared < 100 ** 2:
            if self.rect.x < self.player_rect.x:
                self.direction = 1
                self.animation_state = "FishRight"
            elif self.rect.x > self.player_rect.x:
                self.direction = -1
                self.animation_state = "FishLeft"
            else:
                self.direction = 0
                self.animation_state = "FishLeft"
        else:
            if self.direction == 1:
                self.animation_state = "FishRight"
            else:
                self.animation_state = "FishLeft"

    def check_collision(self):
        if self.rect.colliderect(self.player_rect):
            self.direction = 0  # Detener el movimiento del Fish al colisionar

    def shoot(self):
        direction = -1 if self.direction == -1 else 1
        bullet_x = self.rect.centerx + direction * (self.rect.width // 2)
        bullet_y = self.rect.centery

        fire_images = self.animations["FireLeft"] if self.direction == -1 else self.animations["FireRight"]
        bullet = FireRain(bullet_x, bullet_y, fire_images, direction)
        self.fire_rain_group.add(bullet)  # Agregar la bola de fuego al grupo

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Dibujar el enemigo
        self.fire_rain_group.draw(screen)  # Dibujar las bolas de fuego

#------------------------------------------------------------------------------------------------------------------------------------------------------------

class EnemyHsea(pygame.sprite.Sprite):
    enemiesHsea = []  # Atributo de clase para almacenar los enemigos

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.animations = {
            "Sea_Left": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (3).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (4).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (6).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (7).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (8).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (9).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (1).png").convert_alpha(), (40, 40)),
            ],
            "Sea_Right": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (3).png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (11)R.png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (12)R.png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (10)R.png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (9)R.png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (8)R.png").convert_alpha(), (40, 40)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/seahorse/seahorse (1).png").convert_alpha(), (40, 40)),
            ],
        }
        self.animation_state = "Sea_Left"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.direction = 1  # Por defecto, empieza moviéndose hacia la derecha
        self.speed = 8
        self.y_speed = 0
        self.animation_timer = 0
        self.animation_speed = 7
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.move()
        self.animate()
        self.check_player_distance()
        self.check_collision()

    def move(self):
        self.rect.x += self.direction * self.speed

        if self.rect.right >= WIDTH:
            self.direction = -1
            self.animation_state = "Sea_Left"
        elif self.rect.left <= 0:
            self.direction = 1
            self.animation_state = "Sea_Right"

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_index += 1
            self.animation_timer = 0

            if self.animation_index >= len(self.animations[self.animation_state]):
                self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def check_player_distance(self):
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance_squared = dx ** 2 + dy ** 2

        if distance_squared < 100 ** 2:
            if self.rect.x < self.player.rect.x:
                self.direction = 1
                self.animation_state = "Sea_Right"
            elif self.rect.x > self.player.rect.x:
                self.direction = -1
                self.animation_state = "Sea_Left"
        else:
            if self.direction == 1:
                self.animation_state = "Sea_Right"
            else:
                self.animation_state = "Sea_Left"

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self):
        if self.rect.colliderect(self.player.rect):
            self.direction = 0  # Detener el movimiento del bot al colisionar
