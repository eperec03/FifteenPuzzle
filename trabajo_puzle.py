#Maneja los argumentos de la línea de comandos (para seleccionar qué algoritmo usar).
import argparse 
#Interactúa con la entrada/salida estándar del sistema operativo (aunque no lo hemos usado explícitamente aún).
import sys
#Estructura eficiente para manejar colas de doble extremo, usada en algoritmos de búsqueda como BFS.
from collections import deque
from queue import Queue

class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.rows = len(initial_state)
        self.cols = len(initial_state[0])
        self.empty_tile = self.find_empty_tile()

    def find_empty_tile(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.initial_state[i][j] == 0:
                    return (i, j)
        return None
    
    #Mostramos el estado actual del puzzle
    def display(self):
        for row in self.initial_state:
            #map(str, row): Esta función convierte cada número en la fila en una cadena de texto. [1, 2, 3] ----> ['1', '2', '3'] 
            #' '.join(...): Une los elementos de la lista con un espacio ' ' como separador. ['1', '2', '3'] ----> '1 2 3'
            print(' '.join(map(str, row)))

    #Comprobamos si el puzzle esta resuelto
    def is_solved(self):
        return self.initial_state == self.goal_state
    
    #Mover una pieza y generar un nuevo estado
    def move(self, direction):
        empty_row, empty_col = self.empty_tile
        # Intentar hacer el movimiento en lugar de crear un nuevo estado
        if direction == 'L' and empty_col > 0:
            self.initial_state[empty_row][empty_col], self.initial_state[empty_row][empty_col - 1] = \
                self.initial_state[empty_row][empty_col - 1], self.initial_state[empty_row][empty_col]
            new_empty_pos = (empty_row, empty_col - 1)
        elif direction == 'R' and empty_col < self.cols - 1:
            self.initial_state[empty_row][empty_col], self.initial_state[empty_row][empty_col + 1] = \
                self.initial_state[empty_row][empty_col + 1], self.initial_state[empty_row][empty_col]
            new_empty_pos = (empty_row, empty_col + 1)
        elif direction == 'U' and empty_row > 0:
            self.initial_state[empty_row][empty_col], self.initial_state[empty_row - 1][empty_col] = \
                self.initial_state[empty_row - 1][empty_col], self.initial_state[empty_row][empty_col]
            new_empty_pos = (empty_row - 1, empty_col)
        elif direction == 'D' and empty_row < self.rows - 1:
            self.initial_state[empty_row][empty_col], self.initial_state[empty_row + 1][empty_col] = \
                self.initial_state[empty_row + 1][empty_col], self.initial_state[empty_row][empty_col]
            new_empty_pos = (empty_row + 1, empty_col)
        else:
            return None, None  # Movimiento no válido

        # Actualiza la posición del tile vacío
        self.empty_tile = new_empty_pos
        return self.initial_state, self.empty_tile


#Búsquedas no informadas
def bfs(puzzle):
    initial_state = puzzle.initial_state
    goal_state = puzzle.goal_state
    empty_tile = puzzle.empty_tile
    #queue almacenará los estados del rompecabezas en un momento específico.
    '''deque crea una cola que permite agregar y remover elementos eficientemente desde ambos extremos'''
    queue = deque([(initial_state, empty_tile, [], None)])  # Agregar el último movimiento
    visited = set()
    visited.add(tuple(map(tuple, initial_state)))

    while queue:
        current_state, (empty_row, empty_col), moves, last_direction = queue.popleft()
        
        # Depuración: Imprimir el estado actual y los movimientos
        print(f"Estado actual: {current_state}, Movimientos: {moves}")
        if current_state == goal_state:
            return moves
        
        for direction in ['L', 'R', 'U', 'D']:
            # Eliminar movimientos inútiles (opuestos)
            if last_direction is not None and ((last_direction == 'L' and direction == 'R') or
                                                (last_direction == 'R' and direction == 'L') or
                                                (last_direction == 'U' and direction == 'D') or
                                                (last_direction == 'D' and direction == 'U')):
                continue
            
            new_puzzle = Puzzle([row[:] for row in current_state], goal_state)  # Copia para el nuevo estado
            new_state, new_empty_pos = new_puzzle.move(direction)
            
            if new_state and tuple(map(tuple, new_state)) not in visited:
                visited.add(tuple(map(tuple, new_state)))
                queue.append((new_state, new_empty_pos, moves + [direction], direction))  # Guardar el último movimiento
    return None
    
def dfs(puzzle):
    pass

def idfs(puzzle):
    pass

#Búsquedas informadas
def best_first_search(puzzle, heuristic):
    pass

def a_star(puzzle, heuristic):
    pass

def sma_star(puzzle, heuristic):
    pass

#Funcion para leer el input del rompecabezas
def read_puzzle():
    #Leer la cantidad de filas y columnas
    rows, cols = map(int, input("Ingrese el número de filas y columnas (ej. 4 4): ").split())
    initial_state = []

    #Leer el estado inicial del puzzle
    for i in range(rows):
        initial_state.append(list(map(int, input().split())))

    return initial_state

#Funcion principal
def main():
    #Definir el obejtivo del puzle 4*4
    goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    #Leer el estado inicial del puzzle
    initial_state = read_puzzle()

    #Crear una instancia del puzzle
    puzzle = Puzzle(initial_state, goal_state)

    #Parsear argumentos de linea de comandos
    #argparse.ArgumentParser(...): Aquí se crea un nuevo objeto ArgumentParser. Este objeto se usa para manejar los argumentos que se pasan al programa desde la línea de comandos. Argumento -h o --help, lo que le dará información sobre cómo usar el programa
    #El objeto parser que creamos se encarga de definr y gestionar los argumentos que el programa recibe en la línea de comandoss
    parser = argparse.ArgumentParser(description='Resuelve el rompecabezas de 15.')
    #add_argument(...) permite especificar los argumentos, sus nombres (corto y largo), la función que tienen, y cómo se deben interpretar.
    parser.add_argument('-b', '--bfs', help='Búsqueda en anchura', action='store_true') #tipo booleano--store_true
    parser.add_argument('-d', '--dfs', help='Búsqueda en profundidad', action='store_true')
    parser.add_argument('-i', '--idfs', help='Búsqueda con profundización iterativa', action='store_true')
    parser.add_argument('-f', '--bf', help='Búsqueda best-first', type=int)
    parser.add_argument('-a', '--astar', help='Algoritmo A*', type=int)
    parser.add_argument('-s', '--sma', help='Algoritmo SMA*', type=int)

    # Inicializar la variable solution
    solution = None
    
    #Esta línea analiza los argumentos que se pasan al programa y los convierte en un objeto (en este caso, args) que contiene los valores de los argumentos especificados.
    #Si el usuario ejecuta el programa con python puzzle_solver.py --bfs, entonces args.bfs será True, mientras que args.dfs, args.idfs, etc., serán False
    args = parser.parse_args()

    #Ejecutar la búsqueda correspondiente según el argumento
    if args.bfs:
        solution = bfs(puzzle)
    elif args.dfs:
        solution = dfs(puzzle)
    elif args.idfs:
        solution = idfs(puzzle)
    elif args.bf is not None:
        solution = best_first_search(puzzle, args.bf)
    elif args.astar is not None:
        solution = a_star(puzzle, args.astar)
        
    elif args.sma is not None:
        solution = sma_star(puzzle, args.sma)
    else:
        print("Debe especificar una estrategia de búsqueda.")
        return

    # Mostrar la solución
    if solution is not None:
        print(f"Número de movimientos: {len(solution)}")  # Número de movimientos
        #Esta línea convierte la lista de movimientos (que están en solution) en una cadena de texto. Solution es una lista que contiene caracteres que representan los movimientos, como ['L', 'R', 'U', 'D']
        print(f"Secuencia de movimientos: {''.join(solution)}")  # Secuencia de movimientos
    else:
        print(-1)  # No hay solución

if __name__ == "__main__":
    main()