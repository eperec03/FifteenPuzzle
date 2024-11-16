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

    def get_possible_moves(self, empty_tile):
        """Returns a list of possible moves (L, R, U, D) for the empty tile based on its current position."""
        row, col = empty_tile
        moves = []
        # Definimos las direcciones en un diccionario:
        directions = {
            "U": (-1, 0),  # Up
            "D": (1, 0),   # Down
            "L": (0, -1),  # Left
            "R": (0, 1)    # Right
        }
        for move, (dr, dc) in directions.items():
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                moves.append(move)
        return moves

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
            #intercambiamos
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
            print('puta')
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
    # queue = deque([(initial_state, empty_tile, [], None)])  # Agregar el último movimiento

    queue = [(initial_state, empty_tile, [], None)]  #utilizaremos esta lista como una pila
    
    visited=[]
    visited.append(initial_state)
    
    while queue:
        current_state, current_empty_tile, moves, last_move = queue.pop(0)  # quitamos el primer elemento de la pila
        
        # Depuración: Imprimir el estado actual y los movimientos
        print(f"Estado actual: {current_state}, Movimientos: {moves}")
        if current_state == goal_state:
            return moves
        
        for direction in puzzle.get_possible_moves(current_empty_tile):
            new_puzzle = Puzzle([row[:] for row in current_state], goal_state)  # Copia para el nuevo estado
            new_state, new_empty_pos = new_puzzle.move(direction)
            
            if new_state not in visited:
                visited.append(new_state)
                queue.append((new_state, new_empty_pos, moves + [direction], direction))  # Guardar el último movimiento
    return None

def dfs(puzzle):
    initial_state = puzzle.initial_state
    goal_state = puzzle.goal_state
    empty_tile = puzzle.empty_tile
    # queue almacenará los estados del rompecabezas en un momento específico.
    stack = [(initial_state, empty_tile, [], None)]  #utilizaremos esta lista como una pila
    visited=[]
    visited.append(initial_state)
    while stack:
        #sacamos el último elemento de la pila, es decirl el último ñadido (deep)
        current_state, current_empty_tile, moves, last_move = stack.pop()
        print(f"Estado actual: {current_state}, Movimientos: {moves}")
        #Depuración: Imprimimir el estado actual y los movimientos
        print(f"Estado actual: {current_state}, Movimientos: {moves}")
        if current_state == goal_state:
            return moves
        for direction in puzzle.get_possible_moves(current_empty_tile):
            new_puzzle = Puzzle([row[:] for row in current_state], goal_state)  # Copia para el nuevo estado
            new_state, new_empty_pos = new_puzzle.move(direction)
            
            if new_state not in visited:
                visited.append(new_state)
                stack.append((new_state, new_empty_pos, moves + [direction], direction))  # Guardar el último movimiento
    return None

def idfs(puzzle):
    # Iterar con profundidades crecientes
    for depth_limit in range(1, sys.maxsize):
        # Indica que el bucle va a iterar con valores de depth_limit que comienzan en 1 y aumentan indefinidamente (sys.maxsize es el valor entero más grande que Python permite)
        # Lista de estados visitados para la profundidad actual
        visited = []
        stack = [(puzzle.initial_state, puzzle.empty_tile, [], 0)]  # Stack simula la pila de llamadas para DFS

        while stack:
            state, empty_tile, moves, depth = stack.pop()
            
            print(f"Profundidad: {depth}, Estado actual: {state}, Movimientos: {moves}")
            
            # Verificar si se alcanzó el objetivo
            if state == puzzle.goal_state:
                return moves
            
            # Ignorar si el límite de profundidad se ha excedido
            if depth > depth_limit:
                continue
            
            # Marcar el estado actual como visitado
            visited.append(state)
            
            # Generar nuevos estados moviendo la pieza vacía
            for direction in puzzle.get_possible_moves(empty_tile):
                new_puzzle = Puzzle([row[:] for row in state], puzzle.goal_state)
                new_state, new_empty_pos = new_puzzle.move(direction)
                
                # Solo apilar el nuevo estado si no se ha visitado en esta iteración
                if new_state is not None and new_state not in visited:
                    stack.append((new_state, new_empty_pos, moves + [direction], depth + 1))
        
    # Si no se encontró solución, retorna None
    return None

#Búsquedas informadas
def manhattan_distance(state):
    """Calculate the Manhattan distance of the current state from the goal state."""
    distance = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != 0:  # Skip the blank tile
                value = state[i][j]
                goal_x, goal_y = divmod(value - 1, 4)
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

# def is_goal(state):
#     """Check if the current state is the goal state."""
#     return state == GOAL_STATE

def get_blank_position(state):
    """Find the position of the blank tile in the puzzle."""
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                return i, j

# def generate_neighbors(state):
#     """Generate all possible moves from the current state."""
#     neighbors = []
#     x, y = get_blank_position(state)
#     for dx, dy in DIRECTIONS:
#         new_x, new_y = x + dx, y + dy
#         if 0 <= new_x < 4 and 0 <= new_y < 4:
#             # Swap blank tile with the adjacent tile
#             new_state = [row[:] for row in state]
#             new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
#             neighbors.append(new_state)
#     return neighbors

# def best_first_search(puzzle):
#     initial_state = 
#     """Perform a Best-First Search (Greedy Search) to solve the 15-puzzle."""
#     priority_queue = []
#     visited = set()
#     heapq.heappush(priority_queue, (manhattan_distance(initial_state), initial_state))

#     while priority_queue:
#         heuristic, current_state = heapq.heappop(priority_queue)

#         # Check if goal is reached
#         if is_goal(current_state):
#             return current_state

#         # Avoid revisiting the same state
#         visited.add(tuple(map(tuple, current_state)))

#         # Explore neighbors
#         for neighbor in generate_neighbors(current_state):
#             neighbor_tuple = tuple(map(tuple, neighbor))
#             if neighbor_tuple not in visited:
#                 heapq.heappush(priority_queue, (manhattan_distance(neighbor), neighbor))
#                 visited.add(neighbor_tuple)

#4 def a_star(puzzle, heuristic):
#     pass

# def sma_star(puzzle, heuristic):
#     pass

# #Funcion para leer el input del rompecabezas
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
    # elif args.bf is not None:
    #     solution = best_first_search(puzzle, args.bf)
    # elif args.astar is not None:
    #     solution = a_star(puzzle, args.astar)
        
    # elif args.sma is not None:
    #     solution = sma_star(puzzle, args.sma)
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
