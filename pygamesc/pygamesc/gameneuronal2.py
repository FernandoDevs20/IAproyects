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
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1 
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

#Modelo entrenado
modelo_entrenado = None

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True
        elif salto_altura <= 0 and not en_suelo:
            # Si la velocidad de salto es 0 o negativa, empezar a caer
            jugador.y += gravedad


# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

#funcion para generar nuestro arbol
def generar_arbol(datos_modelo):

    dataset = pd.DataFrame(datos_modelo, columns=['Feature 1', 'Feature 2', 'Label'])

    # Eliminar columnas innecesarias (como la vacía "Unnamed: 3")
    #dataset = dataset.drop(columns=['Unnamed: 3'])

    # Definir características (X) y etiquetas (y)
    X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
    y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el clasificador de Árbol de Decisión
    clf = DecisionTreeClassifier()

    # Entrenar el modelo
    clf.fit(X_train, y_train)

    # Exportar el árbol de decisión en formato DOT para su visualización
    dot_data = export_graphviz(clf, out_file=None, 
                            feature_names=['Feature 1', 'Feature 2'],  
                            class_names=['Clase 0', 'Clase 1'],  
                            filled=True, rounded=True,  
                            special_characters=True)  

    # Crear el gráfico con graphviz
    graph = graphviz.Source(dot_data)

    # Mostrar el gráfico
    graph.view()

def verificar_caida_completa():
    global salto, en_suelo, salto_altura

    if not en_suelo: 
        manejar_salto() 


#funcion para generar modelo de red neuronal 
def generar_modelo(datos_modelo):
    global modelo_entrenado 
    dataset = pd.DataFrame(datos_modelo, columns=['Feature 1', 'Feature 2', 'Label'])

    # Definir características (X) y etiquetas (y)
    X = dataset.iloc[:, :2]
    y = dataset.iloc[:, 2]

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el modelo de red neuronal multicapa
    model = Sequential([
        Dense(32, input_dim=2, activation='relu'),
        Dense(16, activation='relu'),
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')
    ])


    # Compilar el modelo
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])

    # Entrenar el modelo
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=1)

    # Evaluar el modelo en el conjunto de prueba
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nPrecisión en el conjunto de prueba: {accuracy:.2f}")

    # Probar con un nuevo dato  
    nuevo_dato = np.array([[0.8, 0.3]])  # Ejemplo con características específicas
    prediccion = model.predict(nuevo_dato)
    print(f"Predicción para {nuevo_dato}: {prediccion[0][0]:.2f}")
    modelo_entrenado = model



# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, /n 'M' para Manual,presiona /n 'g' para graficar o 'Q' para Salir", True, BLANCO)
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
                    print("Datos recopilados:", datos_modelo)
                    ##graficar_datos_3d(datos_modelo)
                    generar_modelo(datos_modelo)
                    generar_arbol(datos_modelo)
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

# Función para el modo automático
def modo_automatico():
    global jugador, bala, modelo_entrenado, salto, en_suelo, salto_altura

    if modelo_entrenado is None:
        print("El modelo no está entrenado. Juega en modo manual para recolectar datos.")
        return

    # Verificar si el personaje ha completado su caída
    verificar_caida_completa()

    # Solo predecir si el personaje está en el suelo
    if en_suelo:
        # Preparar las características para la predicción
        distancia = abs(jugador.x - bala.x)
        entrada = np.array([[velocidad_bala, distancia]])

        # Realizar la predicción
        prediccion = modelo_entrenado.predict(entrada, verbose=0)
        print(f"Predicción del modelo: {prediccion[0][0]}")

        # Decidir si saltar
        if prediccion[0][0] > 0.5:  # Umbral de decisión
            salto = True
            en_suelo = False
            manejar_salto()  # Comenzar el salto


# Modificar el ciclo principal para usar ambos modos
def main():
    global salto, en_suelo, bala_disparada, modo_auto

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:  # Salto en modo manual
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            if modo_auto:  # Modo automático
                verificar_caida_completa()
                modo_automatico()
            else:  # Modo manual
                if salto:
                    manejar_salto()
                guardar_datos()  # Guardar datos en modo manual

            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()