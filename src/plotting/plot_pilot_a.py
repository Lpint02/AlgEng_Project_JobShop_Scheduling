import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot(results_path="../../results/pilot_wall_results.csv", output_dir="../../plots"):
    print("[INFO] Generazione Plot Pilot A (The Wall - BnB Timeout)...")
    
    if not os.path.exists(results_path):
        print(f"[WARNING] File {results_path} non trovato.")
        return

    df = pd.read_csv(results_path)
    
    # Filtriamo per M=4 (dove avviene la crescita esponenziale) e algoritmo BnB
    df_filtered = df[(df['M'] == 4) & (df['Algo'] == 'BnB')].copy()
    
    if df_filtered.empty:
        print("[WARNING] Nessun dato trovato per M=4 e algoritmo BnB")
        return
    
    # Calcola media per N e Dist, gestendo timeout
    df_avg = df_filtered.groupby(['N', 'Dist'])['Time'].mean().reset_index()
    
    # Identifica timeout (Time >= 60s)
    df_timeout = df_filtered[df_filtered['Time'] >= 60.0].groupby(['N', 'Dist']).size().reset_index(name='timeout_count')
    
    # Setup grafico compatto per Overleaf
    sns.set_style("whitegrid")
    plt.figure(figsize=(6, 4))
    
    # Colori classici
    colors = {'uniform': '#2E8B57', 'job_correlated': '#DC143C'}
    
    # Linea pulita per ogni distribuzione
    for dist in sorted(df_avg['Dist'].unique()):
        data = df_avg[df_avg['Dist'] == dist].sort_values('N')
        
        # Separa dati normali da timeout
        normal_data = data[data['Time'] < 59.5]
        timeout_data = data[data['Time'] >= 59.5]
        
        # Linea continua per dati normali
        if not normal_data.empty:
            plt.plot(normal_data['N'], normal_data['Time'], 
                    color=colors[dist], linewidth=2, marker='o', markersize=5,
                    label=dist.replace('_', ' ').title(), markerfacecolor='white',
                    markeredgewidth=1.5, markeredgecolor=colors[dist])
        
        # Marcatori X rossi per timeout
        if not timeout_data.empty:
            plt.scatter(timeout_data['N'], [60]*len(timeout_data), 
                       color='red', marker='X', s=100, linewidth=2,
                       label=f'{dist.replace("_", " ").title()} (Timeout)' if normal_data.empty else '',
                       alpha=0.8, zorder=5)
    
    # Linea di timeout
    plt.axhline(y=60, color='gray', linestyle='--', alpha=0.7, linewidth=1.5, 
                label='Timeout Limit (60s)')
    
    # Scala LOGARITMICA per catturare l'intera gamma da millisecondi a minuti
    plt.yscale('log')
    
    # Etichette compatte
    plt.title('Pilot A: Branch & Bound "The Wall" (M=4)', fontsize=10, fontweight='bold')
    plt.xlabel('Instance Size (N)', fontsize=9)
    plt.ylabel('Wall Clock Time (seconds)', fontsize=9)
    
    # Ticks personalizzati per scala logaritmica
    plt.xticks(range(8, 28, 2), fontsize=8)
    plt.yticks([0.0001, 0.001, 0.01, 0.1, 1, 10, 60], 
               ['0.1ms', '1ms', '10ms', '0.1s', '1s', '10s', '60s'], fontsize=8)
    plt.ylim(0.00005, 100)
    
    # Legenda compatta
    plt.legend(fontsize=7, loc='upper left', framealpha=0.9)
    plt.grid(True, alpha=0.3)
    
    # Salvataggio PNG e PDF
    os.makedirs(output_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pilot_a_the_wall.png"), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, "pilot_a_the_wall.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: pilot_a_the_wall.png/.pdf")
    plt.close()

if __name__ == "__main__":
    plot()
    
