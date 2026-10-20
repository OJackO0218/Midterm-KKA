"""
Main Execution & Benchmark Script
Supports Distance-Only (alpha=0.0) vs. Fire Urgency/Severity-Weighted (alpha>0.0) optimization.
Generates convergence graphs and satellite-styled flight trajectory maps with hotspot severity markers.
"""
import os
import argparse
import math
import matplotlib.pyplot as plt

from data.dataset import load_dataset, ALL_NODES, AIRBASE, HOTSPOTS, NUM_HOTSPOTS, print_mission_itinerary
from algorithms.hill_climbing import random_restart_hill_climbing
from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic_algorithm import genetic_algorithm

def run_single_demo(num_hotspots=NUM_HOTSPOTS, alpha=0.0):
    mode_desc = "Urgency/Severity-Weighted" if alpha > 0 else "Distance-Only"
    print(f"=== Water-Bombing Helicopter Mission Demo ({num_hotspots} Hotspots | Mode: {mode_desc}) ===")
    
    print("\n1. Running Random-Restart Hill Climbing...")
    hc_tour, hc_cost, hc_dist, hc_dmg, hc_hist, hc_time = random_restart_hill_climbing(num_hotspots=num_hotspots, alpha=alpha)
    print(f"   -> Flight Distance: {hc_dist:.2f} km | Forest Damage: {hc_dmg:.1f} | Runtime: {hc_time:.4f}s")
    
    print("\n2. Running Simulated Annealing...")
    sa_tour, sa_cost, sa_dist, sa_dmg, sa_hist, sa_time = simulated_annealing(num_hotspots=num_hotspots, alpha=alpha)
    print(f"   -> Flight Distance: {sa_dist:.2f} km | Forest Damage: {sa_dmg:.1f} | Runtime: {sa_time:.4f}s")
    
    print("\n3. Running Genetic Algorithm...")
    ga_tour, ga_cost, ga_dist, ga_dmg, ga_hist, ga_time = genetic_algorithm(num_hotspots=num_hotspots, alpha=alpha)
    print(f"   -> Flight Distance: {ga_dist:.2f} km | Forest Damage: {ga_dmg:.1f} | Runtime: {ga_time:.4f}s")
    
    # Identify and print detailed itinerary of the winning tour
    best_candidate = min(
        [("Simulated Annealing", sa_tour, sa_cost), 
         ("Random-Restart Hill Climbing", hc_tour, hc_cost), 
         ("Genetic Algorithm", ga_tour, ga_cost)], 
        key=lambda x: x[2]
    )
    print(f"\n>>> Best Optimized Mission Itinerary ({best_candidate[0]}):")
    print_mission_itinerary(best_candidate[1], alpha=alpha)
    
    return (hc_tour, hc_cost, hc_dist, hc_dmg, hc_hist), (sa_tour, sa_cost, sa_dist, sa_dmg, sa_hist), (ga_tour, ga_cost, ga_dist, ga_dmg, ga_hist)

