import pygame
from settings import *


class Platform(pygame.sprite.Sprite):
    platforms = []  # Lista de plataformas (atributo de clase)

    def __init__(self, x, y, image_path):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), PLATFORM_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collision_rect_bottom = pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2, self.rect.width, self.rect.height // 2)

        # Añadir límites de colisión para bloquear la caída del jugador
        self.collision_rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 100)
        self.collision_rect_bottom = pygame.Rect(self.rect.x, self.rect.bottom - 10, self.rect.width, 100)

        # Agregar la plataforma a la lista de plataformas
        Platform.platforms.append(self)

    
    def update(self):
        # Actualizar los límites de colisión junto con la posición de la plataforma
        self.collision_rect_top.topleft = self.rect.topleft
        self.collision_rect_bottom.topleft = self.rect.topleft
        
