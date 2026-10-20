# Optimization of Water-Bombing Helicopter Flight Paths for Karhutla Hotspot Suppression

> **Course:** Konsep Kecerdasan Artifisial (Artificial Intelligence Concepts - KKA)  
> **Topic:** Midterm Project - Combinatorial Optimization & Local Search (Lecture 6)  
> **Authors:** Informatics Engineering Student Team  

---

## Summary

During severe dry seasons in Indonesia (particularly in Central Kalimantan and Riau), peatland and forest fires (*Karhutla*) spread at alarming rates. The Aerial Firefighting Task Force (*Satgas Udara Penanggulangan Karhutla - BNPB*) deploys water-bombing helicopters (such as the Kamov Ka-32 or Sikorsky S-61) to drop water on active hotspots (*titik api*).

Operating with limited aviation fuel and water payload capacity, the helicopter must depart from a central airbase, suppress **15 active fire hotspots**, and return to base in the **shortest possible flight distance**. 

This repository formulates the mission as a **Travelling Salesperson Problem (TSP)** and provides an empirical comparative study across three distinct local search / metaheuristic models:
1. **Random-Restart Hill Climbing (with 2-Opt)**
2. **Simulated Annealing (SA)**
3. **Genetic Algorithm (GA)**

---

## Problem Formulation

```
                     [ Airbase (Tjilik Riwut) ]
                              ▲     │
                             /       \
                 [Hotspot 15]         [Hotspot 1]
                      ▲                    │
                      │                    ▼
                 [Hotspot 14] ◄────── [Hotspot 2]
```

* **State Representation:** A closed permutation tour starting and ending at the Airbase:
  $$S = [0, \pi_1, \pi_2, \dots, \pi_N, 0]$$
  where index `0` represents the Airbase, and $\pi$ is a permutation of the 15 hotspot IDs.
* **Objective Function (Minimize):**
  $$\text{Total Distance}(S) = D(0, \pi_1) + \sum_{i=1}^{N-1} D(\pi_i, \pi_{i+1}) + D(\pi_N, 0)$$
  where $D(u, v)$ calculates the great-circle spherical distance using the **Haversine Formula**:
  $$a = \sin^2\left(\frac{\Delta \text{lat}}{2}\right) + \cos(\text{lat}_1)\cos(\text{lat}_2)\sin^2\left(\frac{\Delta \text{lon}}{2}\right)$$
  $$d = 2 R \cdot \text{atan2}(\sqrt{a}, \sqrt{1 - a}), \quad R \approx 6,371\text{ km}$$

---

## Dataset Specification

Real-world geographical coordinates modeled after high-risk peatland fire corridors in **Central Kalimantan (Palangka Raya, Pulang Pisau, and Kapuas)**:

| ID | Location Name | Latitude (°S) | Longitude (°E) | Description |
|:--:|:---|:---:|:---:|:---|
| **0** | **Airbase (Tjilik Riwut)** | `-2.2240` | `113.9460` | Central Command & Refueling Base |
| **1** | Hotspot Sebangau A | `-2.3150` | `113.8920` | National Park peat fire |
| **2** | Hotspot Sebangau B | `-2.3850` | `113.8210` | Swamp forest margin |
| **3** | Hotspot Pulang Pisau 1 | `-2.5210` | `114.0150` | Agricultural peatland |
| **4** | Hotspot Pulang Pisau 2 | `-2.6100` | `114.0890` | Dense smoke zone |
| **5** | Hotspot Kahayan Hilir | `-2.7420` | `114.1560` | Riverbank forest fire |
| **6** | Hotspot Kapuas Barat | `-2.8550` | `114.3120` | Southern perimeter |
| **7** | Hotspot Kapuas Murung | `-2.9300` | `114.4500` | Critical boundary fire |
| **8** | Hotspot Basarang | `-2.7100` | `114.3800` | Peat drainage canal zone |
| **9** | Hotspot Selat | `-2.5500` | `114.4200` | Residential border threat |
| **10** | Hotspot Mantangai 1 | `-2.3900` | `114.4800` | Deep peat fire |
| **11** | Hotspot Mantangai 2 | `-2.1800` | `114.3900` | Eastern flank |
| **12** | Hotspot Timpah | `-2.0500` | `114.2800` | Upriver peat forest |
| **13** | Hotspot Bukit Batu 1 | `-1.9800` | `113.7200` | Northwest foothill |
| **14** | Hotspot Bukit Batu 2 | `-2.0900` | `113.8100` | Secondary scrub fire |
| **15** | Hotspot Rakumpit | `-1.8200` | `113.6500` | Northern frontier hotspot |

