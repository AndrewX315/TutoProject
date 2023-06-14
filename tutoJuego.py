import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Definir las dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Definir las dimensiones del jugador
ANCHO_JUGADOR = 50
ALTO_JUGADOR = 50

# Definir las dimensiones del enemigo
ANCHO_ENEMIGO = 50
ALTO_ENEMIGO = 50

# Definir las dimensiones del tiro
ANCHO_TIRO = 10
ALTO_TIRO = 10

# Definir los estados del juego
ESTADO_MENU = 0
ESTADO_JUEGO = 1
ESTADO_FIN_JUEGO = 2
ESTADO_VICTORIA = 3
EN = 100;
# Definir la clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ANCHO_JUGADOR, ALTO_JUGADOR])
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA // 2
        self.rect.y = ALTO_PANTALLA - ALTO_JUGADOR
        self.vida = 100

    def update(self):
        # Obtener la posición actual del mouse
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

# Definir la clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ANCHO_ENEMIGO, ALTO_ENEMIGO])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO_PANTALLA - ANCHO_ENEMIGO)
        self.rect.y = random.randrange(-ALTO_ENEMIGO, -10)
        self.velocidad = random.randint(1, 3)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > ALTO_PANTALLA + ALTO_ENEMIGO:
            self.rect.x = random.randrange(ANCHO_PANTALLA - ANCHO_ENEMIGO)
            self.rect.y = random.randrange(-ALTO_ENEMIGO, -10)
            self.velocidad = random.randint(1, 3)

# Definir la clase Tiro
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([ANCHO_TIRO, ALTO_TIRO])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 5

    def update(self):
        self.rect.y -= self.velocidad
        if self.rect.y < -ALTO_TIRO:
            self.kill()

# Inicializar pantalla
pantalla = pygame.display.set_mode([ANCHO_PANTALLA, ALTO_PANTALLA])
pygame.display.set_caption("Juego con Pygame")

# Crear grupos de sprites
grupo_todos_los_sprites = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_tiros = pygame.sprite.Group()

# Crear al jugador
jugador = Jugador()
grupo_todos_los_sprites.add(jugador)

# Crear los enemigos
for _ in range(EN):
    enemigo = Enemigo()
    grupo_enemigos.add(enemigo)
    grupo_todos_los_sprites.add(enemigo)

# Variable para controlar el bucle principal del juego
hecho = False

# Variable para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Puntuación del jugador
puntuacion = 0

# Fuente del texto en pantalla
fuente = pygame.font.Font(None, 36)

# Variables de estado del juego
opcion_seleccionada = None
estado_juego = ESTADO_MENU

# Bucle principal del juego
while not hecho:
    if estado_juego == ESTADO_MENU:
        # Pantalla del menú
        pantalla.fill(NEGRO)
        texto_titulo = fuente.render("Juego con Pygame", True, BLANCO)
        texto_instrucciones = fuente.render("Presiona ESPACIO para empezar", True, BLANCO)
        pantalla.blit(texto_titulo, (ANCHO_PANTALLA // 2 - texto_titulo.get_width() // 2, 200))
        pantalla.blit(texto_instrucciones, (ANCHO_PANTALLA // 2 - texto_instrucciones.get_width() // 2, 250))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado_juego = ESTADO_JUEGO

    elif estado_juego == ESTADO_JUEGO:
        # Código del juego

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Disparar un tiro al hacer clic izquierdo
                tiro = Tiro(jugador.rect.centerx, jugador.rect.y)
                grupo_tiros.add(tiro)
                grupo_todos_los_sprites.add(tiro)

        grupo_todos_los_sprites.update()

        # Comprobar colisiones entre el jugador y los enemigos
        colisiones_enemigo = pygame.sprite.spritecollide(jugador, grupo_enemigos, True)
        for enemigo in colisiones_enemigo:
            jugador.vida -= 10
            if jugador.vida <= 0:
                estado_juego = ESTADO_FIN_JUEGO

        # Comprobar colisiones entre los tiros y los enemigos
        colisiones_tiro = pygame.sprite.groupcollide(grupo_tiros, grupo_enemigos, True, True)
        for tiro, enemigos in colisiones_tiro.items():
            puntuacion += len(enemigos)

        pantalla.fill(NEGRO)
        grupo_todos_los_sprites.draw(pantalla)
        pygame.draw.rect(pantalla, VERDE, (10, 10, jugador.vida, 10))
        texto_puntuacion = fuente.render("Puntuación: " + str(puntuacion), True, BLANCO)
        pantalla.blit(texto_puntuacion, (10, 30))
        pygame.display.flip()

        if len(grupo_enemigos) == 0:
            estado_juego = ESTADO_VICTORIA

    elif estado_juego == ESTADO_FIN_JUEGO:
        # Pantalla de Game Over
        pantalla.fill(NEGRO)
        texto_game_over = fuente.render("Game Over", True, ROJO)
        texto_puntuacion_final = fuente.render("Puntuación final: " + str(puntuacion), True, BLANCO)
        texto_instrucciones = fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)
        pantalla.blit(texto_game_over, (ANCHO_PANTALLA // 2 - texto_game_over.get_width() // 2, 200))
        pantalla.blit(texto_puntuacion_final, (ANCHO_PANTALLA // 2 - texto_puntuacion_final.get_width() // 2, 250))
        pantalla.blit(texto_instrucciones, (ANCHO_PANTALLA // 2 - texto_instrucciones.get_width() // 2, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado_juego = ESTADO_MENU
                    jugador.vida = 100
                    puntuacion = 0
                    grupo_enemigos.empty()
                    grupo_tiros.empty()
                    for _ in range(EN):
                        enemigo = Enemigo()
                        grupo_enemigos.add(enemigo)
                        grupo_todos_los_sprites.add(enemigo)

    elif estado_juego == ESTADO_VICTORIA:
        # Pantalla de victoria
        pantalla.fill(NEGRO)
        texto_victoria = fuente.render("¡Ganaste!", True, VERDE)
        texto_puntuacion_final = fuente.render("Puntuación final: " + str(puntuacion), True, BLANCO)
        texto_instrucciones = fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)
        pantalla.blit(texto_victoria, (ANCHO_PANTALLA // 2 - texto_victoria.get_width() // 2, 200))
        pantalla.blit(texto_puntuacion_final, (ANCHO_PANTALLA // 2 - texto_puntuacion_final.get_width() // 2, 250))
        pantalla.blit(texto_instrucciones, (ANCHO_PANTALLA // 2 - texto_instrucciones.get_width() // 2, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    estado_juego = ESTADO_MENU
                    jugador.vida = 100
                    puntuacion = 0
                    grupo_enemigos.empty()
                    grupo_tiros.empty()
                    for _ in range(EN):
                        enemigo = Enemigo()
                        grupo_enemigos.add(enemigo)
                        grupo_todos_los_sprites.add(enemigo)

    reloj.tick(60)

pygame.quit()