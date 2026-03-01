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
        control = tk.Frame(self.root)
        control.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Label(control, text="Rows:").pack(side=tk.LEFT)
        self.rows_var = tk.StringVar(value="15")
        tk.Entry(control, textvariable=self.rows_var, width=4).pack(side=tk.LEFT)

        tk.Label(control, text="Cols:").pack(side=tk.LEFT)
        self.cols_var = tk.StringVar(value="15")
        tk.Entry(control, textvariable=self.cols_var, width=4).pack(side=tk.LEFT)

        tk.Button(control, text="Create", command=self.create_grid).pack(side=tk.LEFT, padx=3)

        tk.Label(control, text="Density:").pack(side=tk.LEFT)
        self.density_var = tk.StringVar(value="0.3")
        tk.Entry(control, textvariable=self.density_var, width=4).pack(side=tk.LEFT)
        tk.Button(control, text="Maze", command=self.generate_maze).pack(side=tk.LEFT, padx=3)

        self.algo_var = tk.StringVar(value="A*")
        ttk.Combobox(control, textvariable=self.algo_var, values=["A*", "GBFS"], width=5, state="readonly").pack(side=tk.LEFT, padx=3)

        self.heur_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(control, textvariable=self.heur_var, values=["Manhattan", "Euclidean"], width=9, state="readonly").pack(side=tk.LEFT, padx=3)

        self.dynamic_var = tk.BooleanVar(value=False)
        tk.Checkbutton(control, text="Dynamic", variable=self.dynamic_var).pack(side=tk.LEFT, padx=3)

        tk.Button(control, text="Start", command=self.start_search).pack(side=tk.LEFT, padx=3)
        tk.Button(control, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=3)

        self.metrics_label = tk.Label(self.root, text="Nodes: 0 | Cost: 0 | Time: 0 ms")
        self.metrics_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.on_cell_click)

        self.create_grid()

    def create_grid(self):
        rows = int(self.rows_var.get())
        cols = int(self.cols_var.get())
        self.grid = Grid(rows, cols)
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)
        self.path = []
        self.running = False
        self.draw_grid()

    def generate_maze(self):
        if self.grid is None:
            return
        density = float(self.density_var.get())
        self.grid.generate_maze(density)
        self.path = []
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if (r, c) == self.grid.start:
                    color = "lime"
                elif (r, c) == self.grid.goal:
                    color = "red"
                elif (r, c) in self.grid.walls:
                    color = "black"
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def draw_cell(self, r, c, color):
        x1 = c * self.cell_size
        y1 = r * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def on_cell_click(self, event):
        if self.grid is None or self.running:
            return
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
            self.grid.toggle_wall(r, c)
            self.draw_grid()

    def start_search(self):
        if self.grid is None or self.running:
            return
        self.running = True
        self.dynamic_mode = self.dynamic_var.get()
        if self.heur_var.get() == "Manhattan":
            h = Heuristics.manhattan
        else:
            h = Heuristics.euclidean
        self.search = SearchAlgorithm(self.grid, h)
        self.draw_grid()
        self.run_search()

    def run_search(self):
        start = self.grid.start
        goal = self.grid.goal
        if self.agent_pos:
            start = self.agent_pos

        algo = self.algo_var.get()
        t1 = time.time()
        if algo == "A*":
            found = self.search.astar(start, goal)
        else:
            found = self.search.gbfs(start, goal)
        t2 = time.time()

        for node in self.search.visited:
            if node != self.grid.start and node != self.grid.goal:
                self.draw_cell(node[0], node[1], "lightblue")
        for node in self.search.frontier_set:
            if node != self.grid.start and node != self.grid.goal:
                self.draw_cell(node[0], node[1], "yellow")

        if found:
            self.path = self.search.reconstruct_path(start, goal)
            for node in self.path:
                if node != self.grid.start and node != self.grid.goal:
                    self.draw_cell(node[0], node[1], "green")
            self.update_metrics(self.search.nodes_visited, len(self.path) - 1, (t2 - t1) * 1000)
            if self.dynamic_mode:
                self.agent_pos = start
                self.animate_path()
            else:
                self.running = False
        else:
            self.update_metrics(self.search.nodes_visited, 0, (t2 - t1) * 1000)
            self.running = False

    def animate_path(self):
        if not self.path:
            self.running = False
            return
        self.agent_pos = self.path.pop(0)
        self.draw_grid()
        for node in self.search.visited:
            if node != self.grid.start and node != self.grid.goal:
                self.draw_cell(node[0], node[1], "lightblue")
        for node in self.path:
            if node != self.grid.start and node != self.grid.goal:
                self.draw_cell(node[0], node[1], "green")
        self.draw_cell(self.agent_pos[0], self.agent_pos[1], "orange")

        if self.agent_pos == self.grid.goal:
            self.running = False
            return

        self.spawn_dynamic_obstacles()
        self.root.after(100, self.animate_path)

    def spawn_dynamic_obstacles(self):
        blocked = False
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                if (r, c) not in self.grid.walls and (r, c) != self.grid.start and (r, c) != self.grid.goal and (r, c) != self.agent_pos:
                    if random.random() < 0.01:
                        self.grid.walls.add((r, c))
                        if (r, c) in self.path:
                            blocked = True
        if blocked:
            self.replan()

    def replan(self):
        if self.heur_var.get() == "Manhattan":
            h = Heuristics.manhattan
        else:
            h = Heuristics.euclidean
        self.search = SearchAlgorithm(self.grid, h)
        algo = self.algo_var.get()
        if algo == "A*":
            found = self.search.astar(self.agent_pos, self.grid.goal)
        else:
            found = self.search.gbfs(self.agent_pos, self.grid.goal)
        if found:
            self.path = self.search.reconstruct_path(self.agent_pos, self.grid.goal)
        else:
            self.path = []

    def update_metrics(self, nodes, cost, time_ms):
        self.metrics_label.config(text=f"Nodes: {nodes} | Cost: {cost} | Time: {time_ms:.2f} ms")

    def reset(self):
        self.running = False
        self.path = []
        self.agent_pos = None
        if self.grid:
            self.grid.reset()
            self.draw_grid()
        self.update_metrics(0, 0, 0)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
