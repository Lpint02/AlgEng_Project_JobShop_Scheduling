import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_utils import get_latest_results_file, get_results_paths

def plot(results_path=None, output_dir=None):
    print("[INFO] Generazione Plot Pilot C (Convergence: Gap vs Time)...")
    
    # Usa il file di reference specifico se non specificato
    if results_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        results_path = os.path.join(base_dir, "results", "reference", "pilot_c_convergence.csv")
    
    if output_dir is None:
        paths = get_results_paths("pilot_c", create_dirs=True)
        output_dir = paths['plots_dir']
    
    print(f"[INFO] Usando file: {results_path}")
    print(f"[INFO] Salvando in: {output_dir}")
    
    if not os.path.exists(results_path):
        print(f"[WARNING] File {results_path} non trovato.")
        return

    df = pd.read_csv(results_path)
    
    # Filtriamo solo dati IG per analisi di convergenza
    ig_data = df[df['Algo'] == 'IG'].copy()
    if ig_data.empty:
        print("[WARNING] Nessun dato IG trovato per convergenza")
        return
    
    # Parsing time limit dai parametri
    def parse_time_limit(params_str):
        # Formato: "d=6,T=0.1,t=30s"
        parts = params_str.split(',')
        time_str = [p for p in parts if 't=' in p][0]
        return float(time_str.split('=')[1].replace('s', ''))
    
    ig_data['Time_Limit'] = ig_data['Params'].apply(parse_time_limit)
    
    # Time steps desiderati: 0.1, 0.5, 1, 5, 10, 30, 60
    time_steps = [0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
    
    # Calcola gap medio per N, Dist, Time_Limit
    convergence_data = ig_data.groupby(['N', 'Dist', 'Time_Limit'])['Gap'].mean().reset_index()
    
    # Setup figure compatta per Overleaf
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.5))
    sns.set_style("whitegrid")
    
    # Colori per diverse dimensioni N
    unique_n = sorted(convergence_data['N'].unique())
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blu, Arancio, Verde
    
    # 1. SUBPLOT JOB CORRELATED (Sinistra)
    jc_data = convergence_data[convergence_data['Dist'] == 'job_correlated']
    
    for i, n_val in enumerate(unique_n):
        subset = jc_data[jc_data['N'] == n_val]
        if not subset.empty:
            # Filtra solo i time steps desiderati
            subset_filtered = subset[subset['Time_Limit'].isin(time_steps)].sort_values('Time_Limit')
            
            ax1.plot(subset_filtered['Time_Limit'], subset_filtered['Gap'],
                    color=colors[i], marker='o', linewidth=1.5, markersize=4,
                    label=f'N = {n_val}', markerfacecolor='white',
                    markeredgewidth=1.5, markeredgecolor=colors[i])
    
    ax1.set_title('Job Correlated Distribution', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Time (seconds)', fontsize=9)
    ax1.set_ylabel('Gap from Lower Bound (%)', fontsize=9)
    ax1.set_xticks(time_steps)
    ax1.set_xticklabels(['0.1', '0.5', '1', '5', '10', '30', '60'], fontsize=7)
    ax1.legend(title='Instance Size', loc='upper right', fontsize=7, title_fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. SUBPLOT UNIFORM (Destra)
    uniform_data = convergence_data[convergence_data['Dist'] == 'uniform']
    
    for i, n_val in enumerate(unique_n):
        subset = uniform_data[uniform_data['N'] == n_val]
        if not subset.empty:
            # Filtra solo i time steps desiderati
            subset_filtered = subset[subset['Time_Limit'].isin(time_steps)].sort_values('Time_Limit')
            
            ax2.plot(subset_filtered['Time_Limit'], subset_filtered['Gap'],
                    color=colors[i], marker='o', linewidth=1.5, markersize=4,
                    label=f'N = {n_val}', markerfacecolor='white',
                    markeredgewidth=1.5, markeredgecolor=colors[i])
    
    ax2.set_title('Uniform Distribution', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Time (seconds)', fontsize=9)
    ax2.set_ylabel('Gap from Lower Bound (%)', fontsize=9)
    ax2.set_xticks(time_steps)
    ax2.set_xticklabels(['0.1', '0.5', '1', '5', '10', '30', '60'], fontsize=7)
    ax2.legend(title='Instance Size', loc='upper right', fontsize=7, title_fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # Titolo principale
    fig.suptitle('Pilot C: Algorithm Convergence Analysis (Time vs Quality Trade-off)', 
                 fontsize=11, fontweight='bold')
    
    # Salvataggio PNG e PDF
    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pilot_c_convergence.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: pilot_c_convergence.pdf")
    plt.close()

if __name__ == "__main__":
    plot()