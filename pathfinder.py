import tkinter as tk
from tkinter import ttk
import heapq
import random
import time


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.walls = set()
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)

    def reset(self):
        self.walls = set()

    def generate_maze(self, density):
        self.walls = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) != self.start and (r, c) != self.goal:
                    if random.random() < density:
                        self.walls.add((r, c))

    def toggle_wall(self, r, c):
        if (r, c) == self.start or (r, c) == self.goal:
            return
        if (r, c) in self.walls:
            self.walls.remove((r, c))
        else:
            self.walls.add((r, c))

    def get_neighbors(self, node):
        r, c = node
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.walls


class Heuristics:
    @staticmethod
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def euclidean(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


class SearchAlgorithm:
    def __init__(self, grid, heuristic_fn):
        self.grid = grid
        self.heuristic = heuristic_fn
        self.visited = set()
        self.frontier_set = set()
        self.came_from = {}
        self.cost_so_far = {}
        self.nodes_visited = 0

    def gbfs(self, start, goal):
        self.visited = set()
        self.frontier_set = set()
        self.came_from = {}
        self.nodes_visited = 0
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start, goal), start))
        self.frontier_set.add(start)
        self.came_from[start] = None

        while frontier:
            _, current = heapq.heappop(frontier)
            self.frontier_set.discard(current)

            if current in self.visited:
                continue

            self.visited.add(current)
            self.nodes_visited += 1

            if current == goal:
                return True

            for neighbor in self.grid.get_neighbors(current):
                if neighbor not in self.visited:
                    self.came_from[neighbor] = current
                    heapq.heappush(frontier, (self.heuristic(neighbor, goal), neighbor))
                    self.frontier_set.add(neighbor)

        return False

    def astar(self, start, goal):
        self.visited = set()
        self.frontier_set = set()
        self.came_from = {}
        self.cost_so_far = {}
        self.nodes_visited = 0
        frontier = []
        heapq.heappush(frontier, (0, start))
        self.frontier_set.add(start)
        self.came_from[start] = None
        self.cost_so_far[start] = 0

        while frontier:
            _, current = heapq.heappop(frontier)
            self.frontier_set.discard(current)

            if current in self.visited:
                continue

            self.visited.add(current)
            self.nodes_visited += 1

            if current == goal:
                return True

            for neighbor in self.grid.get_neighbors(current):
                new_cost = self.cost_so_far[current] + 1
                if neighbor not in self.cost_so_far or new_cost < self.cost_so_far[neighbor]:
                    self.cost_so_far[neighbor] = new_cost
                    f = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (f, neighbor))
                    self.frontier_set.add(neighbor)
                    self.came_from[neighbor] = current

        return False

    def reconstruct_path(self, start, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = self.came_from.get(current)
        path.reverse()
        if path[0] == start:
            return path
        return []


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinder")
        self.cell_size = 25
        self.grid = None
        self.search = None
        self.dynamic_mode = False
        self.running = False
        self.path = []
        self.agent_pos = None
        self.setup_ui()

    def setup_ui(self):
        pass

    def create_grid(self):
        pass

    def generate_maze(self):
        pass

    def draw_grid(self):
        pass

    def draw_cell(self, r, c, color):
        pass

    def on_cell_click(self, event):
        pass

    def start_search(self):
        pass

    def run_search(self):
        pass

    def animate_path(self):
        pass

    def spawn_dynamic_obstacles(self):
        pass

    def replan(self):
        pass

    def update_metrics(self, nodes, cost, time_ms):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