def run_benchmark(num_trials=10, num_hotspots=NUM_HOTSPOTS, alpha=0.0):
    mode_desc = "Urgency-Weighted" if alpha > 0 else "Distance-Only"
    print(f"\n=== Running {num_trials}-Trial Statistical Benchmark ({num_hotspots} Hotspots | {mode_desc}) ===")
    results = {
        "Random-Restart Hill Climbing": {"distances": [], "damages": [], "costs": [], "times": []},
        "Simulated Annealing":          {"distances": [], "damages": [], "costs": [], "times": []},
        "Genetic Algorithm":            {"distances": [], "damages": [], "costs": [], "times": []}
    }
    
    for t in range(num_trials):
        seed = 100 + t
        # HC
        _, c, d, dmg, _, tm = random_restart_hill_climbing(seed=seed, num_hotspots=num_hotspots, alpha=alpha)
        results["Random-Restart Hill Climbing"]["costs"].append(c)
        results["Random-Restart Hill Climbing"]["distances"].append(d)
        results["Random-Restart Hill Climbing"]["damages"].append(dmg)
        results["Random-Restart Hill Climbing"]["times"].append(tm)
        
        # SA
        _, c, d, dmg, _, tm = simulated_annealing(seed=seed, num_hotspots=num_hotspots, alpha=alpha)
        results["Simulated Annealing"]["costs"].append(c)
        results["Simulated Annealing"]["distances"].append(d)
        results["Simulated Annealing"]["damages"].append(dmg)
        results["Simulated Annealing"]["times"].append(tm)
        
        # GA
        _, c, d, dmg, _, tm = genetic_algorithm(seed=seed, num_hotspots=num_hotspots, alpha=alpha)
        results["Genetic Algorithm"]["costs"].append(c)
        results["Genetic Algorithm"]["distances"].append(d)
        results["Genetic Algorithm"]["damages"].append(dmg)
        results["Genetic Algorithm"]["times"].append(tm)
        
    print("\n" + "="*88)
    if alpha > 0:
        print(f"{'Algorithm Model':<30} | {'Best Cost':<10} | {'Dist (km)':<10} | {'Damage':<10} | {'Avg Time (s)':<12}")
    else:
        print(f"{'Algorithm Model':<30} | {'Best (km)':<10} | {'Mean (km)':<10} | {'StdDev':<8} | {'Avg Time (s)':<12}")
    print("="*88)
    
    for model_name, data in results.items():
        avg_tm = sum(data["times"]) / num_trials
        if alpha > 0:
            best_c = min(data["costs"])
            idx = data["costs"].index(best_c)
            d_val = data["distances"][idx]
            dmg_val = data["damages"][idx]
            print(f"{model_name:<30} | {best_c:<10.2f} | {d_val:<10.2f} | {dmg_val:<10.1f} | {avg_tm:<12.3f}")
        else:
            best_d = min(data["distances"])
            mean_d = sum(data["distances"]) / num_trials
            std_d = math.sqrt(sum((x - mean_d)**2 for x in data["distances"]) / num_trials)
            print(f"{model_name:<30} | {best_d:<10.2f} | {mean_d:<10.2f} | {std_d:<8.2f} | {avg_tm:<12.3f}")
    print("="*88)
    return results

