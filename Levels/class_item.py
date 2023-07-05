import pygame
from settings import *

class SurvivalKit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(ITEM_SURVIVAL).convert_alpha()

        scale_factor = 1.2
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity_y = 5  # Velocidad vertical del item

    def update(self, player):
        pass
#--------------------------------------------------------------------------------------------------------------------------------------

class Hearts(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(ITEM_HEART).convert_alpha()

        scale_factor = 1.2
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 4  # Velocidad horizontal del item

    def update(self, player):
        self.rect.x += self.velocity_x  # Actualizar posición horizontal

        # Verificar y corregir posición si se sale de los límites horizontales
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x *= -1
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity_x *= -1

#--------------------------------------------------------------------------------------------------------------------------------------

class Stars(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(ITEM_STARS).convert_alpha()

        scale_factor = 0.4
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player):
        pass
#--------------------------------------------------------------------------------------------------------------------------------------

class Moon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(ITEM_MOON).convert_alpha()

        scale_factor = 0.4
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player):
        pass

#--------------------------------------------------------------------------------------------------------------------------------------

class Starship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(ITEM_STARSHIP).convert_alpha()

        scale_factor = 1
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player):
        pass


