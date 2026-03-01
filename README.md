# Dynamic Pathfinding Agent

A grid-based pathfinding visualizer using A* and Greedy Best-First Search with dynamic obstacle support.

## Dependencies

- Python 3
- tkinter (comes with Python standard library)

### Install tkinter (Linux)

```
sudo apt-get install python3-tk
```

On Windows/Mac, tkinter is included with the default Python installer.

## How to Run

```
python pathfinder.py
```

Or with a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
python pathfinder.py
```

## Usage

1. Set grid size (Rows and Cols) and click **Create**
2. Set obstacle density and click **Maze** to generate random walls
3. Click on any cell to manually add/remove walls
4. Select algorithm (**A*** or **GBFS**) and heuristic (**Manhattan** or **Euclidean**)
5. Check **Dynamic** to enable random obstacle spawning during navigation
6. Click **Start** to run the search
7. Click **Reset** to clear the grid

## Color Legend

- **Lime** — Start node
- **Red** — Goal node
- **Black** — Walls
- **Light Blue** — Visited nodes
- **Yellow** — Frontier nodes
- **Green** — Final path
- **Orange** — Agent (dynamic mode)
