import pygame, sys
from pygame.locals import *
from settings import *
from Level1 import *
from Level2 import *
from Level3 import *
import json


class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.game_state = {}  # Inicializa el atributo game_state como un diccionario vacío
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SpaceLost")
        self.icon = pygame.transform.scale(pygame.image.load(ICONMENU_BACKGROUND).convert_alpha(), SIZE_ICON)
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.loading_text = "SPACELOST"
        self.loading_font = pygame.font.Font(SPACE, 60)
        self.loading_time = 10  # Duración de la pantalla de carga en segundos
        self.game1_data = "game1_data.json"
        self.game2_data = "game_data2.json"
        self.game3_data = "game_data3.json"
        self.paused = False
        self.font = pygame.font.Font(SPACE, 50)
        self.score = 0
        self.lives = 3
        self.time_accumulator = 0
        self.sound = pygame.mixer.Sound("assets/sounds/ambience/documentary-background-music-for-crime-and-robbery-videos-trial-153276.mp3")
        self.sound_volume = 0.5  # Valor inicial del volumen del sonido
        self.sound.set_volume(self.sound_volume)
        self.sound.play()

    def adjust_sound_volume(self):
        self.sound.set_volume(self.sound_volume)



    def show_pause_screen(self):
        pause_font = pygame.font.Font(SPACE, 25)
        pause_text = pause_font.render("Paused", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Salir de la pantalla de pausa y reanudar el juego

            self.screen.fill(BLACK)  # Limpiar la pantalla
            # Dibujar contenido de la pantalla de pausa
            self.screen.blit(pause_text, pause_rect)
            # Guardar el estado del juego
            self.save_game_state('game_state.json', self.game_state)
            pygame.display.flip()
            self.clock.tick(120)

        
    def resume_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return  # Salir de la pantalla de reanudación y continuar con el juego

            self.screen.fill(BLACK)  # Limpiar la pantalla
            # Dibujar contenido de la pantalla de reanudación
            resume_text = self.font.render("Game Resumed", True, WHITE)
            resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(resume_text, resume_rect)

            pygame.display.flip()
            self.clock.tick(120)
    

    def show_levels_screen(self):
        title_font = pygame.font.Font(SPACE, 80)
        title_text = title_font.render("LEVELS", True, WHITE)
        title_rect = title_text.get_rect(center=(500, 100))
        self.back_icon_font = pygame.font.Font(SPACE, 25)
        self.back_icon_text = self.back_icon_font.render("Back", True, WHITE)
        self.back_icon_rect = self.back_icon_text.get_rect(left=40, top=30)
        level_unlocked_2 = False
        level_unlocked_3 = False


        level_images = [
            pygame.image.load("assets/images/Background/4172161.jpg"),
            pygame.image.load("assets/images/Background/2206_w026_n002_2110b_p1_2110e.jpg"),
            pygame.image.load("assets/images/Background/2211.w026.n002.2810B.p1.2810e.jpg")
        ]
        level_names = ["Level 1", "Level 2", "Level 3"]
        level_rects = []  # Lista para almacenar los rectángulos de los niveles

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Regresar a la pantalla principal
                    elif event.key == pygame.K_0:
                        self.show_pause_screen()  # Mostrar la pantalla de pausa al presionar la tecla "P"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_icon_rect.collidepoint(event.pos):
                        return  # Regresar a la pantalla principal
                    else:
                        for i, level_rect in enumerate(level_rects):
                            if level_rect.collidepoint(event.pos):
                                if i == 0:
                                    self.show_level_one()  # Mostrar nivel 1
                                    #if self.score >= 400:  # Verificar puntaje alcanzado
                                       # level_unlocked_2 = True  # Desbloquear nivel 2
                                elif i == 1: #and level_unlocked_2:
                                    self.show_level_two()  # Mostrar nivel 2
                                    #if self.score >= 600:  # Verificar puntaje alcanzado
                                        #level_unlocked_3 = True  # Desbloquear nivel 3
                                elif i == 2: #and level_unlocked_3:
                                    self.show_level_three()  # Mostrar nivel 3

            background_image = pygame.image.load(MENU_BACKGROUND).convert()
            self.screen.blit(background_image, ORIGIN)

            # Dibujar el contenido de la pantalla de niveles
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)  # Dibujar el fondo del botón "Back"
            self.screen.blit(self.back_icon_text, self.back_icon_rect)  # Dibujar el texto del botón "Back"

            square_size = 100
            square_margin = 50
            start_x = (WIDTH - square_size) // 3
            start_y = 200

            for i in range(3):
                square_rect = pygame.Rect(start_x, start_y + (square_size + square_margin) * i, square_size, square_size)
                pygame.draw.rect(self.screen, WHITE, square_rect)
                level_image = pygame.transform.scale(level_images[i], (square_size, square_size))
                self.screen.blit(level_image, square_rect)

                level_name_font = pygame.font.Font(SPACE, 20)
                level_name_text = level_name_font.render(level_names[i], True, WHITE)
                level_name_rect = level_name_text.get_rect(left=square_rect.right + 20, centery=square_rect.centery)
                self.screen.blit(level_name_text, level_name_rect)

                level_rects.append(square_rect)  # Agregar el rectángulo a la lista level_rects

            self.screen.blit(title_text, title_rect)
            pygame.display.flip()
            self.clock.tick(120)


