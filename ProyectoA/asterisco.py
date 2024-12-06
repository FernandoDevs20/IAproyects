import pygame
import time 

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A*")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)

# Implementación de la Cola de Prioridad
class lista_abierta_class:
    def __init__(self):
        self.elements = []

    def put(self, item, priority):
        self.elements.append((priority, item))
        self.elements.sort(key=lambda x: x[0])  # Ordenar por prioridad

    def get(self):
        return self.elements.pop(0)[1]  # Sacar el elemento con menor prioridad

    def empty(self):
        return len(self.elements) == 0


class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf")
        self.h = 0
        self.vecinos = []
        self.padre = None
        self.esPared = False

    def __lt__(self, otro):
        return (self.g + self.h) < (otro.g + otro.h)

    def get_pos(self):
        return self.fila, self.col

    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = 0
        self.padre = None
        self.esPared = False

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO
        self.esPared = True

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_camino(self):
        self.color = VERDE

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def buscar_vecinos(self, grid):
        self.vecinos = []
        direcciones = [
            (1, 0),  # Abajo
            (-1, 0),  # Arriba
            (0, 1),  # Derecha
            (0, -1),  # Izquierda
            (1, 1),  # Abajo derecha
            (1, -1),  # Abajo izquierda
            (-1, 1),  # Arriba derecha
            (-1, -1),  # Arriba izquierda
        ]
        for dx, dy in direcciones:
            nueva_fila, nueva_col = self.fila + dx, self.col + dy
            if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                vecino = grid[nueva_fila][nueva_col]
                if not vecino.esPared:
                    self.vecinos.append(vecino)


def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid


def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))


def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()


def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col


def heuristica(nodo1, nodo2):
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return 10 * (abs(x1 - x2) + abs(y1 - y2))  # Distancia Manhattan (solo horizontal y vertical)


def a_star(grid, inicio, fin):
    lista_abierta = lista_abierta_class()
    lista_cerrada = []
    lista_abierta.put(inicio, 0)
    inicio.g = 0
    inicio.h = heuristica(inicio, fin)

    while not lista_abierta.empty():
        time.sleep(0.1)
        current = lista_abierta.get()
        lista_cerrada.append(current)

        if current == fin:
            print(f"Lista cerrada: {[n.get_pos() for n in lista_cerrada]}")
            path = []
            while current.padre:
                path.append(current)
                current = current.padre
            return path[::-1]

        current.buscar_vecinos(grid)

        for vecino in current.vecinos:
            if vecino.esPared or vecino in lista_cerrada:
                continue

            # Verifica si el movimiento es diagonal
            movimiento_diagonal = abs(current.fila - vecino.fila) == 1 and abs(current.col - vecino.col) == 1
            costo_movimiento = 14 if movimiento_diagonal else 10
            temp_g = current.g + costo_movimiento

            if temp_g < vecino.g:
                vecino.padre = current
                vecino.g = temp_g
                vecino.h = heuristica(vecino, fin)
                lista_abierta.put(vecino, vecino.g + vecino.h)

        current.hacer_cerrado()
        dibujar(VENTANA, grid, len(grid), ANCHO_VENTANA)

    return []


def main(ventana, ancho):
    FILAS = 9
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True
    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Clic izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Clic derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    path = a_star(grid, inicio, fin)
                    if path == []:
                        print("No hay camino")
                    else:
                        print(f"camino: {[n.get_pos() for n in path]}")
                        for nodo in path:
                            nodo.hacer_camino()
                            dibujar(VENTANA, grid, FILAS, ANCHO_VENTANA)

                if event.key == pygame.K_r:  # Reiniciar
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()


main(VENTANA, ANCHO_VENTANA)
