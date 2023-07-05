import pygame
from pygame.locals import *
from settings import *
from shoots import Shoot
from sprites import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = get_animations()  # Obtener las animaciones del personaje
        self.animation_state = "left_stop"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.left = 0  # Comienza desde la posición más a la izquierda
        self.rect.bottom = HEIGHT  # Comienza desde la posición más abajo
        self.x_speed = 0
        self.y_speed = 0
        self.jumping = False
        self.direction = "right"
        self.lives = 3  # Número inicial de vidas
        self.is_impacted = False  # Variable para indicar si el jugador está en estado "impactado"
        self.impact_duration = 60  # Duración del efecto de impacto en fotogramas
        self.sonido_disparo = pygame.mixer.Sound("assets/sounds/optionsmenu/igbookfadein.wav")
        self.sonido_salto = pygame.mixer.Sound("assets/sounds/movement/fall.wav")
      

        # Añadir límites de colisión para bloquear la caída del jugador
        self.collision_rect_bottom = pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2, self.rect.width, self.rect.height // 2)

        self.shoot_duration = 0  # Duración actual del estado de "shoot"
        self.shoot_cooldown = 60  # Tiempo de enfriamiento (1 segundo * 60 fotogramas por segundo)
        self.shoots_group = pygame.sprite.Group()  # Grupo de sprites de disparos

    def update(self):
        self.rect.x += self.x_speed  # Movimiento lateral

        if self.rect.left <= 0:  # Límites de la pantalla
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        if self.jumping:
            self.rect.y += self.y_speed
            self.y_speed += GRAVITY  # Ajusta el valor de aceleración de la gravedad aquí (por ejemplo, 0.5)

            if self.rect.bottom >= HEIGHT - 10:
                self.rect.bottom = HEIGHT - 10
                self.jumping = False
                self.y_speed = 0  # Reinicia la velocidad vertical después de tocar el suelo

        if self.x_speed < 0:
            self.direction = "left"
            if self.jumping:
                self.animation_state = "left_jump"
            else:
                self.animation_state = "left_walk"

        elif self.x_speed > 0:
            self.direction = "right"
            if self.jumping:
                self.animation_state = "right_jump"
            else:
                self.animation_state = "right_walk"

        elif self.x_speed == 0 and not self.jumping:
            if self.direction == "left":               
                if self.shoot_duration <= 0:
                    self.animation_state = "left_stop"
                else:
                    self.animation_state = "left_shoot"
            else:
                if self.shoot_duration <= 0:
                    self.animation_state = "right_stop"
                else:
                    self.animation_state = "right_shoot"

        self.animation_index = (self.animation_index + 1) % len(self.animations[self.animation_state])
        self.image = self.animations[self.animation_state][self.animation_index]


        if self.shoot_duration > 0:
            self.shoot_duration -= 1

    def jump(self):
        if not self.jumping:
            self.y_speed = -JUMP_SPEED
            self.jumping = True


    def shoot(self):
        if self.direction == "right":
            self.animation_state = "right_shoot"
        else:
            self.animation_state = "left_shoot"

        shoot = Shoot(self.rect, SHOOT_SPEED, self.direction)  # Pasa la dirección del jugador a la instancia de Shoot
        self.shoots_group.add(shoot)

        self.shoot_duration = self.shoot_cooldown  # Reiniciar la duración del estado de "shoot"
        for shoot in self.shoots_group:
            shoot.update()


    def stop_shooting(self):
        if self.direction == "left":
            self.animation_state = "left_stop"
        else:
            self.animation_state = "right_stop"

        self.shoot_duration = 0  # Reiniciar la duración del estado de "shoot"

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

    def handle_move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_speed = -ASTRONAUT_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_speed = ASTRONAUT_SPEED
        else:
            self.x_speed = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump()
            self.sonido_salto.play()

        if keys[pygame.K_SPACE]:  # Verificar si se presiona la tecla de disparo (en este caso SPACE)
            self.shoot()
            self.sonido_disparo.play()
            
        if keys[pygame.K_TAB]:  # Verificar si se presiona la tecla TAB
            self.stop_shooting()

        