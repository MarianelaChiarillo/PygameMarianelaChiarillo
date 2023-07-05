import pygame

class Sounds:  
    def __init__(self):
        pygame.mixer.init()
        self.sound_effects = {
                "sonido": pygame.mixer.Sound("assets/sounds/ambience/documentary-background-music-for-crime-and-robbery-videos-trial-153276.mp3"),
                "sonido_colision_bird": pygame.mixer.Sound("assets/sounds/colorado-bird-crow-03.wav"),
                "sonido_fire": pygame.mixer.Sound("assets/sounds/shoot/FIREIGNITELRG.WAV"),
                "sonido_item": pygame.mixer.Sound("assets/sounds/Dixie Hurt.WAV"),
                "sonido_colision_bot": pygame.mixer.Sound("assets/sounds/shoot/botpunch.wav"),
                "sonido_ground": pygame.mixer.Sound("assets/sounds/shoot/MIX_CAD_BANE_EXPLOSION_ASHES.wav"),
                "sonido_fire_bot": pygame.mixer.Sound("assets/sounds/shoot/BoomerExplosionDistant03_2.ogg"),
                "sonido_colision_fish": pygame.mixer.Sound("assets/sounds/movement/step_acolyte1bmetal2.wav"),
                "sonido_fire_dos": pygame.mixer.Sound("assets/sounds/shoot/EVENT_BRIDGE_COLLAPSE.wav"),
                "sonido_fire_rain": pygame.mixer.Sound("assets/sounds/endship.wav"),
                "sonido_enemyhorse": pygame.mixer.Sound("assets/sounds/shoot/punchplayer.wav")
            }
        
        self.volume_level = 0.5

    def adjust_volume(self):
        for sound in self.sound_effects.values():
            sound.set_volume(self.volume_level)

    def set_volume_level(self, volume_level):
        self.volume_level = max(0, min(volume_level, 1))
        self.adjust_volume()