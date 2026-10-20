"""
Model 3: Genetic Algorithm (GA)
Supports both Distance-Only and Severity/Urgency-Weighted routing.
"""
import sys
import os
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.dataset import NUM_HOTSPOTS, calculate_tour_cost, two_opt_swap, ALL_NODES, AIRBASE, print_mission_itinerary

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end+1] = parent1[start:end+1]
    
    copied_set = set(child[start:end+1])
    p2_idx = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_idx] in copied_set:
                p2_idx += 1
            child[i] = parent2[p2_idx]
            copied_set.add(parent2[p2_idx])
            p2_idx += 1
    return child

def mutate_inversion(tour, mutation_rate=0.15):
    if random.random() < mutation_rate:
        i, j = sorted(random.sample(range(len(tour)), 2))
        return two_opt_swap(tour, i, j)
    return tour

def genetic_algorithm(pop_size=80, generations=200, tournament_k=3, mutation_rate=0.15, seed=42, num_hotspots=None, alpha=0.0):
    """
    Executes Genetic Algorithm with Elitism, Tournament Selection, Ordered Crossover, and Inversion Mutation.
    alpha > 0 activates fire urgency / severity weighting.
    """
    if seed is not None:
        random.seed(seed)
        
    n_targets = num_hotspots if num_hotspots is not None else NUM_HOTSPOTS
    start_time = time.time()
    
    population = []
    for _ in range(pop_size):
        ind = list(range(1, n_targets + 1))
        random.shuffle(ind)
        population.append(ind)
        
    convergence_history = []
    global_best_tour = None
    global_best_cost = float('inf')
    global_best_dist = float('inf')
    global_best_damage = float('inf')
    
    for gen in range(generations):
        evals = [calculate_tour_cost(ind, alpha=alpha) for ind in population]
        costs = [e[0] for e in evals]
        
        min_cost = min(costs)
        best_idx = costs.index(min_cost)
        
        if min_cost < global_best_cost:
            global_best_cost = min_cost
            global_best_dist = evals[best_idx][1]
            global_best_damage = evals[best_idx][2]
            global_best_tour = population[best_idx].copy()
            
        convergence_history.append(global_best_cost)
        new_population = [global_best_tour.copy()]
        
        while len(new_population) < pop_size:
            t1 = random.sample(list(range(pop_size)), tournament_k)
            p1_idx = min(t1, key=lambda idx: costs[idx])
            parent1 = population[p1_idx]
            
            t2 = random.sample(list(range(pop_size)), tournament_k)
            p2_idx = min(t2, key=lambda idx: costs[idx])
            parent2 = population[p2_idx]
            
            child = ordered_crossover(parent1, parent2)
            child = mutate_inversion(child, mutation_rate)
            new_population.append(child)
            
        population = new_population
        
    elapsed_time = time.time() - start_time
    return global_best_tour, global_best_cost, global_best_dist, global_best_damage, convergence_history, elapsed_time

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.05, help="Urgency factor (0.0 = pure distance, >0 = severity weighted)")
    parser.add_argument("--nodes", type=int, default=15, help="Number of hotspots")
    args = parser.parse_args()
    
    mode_str = "Severity/Urgency-Weighted" if args.alpha > 0 else "Distance-Only"
    print(f"=== Model 3: Genetic Algorithm [{mode_str} Mode] ===")
    tour, cost, dist, damage, _, runtime = genetic_algorithm(alpha=args.alpha, num_hotspots=args.nodes)
    print(f"Algorithm Runtime: {runtime:.4f} seconds")
    
    # Detailed mission telemetry log
    print_mission_itinerary(tour, alpha=args.alpha)
