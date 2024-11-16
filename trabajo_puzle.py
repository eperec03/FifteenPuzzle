#Maneja los argumentos de la línea de comandos (para seleccionar qué algoritmo usar).
import argparse 
#Interactúa con la entrada/salida estándar del sistema operativo (aunque no lo hemos usado explícitamente aún).
import sys
#Estructura eficiente para manejar colas de doble extremo, usada en algoritmos de búsqueda como BFS.
from collections import deque
from queue import Queue
import heapq  # Para manejar la cola de prioridad en Best-First Search


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
    max_depth = 10  # Límite de profundidad

    # Pila que almacenará los estados del rompecabezas en un momento específico.
    stack = [(initial_state, empty_tile, [], None)]  # Utilizaremos esta lista como una pila
    visited = []
    visited.append(initial_state)

    while stack:
        # Sacamos el último elemento de la pila (último añadido - LIFO)
        current_state, current_empty_tile, moves, last_move = stack.pop()

        # Depuración: Imprimir el estado actual y los movimientos
        print(f"Estado actual: {current_state}, Movimientos: {moves}")

        # Verificar si se alcanzó el estado objetivo
        if current_state == goal_state:
            return moves

        # Si excede el límite de profundidad, continuar con el siguiente estado
        if len(moves) >= max_depth:
            continue

        # Generar y explorar movimientos posibles
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
def manhattan_distance(state, goal_state):
    # Aquí pasamos el estado actual y el estado objetivo
    distance = 0
    rows, cols = len(state), len(state[0])
    for i in range(rows):
        for j in range(cols):
            if state[i][j] != 0:  # Ignorar el espacio vacío
                value = state[i][j]
                goal_x, goal_y = divmod(value - 1, cols)
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

# Algoritmo Best-First Search
def best_first_search(puzzle):
    """Perform a Best-First Search (Greedy Search) to solve the puzzle using a list instead of heapq."""
    initial_state = puzzle.initial_state
    goal_state = puzzle.goal_state
    empty_tile = puzzle.empty_tile

    # Lista que actúa como la cola de prioridad
    priority_list = [(manhattan_distance(initial_state, goal_state), initial_state, empty_tile, [])]

    visited = set()  # Para evitar ciclos

    while priority_list:
        # Ordenar la lista por heurística (siempre trabajar con el menor costo primero)
        priority_list.sort(key=lambda x: x[0])  # Ordenar por el primer elemento (heurística)
        
        # Sacar el estado con menor heurística
        heuristic, current_state, current_empty_tile, moves = priority_list.pop(0)

        # Depuración: Imprimir el estado actual y su heurística
        print(f"Heurística: {heuristic}, Estado actual: {current_state}, Movimientos: {moves}")

        # Verificar si se alcanzó el estado objetivo
        if current_state == goal_state:
            return moves

        # Marcar el estado actual como visitado
        visited.add(tuple(map(tuple, current_state)))

        # Generar y explorar movimientos posibles
        for direction in puzzle.get_possible_moves(current_empty_tile):
            new_puzzle = Puzzle([row[:] for row in current_state], goal_state)
            new_state, new_empty_pos = new_puzzle.move(direction)

            # Evitar estados visitados previamente
            if tuple(map(tuple, new_state)) not in visited:
                # Calcular la heurística para el nuevo estado
                heuristic = manhattan_distance(new_state, goal_state)
                # Insertar el nuevo estado en la lista
                priority_list.append((heuristic, new_state, new_empty_pos, moves + [direction]))

    # Si no se encuentra solución, devolver None
    return None

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
    parser.add_argument('-f', '--bf', help='Búsqueda best-first', action='store_true')
    parser.add_argument('-a', '--astar', help='Algoritmo A*', action='store_true')
    parser.add_argument('-s', '--sma', help='Algoritmo SMA*', action='store_true')

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
        solution = best_first_search(puzzle)
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
