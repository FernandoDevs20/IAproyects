import pygame

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("A* Simplificado Proyecto1")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        self.color = VERDE

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

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

def obtener_vecinos(nodo, grid):
    vecinos = []
    fila, col = nodo.get_pos()

    if fila > 0 and not grid[fila - 1][col].es_pared():  # Arriba
        vecinos.append(grid[fila - 1][col])

    if fila < nodo.total_filas - 1 and not grid[fila + 1][col].es_pared():  # Abajo
        vecinos.append(grid[fila + 1][col])

    if col > 0 and not grid[fila][col - 1].es_pared():  # Izquierda
        vecinos.append(grid[fila][col - 1])

    if col < nodo.total_filas - 1 and not grid[fila][col + 1].es_pared():  # Derecha
        vecinos.append(grid[fila][col + 1])

    return vecinos

def heuristica(nodo_actual, nodo_final):
    x1, y1 = nodo_actual.get_pos()
    x2, y2 = nodo_final.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)  # Distancia Manhattan

def a_star(dibujar, grid, inicio, fin):
    abiertos = [inicio]  # Lista de nodos por evaluar
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio, fin)

    while abiertos:
        # Encuentra el nodo con el menor f_score
        current = min(abiertos, key=lambda nodo: f_score[nodo])

        if current == fin:
            while current in came_from:
                current = came_from[current]
                current.hacer_camino()
                dibujar()
            return True

        abiertos.remove(current)

        for vecino in obtener_vecinos(current, grid):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[vecino]:
                came_from[vecino] = current
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino, fin)

                if vecino not in abiertos:
                    abiertos.append(vecino)

        dibujar()
        if current != inicio:
            current.hacer_camino()

    return False

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
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

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
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
                    a_star(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)