---

## Implemented Models

### 1. Random-Restart Hill Climbing (with 2-Opt)
* **Neighborhood Search:** Explores all possible 2-Opt edge swaps (reversing sub-segments $[i, j]$).
* **Escape Strategy:** Whenever trapped at a local optimum where no 2-Opt neighbor improves the route, it **restarts from a new random permutation** (default: 25 restarts), keeping track of the global best.

### 2. Simulated Annealing (SA)
* **Perturbation:** Random 2-Opt swap per step.
* **Metropolis Criterion:**
  * If $\Delta E < 0$ (shorter route): **Always accepted**.
  * If $\Delta E \ge 0$ (longer route): Accepted with probability:
    $$P = \exp\left(-\frac{\Delta E}{T}\right)$$
* **Cooling Schedule:** Geometric decay $T_{k+1} = \alpha \cdot T_k$ with $T_0 = 1000.0$ and $\alpha = 0.995$.

### 3. Genetic Algorithm (GA)
* **Chromosome:** Permutation vector of length 15.
* **Selection:** Tournament Selection ($k = 3$).
* **Crossover:** **Ordered Crossover (OX)** — preserves order and relative position without duplicate visits.
* **Mutation:** Inversion Mutation ($P_m = 0.15$) applied to random slices.
* **Elitism:** The fittest individual of each generation survives untouched.

---

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
├── requirements.txt            # Python dependencies (matplotlib)
└── README.md                   # Project documentation
```

---

## Getting Started

### 1. Prerequisites
Ensure Python 3.8+ is installed. Only `matplotlib` is required for visualization:
```bash
pip install -r requirements.txt
```

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

## Experimental Results (For Chapter 3)

The algorithms were evaluated over **10 independent runs** on the 15-hotspot Karhutla scenario:

| Algorithm Model | Best Distance (km) | Mean Distance (km) | StdDev (km) | Avg Runtime (s) |
|:---|:---:|:---:|:---:|:---:|
| **Random-Restart Hill Climbing** | **355.66** | 355.66 | 0.00 | 0.103 s |
| **Simulated Annealing (SA)** | **355.66** | **355.66** | **0.00** | **0.012 s** ⚡ |
| **Genetic Algorithm (GA)** | **355.66** | 356.39 | 2.18 | 0.390 s |

### Visualizations:
* **Figure 1 (Convergence Curves):** Compares how fast each algorithm minimizes flight distance across search progress.
* **Figure 2 (Flight Trajectories):** 2D geospatial maps comparing the flight loops across the peatland coordinates.

```
Initial Unoptimized Tour : ~1,300 km
Optimized Global Tour    : 355.66 km  (72.6% fuel & flight-time reduction)
```

---

## Key Discussion & Insights

1. **Solution Optimality:**  
   All three algorithms successfully discover the optimal global tour of **$355.66\text{ km}$**. Without optimization, random helicopter routing produces a chaotic path of over $1,300\text{ km}$.
2. **Computational Speed for Real-Time Dispatch:**  
   **Simulated Annealing** converges in just **$0.012\text{ seconds}$**, making it the most suitable engine for dynamic emergency response systems where new hotspots appear mid-mission.
3. **Escaping Local Optima:**  
   While basic Hill Climbing without restarts quickly gets stuck in local traps, adding random restarts allows it to match SA and GA, but at a higher computational cost ($0.103\text{ s}$).

---

## References

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach (4th ed.)*. Pearson. (Chapter 4 & 6: Search in Complex Environments).
2. Badan Nasional Penanggulangan Bencana (BNPB). *Laporan Penanganan Darurat Bencana Kebakaran Hutan dan Lahan (Karhutla)*.
3. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). *Optimization by Simulated Annealing*. Science, 220(4598), 671-680.
4. Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
