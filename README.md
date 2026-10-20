# Optimization of Water-Bombing Helicopter Flight Paths for Karhutla Hotspot Suppression

> **Course:** Konsep Kecerdasan Artifisial (Artificial Intelligence Concepts - KKA)  
> **Topic:** Midterm Project - Combinatorial Optimization & Local Search (Lecture 6)  
> **Authors:** Informatics Engineering Student Team  

## Repository Structure

```
karhutla_firefighter_project/
├── data/
│   └── dataset.py              # Coordinate data, Haversine distance & 2-opt operator
├── algorithms/
│   ├── hill_climbing.py        # Model 1: Random-Restart Hill Climbing
│   ├── simulated_annealing.py  # Model 2: Simulated Annealing
│   └── genetic_algorithm.py    # Model 3: Genetic Algorithm
├── main.py                     # Benchmark runner & visual plot generator
└── README.md                   # Project documentation
```


## Getting Started

### 1. Prerequisites
Ensure Python 3.8+ is installed. Only `matplotlib` is required for visualization.

### 2. Running Individual Algorithms
Each model is completely standalone and can be executed independently:

* **Run Model 1 (Hill Climbing):**
  ```bash
  python algorithms/hill_climbing.py
  ```
* **Run Model 2 (Simulated Annealing):**
  ```bash
  python algorithms/simulated_annealing.py
  ```
* **Run Model 3 (Genetic Algorithm):**
  ```bash
  python algorithms/genetic_algorithm.py
  ```

### 3. Running the Full Comparative Benchmark
To run the full 10-trial statistical evaluation and auto-generate the visualization charts:
```bash
python main.py
```

---
