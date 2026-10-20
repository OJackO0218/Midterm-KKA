"""
Model 1: Random-Restart Hill Climbing (with 2-Opt)
Supports both Distance-Only and Severity/Urgency-Weighted routing.
"""
import sys
import os
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.dataset import NUM_HOTSPOTS, calculate_tour_cost, two_opt_swap, ALL_NODES, AIRBASE, print_mission_itinerary

def random_restart_hill_climbing(num_restarts=25, max_steps_per_restart=200, seed=42, num_hotspots=None, alpha=0.0):
    """
    Executes Steepest-Ascent Hill Climbing with Random Restarts.
    alpha > 0 activates fire urgency / severity weighting.
    """
    if seed is not None:
        random.seed(seed)
        
    n_targets = num_hotspots if num_hotspots is not None else NUM_HOTSPOTS
    start_time = time.time()
    global_best_tour = None
    global_best_cost = float('inf')
    global_best_dist = float('inf')
    global_best_damage = float('inf')
    convergence_history = []
    
    for r in range(num_restarts):
        current_tour = list(range(1, n_targets + 1))
        random.shuffle(current_tour)
        current_cost, current_dist, current_damage = calculate_tour_cost(current_tour, alpha=alpha)
        
        if current_cost < global_best_cost:
            global_best_cost = current_cost
            global_best_dist = current_dist
            global_best_damage = current_damage
            global_best_tour = current_tour.copy()
        convergence_history.append(global_best_cost)
        
        step = 0
        improved = True
        
        while improved and step < max_steps_per_restart:
            improved = False
            best_neighbor = None
            best_neighbor_cost = current_cost
            best_neighbor_dist = current_dist
            best_neighbor_damage = current_damage
            
            n = len(current_tour)
            for i in range(n - 1):
                for j in range(i + 1, n):
                    neighbor = two_opt_swap(current_tour, i, j)
                    neighbor_cost, neighbor_dist, neighbor_damage = calculate_tour_cost(neighbor, alpha=alpha)
                    
                    if neighbor_cost < best_neighbor_cost:
                        best_neighbor_cost = neighbor_cost
                        best_neighbor_dist = neighbor_dist
                        best_neighbor_damage = neighbor_damage
                        best_neighbor = neighbor
            
            if best_neighbor is not None and best_neighbor_cost < current_cost:
                current_tour = best_neighbor
                current_cost = best_neighbor_cost
                current_dist = best_neighbor_dist
                current_damage = best_neighbor_damage
                improved = True
                step += 1
                
                if current_cost < global_best_cost:
                    global_best_cost = current_cost
                    global_best_dist = current_dist
                    global_best_damage = current_damage
                    global_best_tour = current_tour.copy()
                    
            convergence_history.append(global_best_cost)
            
    elapsed_time = time.time() - start_time
    return global_best_tour, global_best_cost, global_best_dist, global_best_damage, convergence_history, elapsed_time

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.05, help="Urgency factor (0.0 = pure distance, >0 = severity weighted)")
    parser.add_argument("--nodes", type=int, default=15, help="Number of hotspots")
    args = parser.parse_args()
    
    mode_str = "Severity/Urgency-Weighted" if args.alpha > 0 else "Distance-Only"
    print(f"=== Model 1: Random-Restart Hill Climbing [{mode_str} Mode] ===")
    tour, cost, dist, damage, _, runtime = random_restart_hill_climbing(alpha=args.alpha, num_hotspots=args.nodes)
    print(f"Algorithm Runtime: {runtime:.4f} seconds")
    
    # Detailed mission telemetry log
    print_mission_itinerary(tour, alpha=args.alpha)
