import pygame
from settings import *

class Shoot(pygame.sprite.Sprite):
    def __init__(self, player_rect, speed, direction):
        super().__init__()

        original_image = pygame.image.load("assets/images/Background/pngegg.png").convert_alpha()
        scale_factor = 1  # Factor de escala para ajustar el tamaño del láser
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()

        if direction == "right":
            if player_rect.left < WIDTH / 2:
                self.rect.midright = player_rect.midleft
                self.rect.x += 150  # Ajustar la coordenada X con un desplazamiento positivo
                self.rect.y -= 16  # Subir los disparos ajustando la coordenada Y
            else:
                self.rect.midleft = player_rect.midright
                self.rect.x -= 150  # Ajustar la coordenada X con un desplazamiento negativo
                self.rect.y -= 16  # Subir los disparos ajustando la coordenada Y
        elif direction == "left":
            if player_rect.left < WIDTH / 2:
                self.rect.midleft = player_rect.midright
                self.rect.x -= 150  # Ajustar la coordenada X con un desplazamiento negativo
                self.rect.y -= 16  # Subir los disparos ajustando la coordenada Y
            else:
                self.rect.midright = player_rect.midleft
                self.rect.x += 150  # Ajustar la coordenada X con un desplazamiento positivo
                self.rect.y -= 16  # Subir los disparos ajustando la coordenada Y

        self.velocidad_x = -speed if direction == "left" else speed  # Velocidad negativa para la izquierda, velocidad positiva para la derecha
        self.velocidad_y = 0

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

      

#-------------------------------------------------------------------------------------------------------------------------------------------------

class Shootbot(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("assets/images/firer (1).png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 6
        self.direction = direction

    def update(self):
        self.rect.x += self.direction * self.speed

#------------------------------------------------------------------------------------------------------------------------------------------------
class FireRain(pygame.sprite.Sprite):
    def __init__(self, x, y, images, direction):
        super().__init__()
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 6
        self.timer = 0
        self.interval = 10
        self.direction = direction

    def update(self):
        self.timer += 10

        if self.timer > self.interval:
            self.timer = 0
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0

            self.image = self.images[self.image_index]

        self.rect.y += self.speed
        self.rect.x += self.direction * self.speed
