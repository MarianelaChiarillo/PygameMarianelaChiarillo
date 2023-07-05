import pygame
from pygame.locals import *
from settings import *
from sprites import *

class FireSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {
            'fire_red': [
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (4).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (5).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (6).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (7).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (8).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (9).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Sky plattform/firer (10).png").convert_alpha(), (20, 20)),
               
            ]

        }
        self.animation_state = "fire_red"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.left = 0  # Posición inicial en el borde izquierdo
        self.rect.bottom = HEIGHT  # Posición vertical en la parte inferior
        self.image.set_colorkey(BACKGROUND_COLOR)

    def update(self):
        self.animation_index = (self.animation_index + 1) % len(self.animations[self.animation_state])
        self.image = self.animations[self.animation_state][self.animation_index]
    

class Blue(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {
            "Blue": [
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Items/umbrella (4).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Items/umbrella (6).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Items/umbrella (7).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Items/umbrella (8).png").convert_alpha(), (20, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/Characters/Items/umbrellacl.png").convert_alpha(), (20, 20)),            
            ]

        }
        self.animation_state = "Blue"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.left = 0  # Posición inicial en el borde izquierdo
        self.rect.bottom = HEIGHT  # Posición vertical en la parte inferior
        self.image.set_colorkey(BACKGROUND_COLOR)

    def update(self):
        self.animation_index = (self.animation_index + 1) % len(self.animations[self.animation_state])
        self.image = self.animations[self.animation_state][self.animation_index]


class Level3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {
            "Level3": [
                pygame.transform.scale(pygame.image.load("assets/images/firer (2).png").convert_alpha(), (30, 20)),
                pygame.transform.scale(pygame.image.load("assets/images/firer (3).png").convert_alpha(), (30, 20)),
            ]
        }
        self.animation_state = "Level3"
        self.animation_index = 0
        self.image = self.animations[self.animation_state][self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.left = 0  # Posición inicial en el borde izquierdo
        self.rect.bottom = HEIGHT  # Posición vertical en la parte inferior
        self.image.set_colorkey(BACKGROUND_COLOR)

    def update(self):
        self.animation_index = (self.animation_index + 1) % len(self.animations[self.animation_state])
        self.image = self.animations[self.animation_state][self.animation_index]