def generate_plots(hc_data, sa_data, ga_data, num_hotspots=NUM_HOTSPOTS, alpha=0.0, output_dir="."):
    hc_tour, hc_cost, hc_dist, hc_dmg, hc_hist = hc_data
    sa_tour, sa_cost, sa_dist, sa_dmg, sa_hist = sa_data
    ga_tour, ga_cost, ga_dist, ga_dmg, ga_hist = ga_data
    
    # 1. Figure 1: Convergence Curves
    plt.figure(figsize=(9, 4.5))
    def sample_curve(history, num_points=100):
        step = max(1, len(history) // num_points)
        return [history[i] for i in range(0, len(history), step)]
        
    plt.plot(sample_curve(hc_hist), label='Random-Restart Hill Climbing', color='darkorange', linewidth=2)
    plt.plot(sample_curve(sa_hist), label='Simulated Annealing (SA)', color='crimson', linewidth=2)
    plt.plot(sample_curve(ga_hist), label='Genetic Algorithm (GA)', color='forestgreen', linewidth=2)
    
    metric_label = "Combined Cost Metric" if alpha > 0 else "Tour Distance (km)"
    plt.title(f'Figure 1: Convergence Comparison ({num_hotspots} Hotspots | alpha={alpha})', fontsize=12, fontweight='bold')
    plt.xlabel('Search Progress (Sampled Steps)', fontsize=10)
    plt.ylabel(metric_label, fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    fig1_path = os.path.abspath(os.path.join(output_dir, 'convergence_comparison.png'))
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"\n[Generated] '{fig1_path}'")
    
    # 2. Figure 2: Trajectory Maps with Severity/Temperature Visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    models = [
        ("Random-Restart Hill Climbing", hc_tour, hc_dist, hc_dmg, axes[0], 'darkorange'),
        ("Simulated Annealing", sa_tour, sa_dist, sa_dmg, axes[1], 'crimson'),
        ("Genetic Algorithm", ga_tour, ga_dist, ga_dmg, axes[2], 'forestgreen')
    ]
    
    active_hotspots = HOTSPOTS[:num_hotspots]
    for title, tour, dist, dmg, ax, line_color in models:
        full_tour_indices = [0] + tour + [0]
        lons = [ALL_NODES[idx]['lon'] for idx in full_tour_indices]
        lats = [ALL_NODES[idx]['lat'] for idx in full_tour_indices]
        
        # Flight path
        ax.plot(lons, lats, color=line_color, linestyle='-', linewidth=2, zorder=2, label='Flight Path')
        
        # Plot Hotspots: size scaled by fire severity weight!
        h_lons = [h['lon'] for h in active_hotspots]
        h_lats = [h['lat'] for h in active_hotspots]
        h_sizes = [h['weight'] * 35 for h in active_hotspots]  # Raging fires appear larger!
        h_temps = [h['brightness_k'] for h in active_hotspots]
        
        scatter = ax.scatter(h_lons, h_lats, c=h_temps, s=h_sizes, cmap='YlOrRd', 
                             edgecolors='black', linewidth=1.2, zorder=3, label='Fire Hotspot')
        
        # Airbase
        ax.scatter([AIRBASE['lon']], [AIRBASE['lat']], 
                   color='blue', s=240, marker='*', edgecolors='black', zorder=4, label='Airbase (Base)')
        
        # Number labels
        for h in active_hotspots:
            ax.annotate(str(h['id']), (h['lon']+0.015, h['lat']+0.01), fontsize=8, fontweight='bold', color='darkred')
        ax.annotate('BASE', (AIRBASE['lon']+0.015, AIRBASE['lat']+0.01), fontsize=10, fontweight='bold', color='darkblue')
        
        title_str = f"{title}\nDistance: {dist:.1f} km | Burn Damage: {dmg:.0f}" if alpha > 0 else f"{title}\nDistance: {dist:.2f} km"
        ax.set_title(title_str, fontsize=11, fontweight='bold')
        ax.set_xlabel('Longitude (°E)', fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.5)
        
    axes[0].set_ylabel('Latitude (°S)', fontsize=10)
    axes[0].legend(loc='lower left', fontsize=9)
    plt.suptitle(f"Figure 2: Water-Bombing Helicopter Flight Trajectories (Hotspot Size = Fire Severity)", fontsize=13, fontweight='bold', y=1.02)
    fig2_path = os.path.abspath(os.path.join(output_dir, 'flight_trajectories.png'))
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[Generated] '{fig2_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Karhutla Water-Bombing Route Optimization")
    parser.add_argument("--model", choices=["all", "hc", "sa", "ga"], default="all", help="Algorithm to run")
    parser.add_argument("--trials", type=int, default=5, help="Number of benchmark trials")
    parser.add_argument("--nodes", type=int, default=15, help="Number of active hotspots (e.g., 10, 15, 20)")
    parser.add_argument("--alpha", type=float, default=0.05, help="Urgency factor (0.0 = Distance-Only, 0.05 = Severity-Weighted)")
    args = parser.parse_args()
    
    if args.model == "hc":
        random_restart_hill_climbing(num_hotspots=args.nodes, alpha=args.alpha)
    elif args.model == "sa":
        simulated_annealing(num_hotspots=args.nodes, alpha=args.alpha)
    elif args.model == "ga":
        genetic_algorithm(num_hotspots=args.nodes, alpha=args.alpha)
    else:
        hc_res, sa_res, ga_res = run_single_demo(num_hotspots=args.nodes, alpha=args.alpha)
        run_benchmark(num_trials=args.trials, num_hotspots=args.nodes, alpha=args.alpha)
        generate_plots(hc_res, sa_res, ga_res, num_hotspots=args.nodes, alpha=args.alpha)