#-------------------------------------------------------------------------------------------------------------------------------
    def show_level_one(self):
        level_one = LevelOne()
        self.paused = False  # Inicializar la variable de pausa
        resume_pressed = False  # Inicializar la variable de reanudación

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Salir del nivel y regresar a la pantalla principal
                    elif event.key == pygame.K_0:
                        self.paused = not self.paused  # Cambiar el estado de pausa al presionar la tecla "P"
                    elif event.key == pygame.K_1:
                        resume_pressed = True  # Establecer la variable de reanudación en True al presionar la tecla "R"

            if not self.paused:
                level_one.run()
            
            if self.lives <= 0:
                self.show_game_over_screen()  # Mostrar la pantalla de Game Over
                return  # Regresar a la pantalla de niveles
            
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)  # Dibujar el botón "Back"
            self.screen.blit(self.back_icon_text, self.back_icon_rect)


            # Dibujar el botón de regreso
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)
            self.screen.blit(self.back_icon_text, self.back_icon_rect)

            if self.paused:
                # Dibujar el botón de reanudar
                resume_icon_rect = pygame.Rect(40, 80, 80, 30)
                pygame.draw.rect(self.screen, BLACK, resume_icon_rect)
                self.resume_icon_text = pygame.font.Font(SPACE, 25)
                self.resume_icon_text = self.back_icon_font.render("Resume", True, WHITE)
                self.screen.blit(self.resume_icon_text, self.resume_icon_rect)

            pygame.display.flip()
            self.clock.tick(120)

            if resume_pressed:
                self.resume_game()
                level_one = LevelOne()  # Reiniciar el nivel
                self.paused = False  # Restablecer el estado de pausa
                resume_pressed = False  # Restablecer el estado de reanudación


    def show_level_two(self):
        level_two = LevelTwo()
        self.paused = False  # Inicializar la variable de pausa
        resume_pressed = False  # Inicializar la variable de reanudación

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Salir del nivel y regresar a la pantalla principal
                    elif event.key == pygame.K_0:
                        self.paused = not self.paused  # Cambiar el estado de pausa al presionar la tecla "P"
                    elif event.key == pygame.K_1:
                        resume_pressed = True  # Establecer la variable de reanudación en True al presionar la tecla "R"

            if not self.paused:
                level_two.run()
            
            if self.lives <= 0:
                self.show_game_over_screen()  # Mostrar la pantalla de Game Over
                return  # Regresar a la pantalla de niveles

            # Dibujar el botón de regreso
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)
            self.screen.blit(self.back_icon_text, self.back_icon_rect)

            if self.paused:
                # Dibujar el botón de reanudar
                resume_icon_rect = pygame.Rect(40, 80, 80, 30)
                pygame.draw.rect(self.screen, BLACK, resume_icon_rect)
                self.resume_icon_text = pygame.font.Font(SPACE, 25)
                self.resume_icon_text = self.back_icon_font.render("Resume", True, WHITE)
                self.screen.blit(self.resume_icon_text, self.resume_icon_rect)

            pygame.display.flip()
            self.clock.tick(120)

            if resume_pressed:
                self.resume_game()
                level_two = LevelTwo()  # Reiniciar el nivel
                self.paused = False  # Restablecer el estado de pausa
                resume_pressed = False  # Restablecer el estado de reanudación


    def show_level_three(self):
        level_three = LevelThree()
        self.paused = False  # Inicializar la variable de pausa
        resume_pressed = False  # Inicializar la variable de reanudación

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Salir del nivel y regresar a la pantalla principal
                    elif event.key == pygame.K_0:
                        self.paused = not self.paused  # Cambiar el estado de pausa al presionar la tecla "P"
                    elif event.key == pygame.K_1:
                        resume_pressed = True  # Establecer la variable de reanudación en True al presionar la tecla "R"

            if not self.paused:
                level_three.run()
            
            if self.lives <= 0:
                self.show_game_over_screen()  # Mostrar la pantalla de Game Over
                return  # Regresar a la pantalla de niveles

            # Dibujar el botón de regreso
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)
            self.screen.blit(self.back_icon_text, self.back_icon_rect)

            if self.paused:
                # Dibujar el botón de reanudar
                resume_icon_rect = pygame.Rect(40, 80, 80, 30)
                pygame.draw.rect(self.screen, BLACK, resume_icon_rect)
                self.resume_icon_text = pygame.font.Font(SPACE, 25)
                self.resume_icon_text = self.back_icon_font.render("Resume", True, WHITE)
                self.screen.blit(self.resume_icon_text, self.resume_icon_rect)

            pygame.display.flip()
            self.clock.tick(120)

            if resume_pressed:
                self.resume_game()
                level_three = LevelThree()  # Reiniciar el nivel
                self.paused = False  # Restablecer el estado de pausa
                resume_pressed = False  # Restablecer el estado de reanudación


