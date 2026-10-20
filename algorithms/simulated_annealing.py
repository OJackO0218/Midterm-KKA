"""
Model 2: Simulated Annealing (SA)
Supports both Distance-Only and Severity/Urgency-Weighted routing.
"""
import sys
import os
import math
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.dataset import NUM_HOTSPOTS, calculate_tour_cost, two_opt_swap, ALL_NODES, AIRBASE, print_mission_itinerary

def simulated_annealing(initial_temp=1000.0, cooling_rate=0.995, min_temp=0.01, max_iter=3000, seed=42, num_hotspots=None, alpha=0.0):
    """
    Executes Simulated Annealing with geometric cooling schedule and 2-opt perturbations.
    alpha > 0 activates fire urgency / severity weighting.
    """
    if seed is not None:
        random.seed(seed)
        
    n_targets = num_hotspots if num_hotspots is not None else NUM_HOTSPOTS
    start_time = time.time()
    current_tour = list(range(1, n_targets + 1))
    random.shuffle(current_tour)
    current_cost, current_dist, current_damage = calculate_tour_cost(current_tour, alpha=alpha)
    
    best_tour = current_tour.copy()
    best_cost = current_cost
    best_dist = current_dist
    best_damage = current_damage
    
    T = initial_temp
    convergence_history = []
    n = len(current_tour)
    
    for iteration in range(max_iter):
        if T <= min_temp:
            break
            
        i = random.randint(0, n - 2)
        j = random.randint(i + 1, n - 1)
        neighbor = two_opt_swap(current_tour, i, j)
        neighbor_cost, neighbor_dist, neighbor_damage = calculate_tour_cost(neighbor, alpha=alpha)
        
        delta_E = neighbor_cost - current_cost
        
        # Metropolis acceptance criterion
        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            current_tour = neighbor
            current_cost = neighbor_cost
            current_dist = neighbor_dist
            current_damage = neighbor_damage
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_dist = current_dist
                best_damage = current_damage
                best_tour = current_tour.copy()
                
        convergence_history.append(best_cost)
        T *= cooling_rate
        
    elapsed_time = time.time() - start_time
    return best_tour, best_cost, best_dist, best_damage, convergence_history, elapsed_time

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.05, help="Urgency factor (0.0 = pure distance, >0 = severity weighted)")
    parser.add_argument("--nodes", type=int, default=15, help="Number of hotspots")
    args = parser.parse_args()
    
    mode_str = "Severity/Urgency-Weighted" if args.alpha > 0 else "Distance-Only"
    print(f"=== Model 2: Simulated Annealing [{mode_str} Mode] ===")
    tour, cost, dist, damage, _, runtime = simulated_annealing(alpha=args.alpha, num_hotspots=args.nodes)
    print(f"Algorithm Runtime: {runtime:.4f} seconds")
    
    # Detailed mission telemetry log
    print_mission_itinerary(tour, alpha=args.alpha)
