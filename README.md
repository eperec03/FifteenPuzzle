#### Fifteen puzzle

"Fifteen puzzle" can be described as a frame with embedded 15 pieces. They can be moved as there is one piece missing in the puzzle and the frame has size 4x4. The goal of the game is to move pieces inside frame in such a way to achieve ordered state, e.g. from initial state:

![[Pasted image 20241021114739.png]]
#### Problem and task

The task presented to groups is to write a program that will solve the puzzle, which mean it will find a sequence of actions that transforms initial state (given as input at program startup) to the final pattern thus solving the puzzle  
Students are expected to implement various searching strategies and compare their characteristics. Comparison must be made basing on exhaustive empirical study. The results should be presented on technical report level (directions will be given during the classes). Following search strategies are compulsory:
* BFS
- DFS
- IDFS
- Best-first search
- A*
- SMA*
Informed search strategies must be tested using at least 2 heuristics. Additionally they should be teted with h(x)=0 heuristic.

#### Functional requirements

It is expected from each group to present two programs. The first one, verifiable in linux/unix environment, reads initial state of a puzzle from standard input and on standard output presents the solution found - sequence of actions solving the puzzle. It is assumed, that letter 'L' denotes a move of a piece having freedom to the left, R to the right, U up, and D down. The program must be parametrised using following command line arguments.


| Argument      | Syntax                  | Description               |
|---------------|-------------------------|---------------------------|
| `-b`, `--bfs` | `-b <order>` or `--bfs <order>` | Executes a Breadth-First Search (BFS) strategy. |
| `-d`, `--dfs` | `-d <order>` or `--dfs <order>` | Executes a Depth-First Search (DFS) strategy. |
| `-i`, `--idfs` | `-i <order>` or `--idfs <order>` | Executes an Iterative Deepening DFS (IDFS) strategy. |
| `-h`, `--bf` | `-h <id_of_heuristic>` or `--bf <id_of_heuristic>` | Executes a Best-First search strategy, using the specified heuristic. |
| `-a`, `--astar` | `-a <id_of_heuristic>` or `--astar <id_of_heuristic>` | Executes an A* search strategy, using the specified heuristic. |
| `-s`, `--sma` | `-s <id_of_heuristic>` or `--sma <id_of_heuristic>` | Executes an SMA* search strategy, using the specified heuristic. |


Where _order_ is a permutation of a set {'L','R','U','D'} defining an order in which successors of given state are processed, e.g. string DULR means the following search order: down, up, left, right. If _order_ starts with 'R' it should be random (each node has random neighborhood search order).

### Input

In the first line of standard input two integer values _R_ _C_ are given: , row count and column count respectively, defining frame size. In each subsequent _R_ lines of standard input contains _C_ space separated integer values describing a piece in the puzzle. Value 0 denotes empty space in the given frame.

### Output

Standard output of a given program should consist of at least two lines. The first line should contain one value _n_: the length of the solution found by the program or -1 if puzzle has not been solved. Second line of standard output should be a string of length _n_ containing uppercase latin characters from set {'L','R', 'U', 'D'} describing the solution. If the solution does not exist the second line should be empty.

## Viewer

Student are also required to present a second application that allows to view previously found solution step by step (with jumps).
