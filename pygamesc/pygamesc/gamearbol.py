import pygame
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto y Árbol de Decisión")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, fondo
jugador = None
bala = None
fondo = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False

# Lista para guardar los datos
datos_modelo = []

# Modelo entrenado
modelo_arbol = None

# Cargar imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10
frame_count = 0

# Variables para la bala
velocidad_bala = -10
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad

        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

# Función para actualizar el juego
def update():
    global fondo_x1, fondo_x2, frame_count, current_frame

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar el fondo
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(bala_img, (bala.x, bala.y))

    # Mover la bala
    if bala_disparada:
        bala.x += velocidad_bala
    if bala.x < 0:
        reset_bala()

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()

# Función para guardar datos del modelo
def guardar_datos():
    global datos_modelo, jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para generar el modelo de árbol
def generar_arbol():
    global modelo_arbol, datos_modelo
    dataset = pd.DataFrame(datos_modelo, columns=['Velocidad', 'Distancia', 'Salto'])
    X = dataset.iloc[:, :2]
    y = dataset.iloc[:, 2]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo_arbol = DecisionTreeClassifier()
    modelo_arbol.fit(X_train, y_train)

    accuracy = modelo_arbol.score(X_test, y_test)
    print(f"Precisión del modelo: {accuracy:.2f}")

    dot_data = export_graphviz(modelo_arbol, out_file=None,
                               feature_names=['Velocidad', 'Distancia'],
                               class_names=['No Saltar', 'Saltar'],
                               filled=True, rounded=True)
    graph = graphviz.Source(dot_data)
    graph.view()

# Función para el modo automático
def modo_automatico():
    global modelo_arbol, jugador, bala, salto, en_suelo
    if modelo_arbol is None:
        print("Modelo no entrenado.")
        return

    distancia = abs(jugador.x - bala.x)
    entrada = np.array([[velocidad_bala, distancia]])
    prediccion = modelo_arbol.predict(entrada)
    print(f"Predicción: {prediccion[0]}")

    if en_suelo and prediccion[0] == 1:
        salto = True
        manejar_salto()

# Función para reiniciar el juego tras colisión
def reiniciar_juego():
    global menu_activo, bala_disparada
    menu_activo = True
    jugador.x, jugador.y = 50, h - 100
    reset_bala()
    bala_disparada = False
    mostrar_menu()

# Función para mostrar el menú
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, 'G' para Entrenar o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_g:
                    generar_arbol()
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Función principal
def main():
    global salto, en_suelo, bala_disparada, modo_auto

    reloj = pygame.time.Clock()
    mostrar_menu()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:
                    salto = True
                    en_suelo = False

        if not pausa:
            if modo_auto:
                modo_automatico()
            else:
                if salto:
                    manejar_salto()
                guardar_datos()
            if not bala_disparada:
                disparar_bala()
            update()

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
