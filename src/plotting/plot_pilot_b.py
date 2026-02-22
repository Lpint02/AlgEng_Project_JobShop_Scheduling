import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_utils import get_latest_results_file, get_results_paths

def plot(results_path=None, output_dir=None):
    print("[INFO] Generazione Plot Pilot B (Tuning: Heatmap)...")
    
    # Usa il file di reference specifico se non specificato
    if results_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        results_path = os.path.join(base_dir, "results", "reference", "pilot_b_tuning.csv")
    
    if output_dir is None:
        paths = get_results_paths("pilot_b", create_dirs=True)
        output_dir = paths['plots_dir']
    
    print(f"[INFO] Usando file: {results_path}")
    print(f"[INFO] Salvando in: {output_dir}")
    
    if not os.path.exists(results_path):
        print(f"[WARNING] File {results_path} non trovato.")
        return

    df = pd.read_csv(results_path)
    
    # Parsing dei parametri dalla colonna Params
    def parse_ig_params(params_str):
        # Formato: "d=4,T=0.5,t=30s"  
        parts = params_str.replace('s', '').split(',')
        d = int(parts[0].split('=')[1])
        T = float(parts[1].split('=')[1]) 
        return d, T
    
    # Applica parsing solo alle righe IG
    ig_data = df[df['Algo'] == 'IG'].copy()
    if ig_data.empty:
        print("[WARNING] Nessun dato IG trovato per tuning")
        return
        
    ig_data[['d', 'T']] = ig_data['Params'].apply(lambda x: pd.Series(parse_ig_params(x)))
    
    # Calcola Gap medio per combinazione (d, T)
    agg_data = ig_data.groupby(['d', 'T'])['Gap'].mean().reset_index()
    pivot_data = agg_data.pivot(index='d', columns='T', values='Gap')
    
    # Setup figure compatta per Overleaf
    plt.figure(figsize=(5, 4))
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # HEATMAP
    sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='RdYlBu_r', 
                cbar_kws={'label': 'Average Gap (%)'}, annot_kws={'size': 8})
    plt.title('Parameter Tuning Heatmap\n(Lower is Better)', fontsize=10, fontweight='bold')
    plt.xlabel('Temperature (T)', fontsize=9)
    plt.ylabel('Destruction Level (d)', fontsize=9)
    
    # Salvataggio PNG e PDF
    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pilot_b_tuning.png"), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, "pilot_b_tuning.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: pilot_b_tuning.png/.pdf")
    plt.close()

def plot_interaction(results_path="../../results/pilot_b_tuning.csv", output_dir="../../plots"):
    """
    Genera grafico interaction che mostra:
    - Asse x: taglia delle istanze (N)
    - Asse y: gap dal lower bound (%)
    - 3 linee, una per ogni valore di d (destruction level)
    """
    print("[INFO] Generazione Plot Pilot B Interaction (Instance Size vs Gap per d)...")
    
    if not os.path.exists(results_path):
        print(f"[WARNING] File {results_path} non trovato.")
        return

    df = pd.read_csv(results_path)
    
    # Parsing dei parametri dalla colonna Params
    def parse_ig_params(params_str):
        # Formato: "d=4,T=0.5,t=30s"  
        parts = params_str.replace('s', '').split(',')
        d = int(parts[0].split('=')[1])
        T = float(parts[1].split('=')[1]) 
        return d, T
    
    # Applica parsing solo alle righe IG
    ig_data = df[df['Algo'] == 'IG'].copy()
    if ig_data.empty:
        print("[WARNING] Nessun dato IG trovato per tuning")
        return
        
    ig_data[['d', 'T']] = ig_data['Params'].apply(lambda x: pd.Series(parse_ig_params(x)))
    
    # Calcola Gap medio per combinazione (N, d) - aggregando su tutte le T
    agg_data = ig_data.groupby(['N', 'd'])['Gap'].mean().reset_index()
    
    # Setup figure compatta per Overleaf
    plt.figure(figsize=(6, 4))
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Definisci colori e marker per ogni valore di d
    colors = ['#2E86C1', '#E74C3C', '#28B463']
    markers = ['o', 's', '^']
    
    # Plot delle tre linee (una per ogni d)
    for i, d_val in enumerate(sorted(agg_data['d'].unique())):
        subset = agg_data[agg_data['d'] == d_val]
        plt.plot(subset['N'], subset['Gap'], 
                marker=markers[i], 
                color=colors[i],
                linewidth=2, 
                markersize=6, 
                label=f'd = {d_val}',
                markerfacecolor='white',
                markeredgewidth=1.5,
                markeredgecolor=colors[i])
    
    plt.title('Parameter Interaction Effects\n(Instance Size vs Gap by Destruction Level)', 
              fontsize=10, fontweight='bold', pad=10)
    plt.xlabel('Instance Size (N)', fontsize=9, fontweight='bold')
    plt.ylabel('Average Gap from Lower Bound (%)', fontsize=9, fontweight='bold')
    
    # Personalizza la griglia 
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Personalizza la leggenda
    plt.legend(title='Destruction Level (d)', 
               title_fontsize=8,
               fontsize=7,
               loc='best',
               frameon=True,
               shadow=True)
    
    # Personalizza gli assi
    plt.xticks(sorted(agg_data['N'].unique()), fontsize=8)
    plt.yticks(fontsize=8)
    
    # Aggiungi margini
    plt.xlim(min(agg_data['N']) - 10, max(agg_data['N']) + 10)
    gap_min, gap_max = agg_data['Gap'].min(), agg_data['Gap'].max()
    gap_range = gap_max - gap_min
    plt.ylim(gap_min - 0.1*gap_range, gap_max + 0.1*gap_range)
    
    # Salvataggio PNG e PDF
    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pilot_b_interaction.png"), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, "pilot_b_interaction.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: pilot_b_interaction.png/.pdf")
    plt.close()

if __name__ == "__main__":
    plot()
    plot_interaction()
    print("✅ Salvato: pilot_b_tuning.png")
    print("✅ Salvato: pilot_b_interaction.png")