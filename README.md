# AI Pacman Search Algorithms

The goal of this project is to teach an autonomous Pac-Man agent to plan or optimal or near-optimal paths through mazes using different search algorithms.
I implemented each algorithm, built admissible and consistent heuristics, and produced a fully functional agent that clears every supplied layout within the performance thresholds laid out in the specification.

## Repository Layout

| Path              | Purpose                                                                |
| ----------------- | ---------------------------------------------------------------------- |
| `search.py`       | Core graph‑search framework + DFS, BFS, UCS, A\* implementations       |
| `searchAgents.py` | All custom Pac‑Man agents, Corners / Food search problems & heuristics |
| `pacman.py`       | _Unmodified_ game driver provided by the instructors                   |
| `util.py`         | Priority queues & helper data structures (provided)                    |
| `commands.txt`    | Handy one‑liner commands for quick testing                             |

> **Note:** _Only_ `search.py` and `searchAgents.py` were edited; every other file is stock so grading scripts run as expected.

---

## Quick Start

1. **Clone & enter** the repo:

    ```bash
    git clone git@github.com:kzeen/ai-pacman.git
    cd ai-pacman
    ```

2. **Run a tiny test** (Depth‑First Search):

    ```bash
    python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
    ```

3. **Benchmark A\*** on the largest layout supplied:

    ```bash
    python pacman.py -l bigMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic -z 0.5
    ```

Python ≥ 3.8 is sufficient; the project has **no external dependencies**.

---

## 🧠 Algorithms & Heuristics Implemented

| Feature                   | File                               | Highlights                                                                                     |
| ------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Depth‑First Search**    | `search.py` → `depthFirstSearch`   | Graph‑search variant avoids re‑expansion; solution length 130 on `mediumMaze`.                 |
| **Breadth‑First Search**  | `search.py` → `breadthFirstSearch` | Guarantees optimal path by queue discipline; 268 nodes on `mediumMaze`.                        |
| **Uniform‑Cost Search**   | `search.py` → `uniformCostSearch`  | Cost‑sensitive fringe ordering via `PriorityQueue`.                                            |
| **A\***                   | `search.py` → `aStarSearch`        | Modular heuristic injection; tie‑breaking keeps expansions deterministic.                      |
| **CornersProblem**        | `searchAgents.py`                  | State = `(pos, visitedCornersMask)` → 29 ×  faster than naive GameState search.                |
| **`cornersHeuristic`**    | `searchAgents.py`                  | Minimum spanning tree + manhattan lower‑bounds; ≤ 1 200 nodes on `mediumCorners`.              |
| **FoodSearchProblem**     | `searchAgents.py`                  | Collect all pellets; positions encoded as `(pos, foodGridBits)`.                               |
| **`foodHeuristic`**       | `searchAgents.py`                  | Max{mazeDist(current, pellet), average pairwise pellet dist}; ≤ 9 000 nodes on `trickySearch`. |
| **ClosestDotSearchAgent** | `searchAgents.py`                  | Greedy sub‑optimal baseline; completes `bigSearch` < 0.8 s, cost ≈ 350.                        |

All heuristics are **admissible & consistent** – verified by equality of UCS vs A\* path costs and monotone `f`‑values during expansion.

---

## 📈 Performance Snapshots

| Layout             | Agent                    | Expanded Nodes | Path Cost |
| ------------------ | ------------------------ | -------------- | --------- |
| `mediumMaze`       | DFS                      | 1 090          | 130       |
| `mediumMaze`       | BFS                      | **268**        | **68**    |
| `mediumDottedMaze` | StayEast (UCS)           | 550            | 199       |
| `bigMaze`          | A\* + Manhattan          | **549**        | **162**   |
| `mediumCorners`    | A\* + `cornersHeuristic` | **1 155**      | **98**    |
| `trickySearch`     | A\* + `foodHeuristic`    | **8 734**      | **124**   |

_(Counts measured with `--frameTime 0` on an Apple M4; numbers may vary slightly.)_

---

## 🙏 Acknowledgements

The assignment skeleton and sprites are © UC Berkeley & Pacman AI authors **J. DeNero, D. Klein, P. Abbeel**.
This solution is my original work developed for the **CSC460 AI** course at the **Lebanese American University**.