#----------------------------------------------------------------------------------------------------------------------------
    def show_settings_screen(self):
        self.back_icon_font = pygame.font.Font(SPACE, 25)
        self.back_icon_text = self.back_icon_font.render("Back", True, WHITE)
        self.back_icon_rect = self.back_icon_text.get_rect(left=40, top=30)

        sound_slider_x = 300
        sound_slider_y = 450
        sound_slider_width = 400
        sound_slider_height = 20
        sound_slider_handle_radius = 10
        sound_slider_handle_color = BAR_COLOR

        # Crear el rectángulo para el control deslizante del sonido
        sound_slider_rect = pygame.Rect(sound_slider_x, sound_slider_y, sound_slider_width, sound_slider_height)

        # Crear el rectángulo para el control deslizante del sonido
        sound_slider_handle_x = int(sound_slider_x + (self.sound_volume / 1) * sound_slider_width) - sound_slider_handle_radius
        sound_slider_handle_y = sound_slider_y - sound_slider_handle_radius
        sound_slider_handle_rect = pygame.Rect(sound_slider_handle_x, sound_slider_handle_y, 2 * sound_slider_handle_radius, 2 * sound_slider_handle_radius)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Regresar a la pantalla principal
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if sound_slider_handle_rect.collidepoint(event.pos):
                            self.slider_grabbed = True
                        elif self.back_icon_rect.collidepoint(event.pos):
                            return  # Regresar a la pantalla principal
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.slider_grabbed = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.slider_grabbed:
                        new_x = event.pos[0] - sound_slider_handle_radius
                        if new_x < sound_slider_x:
                            new_x = sound_slider_x
                        elif new_x > sound_slider_x + sound_slider_width - 2 * sound_slider_handle_radius:
                            new_x = sound_slider_x + sound_slider_width - 2 * sound_slider_handle_radius

                        sound_slider_handle_rect.x = new_x
                        self.sound_volume = ((new_x - sound_slider_x) / sound_slider_width) * 1
                        self.adjust_sound_volume()

            self.screen.fill(BLACK)  # Limpiar pantalla

            # Dibujar el control deslizante
            pygame.draw.rect(self.screen, WHITE, sound_slider_rect)
            pygame.draw.circle(self.screen, sound_slider_handle_color, sound_slider_handle_rect.center, sound_slider_handle_radius)

            # Dibujar el texto del volumen
            volume_text_font = pygame.font.Font(SPACE, 25)
            volume_text = volume_text_font.render("Volume: {}%".format(int(self.sound_volume * 100)), True, WHITE)
            volume_text_rect = volume_text.get_rect(center=(WIDTH // 2, sound_slider_y - 50))
            self.screen.blit(volume_text, volume_text_rect)

            # Dibujar el botón "Back"
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)
            self.screen.blit(self.back_icon_text, self.back_icon_rect)

            pygame.display.flip()
            self.clock.tick(60)
#--------------------------------------------------------------------------------------------------------------------------

    def show_info_screen(self):
        title_font = pygame.font.Font(SPACE, 80)
        title_text = title_font.render("SCORES", True, WHITE)
        title_rect = title_text.get_rect(center=(500, 100))
        self.back_icon_font = pygame.font.Font(SPACE, 20)
        self.back_icon_text = self.back_icon_font.render("Back", True, WHITE)
        self.back_icon_rect = self.back_icon_text.get_rect(left=40, top=30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Volver a la pantalla 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_icon_rect.collidepoint(event.pos):
                        return  # Volver a la pantalla principal

            try:
                with open(self.game1_data, "r") as file:
                    all_data = json.load(file)
            except Exception:
                all_data = []

            try:
                with open(self.game2_data, "r") as file:
                    json_data_2 = json.load(file)
            except Exception:
                json_data_2 = []

            try:
                with open(self.game3_data, "r") as file:
                    json_data_3 = json.load(file)
            except Exception:
                json_data_3 = []

            background_image = pygame.image.load(MENU_BACKGROUND).convert()
            self.screen.blit(background_image, ORIGIN)

            # Ordenar los datos por puntuación de mayor a menor
            all_data = sorted(all_data, key=lambda x: x['score'], reverse=True)
            json_data_2 = sorted(json_data_2, key=lambda x: x['score'], reverse=True)
            json_data_3 = sorted(json_data_3, key=lambda x: x['score'], reverse=True)

            # Dibujar las partidas con mayor puntuación
            font = pygame.font.Font(SPACE, 20)
            y = 250  # Posición vertical inicial para dibujar los datos
            max_entries = 5  # Número máximo de entradas para mostrar
            entry_count = 0  # Contador de entradas mostradas

            for data in all_data:
                if entry_count >= max_entries:
                    break
                score_text = font.render("Score: " + str(data["score"]), True, WHITE)
                time_text = font.render("Time: " + str(data["time"]), True, WHITE)
                self.screen.blit(score_text, (150, y))
                self.screen.blit(time_text, (350, y))
                y += 30
                entry_count += 1

            for data in json_data_2:
                if entry_count >= max_entries:
                    break
                score_text = font.render("Score L2: " + str(data["score"]), True, WHITE)
                time_text = font.render("Time: " + str(data["time"]), True, WHITE)
                self.screen.blit(score_text, (550, y))
                self.screen.blit(time_text, (750, y))
                y += 30
                entry_count += 1

            for data in json_data_3:
                if entry_count >= max_entries:
                    break
                score_text = font.render("Score L3: " + str(data["score"]), True, WHITE)
                time_text = font.render("Time: " + str(data["time"]), True, WHITE)
                self.screen.blit(score_text, (950, y))
                self.screen.blit(time_text, (1150, y))
                y += 30
                entry_count += 1

            # Dibujar el botón de regreso
            pygame.draw.rect(self.screen, BLACK, self.back_icon_rect)
            self.screen.blit(self.back_icon_text, self.back_icon_rect)
            self.screen.blit(title_text, title_rect)
            pygame.display.flip()
            self.clock.tick(60)

#------------------------------------------------------------------------------------------------------------------------
    
    def show_main_screen(self):
    
        background_image = pygame.image.load(MENU_BACKGROUND).convert()
        self.screen.blit(background_image, ORIGIN)

        title_font = pygame.font.Font(SPACEMAN, 80)
        option_font = pygame.font.Font(SPACEMAN, 50)
        title_text = title_font.render("SpaceLost", True, WHITE)
        title_rect = title_text.get_rect(center=(500, 130))
        play_text = option_font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=(500, 350))
        config_text = option_font.render("Settings", True, WHITE)
        config_rect = config_text.get_rect(center=(500, 450))
        ranking_text = option_font.render("Info", True, WHITE)
        ranking_rect = ranking_text.get_rect(center=(500, 550))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_rect.collidepoint(mouse_pos):
                        self.show_levels_screen()
                    elif config_rect.collidepoint(mouse_pos):
                        self.show_settings_screen()
                    elif ranking_rect.collidepoint(mouse_pos):
                        self.show_info_screen()

        
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(play_text, play_rect)
            self.screen.blit(config_text, config_rect)
            self.screen.blit(ranking_text, ranking_rect)

            pygame.display.flip()
            self.clock.tick(60)  # Limitar el framerate a 60 FPS

                
    def run(self):
        self.show_main_screen()
        menu.show_settings_screen()

        pygame.quit()
        sys.exit()

menu = Menu()
menu.run()
level_one = LevelOne()
menu = Menu(level_one)
 
    
