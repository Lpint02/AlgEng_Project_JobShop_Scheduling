import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_utils import get_latest_results_file, get_results_paths

def plot(results_path=None, output_dir=None):
    print("[INFO] Generazione Plot Validazione (Bar Chart Logaritmico)...")
    
    if not os.path.exists(results_path):
        print(f"[WARNING] File {results_path} non trovato.")
        return

    df = pd.read_csv(results_path)
    
    # Filtriamo per algoritmi esatti (BF e BnB) per istanze piccole
    exact_data = df[df['Algo'].isin(['BF', 'BnB'])].copy()
    if exact_data.empty:
        print("[WARNING] Nessun dato trovato per algoritmi esatti")
        return
    
    # Raggruppiamo per N, Algo e calcoliamo medie
    grouped_data = exact_data.groupby(['N', 'Algo']).agg({
        'Time': 'mean',
        'Nodes': 'mean'
    }).reset_index()
    
    # Setup figure compatta per Overleaf
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.5))
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Colori professionali
    colors = {'BF': '#1f4e79', 'BnB': '#2d5d31'}  # Blu scuro e Verde scuro
    
    # Larghezza barre
    bar_width = 0.35
    x_positions = np.arange(len(grouped_data['N'].unique()))
    
    # 1. SUBPLOT TIME (Sinistra)
    for i, algo in enumerate(['BF', 'BnB']):       
        algo_data = grouped_data[grouped_data['Algo'] == algo]
        if not algo_data.empty:
            positions = x_positions + (i - 0.5) * bar_width
            ax1.bar(positions, algo_data['Time'], bar_width, 
                   color=colors[algo], alpha=0.8, label=algo)
    
    ax1.set_yscale('log')
    ax1.set_title('Execution Time Comparison\n(Brute Force vs Branch & Bound)', 
                  fontsize=10, fontweight='bold')
    ax1.set_xlabel('Instance Size (N)', fontsize=9)
    ax1.set_ylabel('Time (seconds) - Log Scale', fontsize=9)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(sorted(grouped_data['N'].unique()), fontsize=8)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. SUBPLOT NODES (Destra)
    for i, algo in enumerate(['BF', 'BnB']):
        algo_data = grouped_data[grouped_data['Algo'] == algo]
        if not algo_data.empty:
            positions = x_positions + (i - 0.5) * bar_width
            ax2.bar(positions, algo_data['Nodes'], bar_width, 
                   color=colors[algo], alpha=0.8, label=algo)
    
    ax2.set_yscale('log')
    ax2.set_title('Nodes Visited Comparison\n(Pruning Effectiveness)', 
                  fontsize=10, fontweight='bold')
    ax2.set_xlabel('Instance Size (N)', fontsize=9)
    ax2.set_ylabel('Nodes Visited - Log Scale', fontsize=9)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(sorted(grouped_data['N'].unique()), fontsize=8)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # Aggiunta annotazioni per evidenziare il pruning
    if len(grouped_data) > 0:
        max_n = max(grouped_data['N'])
        bf_nodes = grouped_data[(grouped_data['N'] == max_n) & (grouped_data['Algo'] == 'BF')]['Nodes']
        bnb_nodes = grouped_data[(grouped_data['N'] == max_n) & (grouped_data['Algo'] == 'BnB')]['Nodes']
        
        if not bf_nodes.empty and not bnb_nodes.empty:
            pruning_factor = bf_nodes.iloc[0] / bnb_nodes.iloc[0]
            ax2.text(0.7, 0.95, f'Pruning Factor\n(N={max_n}): {pruning_factor:.1f}x',
                    transform=ax2.transAxes, fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    # Salvataggio PNG e PDF
    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "validation_micro_benchmarks.png"), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, "validation_micro_benchmarks.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: validation_micro_benchmarks.png/.pdf")
    plt.close()

if __name__ == "__main__":
    plot()