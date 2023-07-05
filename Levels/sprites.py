import pygame, sys

def get_animations():
    left_walk = [
        pygame.transform.scale(pygame.image.load("assets\images\Player\Left\walk (5).png").convert_alpha(), (65, 65)),
        pygame.transform.scale(pygame.image.load("assets\images\Player\Left\walk (6).png").convert_alpha(), (65, 65)),
    ]
    left_stop = [pygame.transform.scale(pygame.image.load("assets\images\Player\Left\walk (5).png").convert_alpha(), (65, 65))]

    left_jump = [
        pygame.transform.scale(pygame.image.load("assets\images\Player\Left\jump (2).png").convert_alpha(), (65, 65)),
    ]

    left_shoot = [
        pygame.transform.scale(pygame.image.load("assets\images\Player\Left\shoot (6).png").convert_alpha(), (65, 65)),
    ]

    right_stop = [pygame.transform.scale(pygame.image.load("assets\images\Player\Right\walk (5).png").convert_alpha(), (65, 65))]

    right_walk = [
        pygame.transform.scale(pygame.image.load("assets\images\Player\Right\walk (5).png").convert_alpha(), (65, 65)),
        pygame.transform.scale(pygame.image.load("assets\images\Player\Right\walk (6).png").convert_alpha(), (65, 65)),
    ]

    right_jump = [
        pygame.transform.scale(pygame.image.load("assets\images\Player\Right\walk (8).png").convert_alpha(), (65, 65)),
    ]

    right_shoot = [
        pygame.transform.scale(pygame.image.load("assets\images\Player\Right\shoot (6).png").convert_alpha(), (65, 60)),
    ]


    return {
        "left_walk": left_walk,
        "left_jump": left_jump,
        "left_shoot": left_shoot,
        "right_walk": right_walk,
        "right_jump": right_jump,
        "right_shoot": right_shoot,
        "right_stop": right_stop,
        "left_stop" : left_stop,

    }


