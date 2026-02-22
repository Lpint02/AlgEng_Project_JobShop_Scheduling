import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from path_utils import get_latest_results_file, get_results_paths

def plot(results_path=None, output_dir=None):
    """
    Genera i 4 grafici principali per l'analisi della campagna sperimentale workhorse.
    """
    print("[INFO] Generazione Plot Workhorse (Campagna Sperimentale Finale)...")
    
    # Usa il file di reference specifico se non specificato
    if results_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        results_path = os.path.join(base_dir, "results", "reference", "workhorse_results.csv")
    
    if output_dir is None:
        paths = get_results_paths("workhorse", create_dirs=True)
        output_dir = paths['plots_dir']
    
    print(f"[INFO] Usando file: {results_path}")
    print(f"[INFO] Salvando in: {output_dir}")
    
    if not os.path.exists(results_path):
        print(f"[WARNING] File {results_path} non trovato.")
        return

    df = pd.read_csv(results_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Rinomina Dist -> Distribution per consistenza
    if 'Dist' in df.columns:
        df = df.rename(columns={'Dist': 'Distribution'})
    
    # Tabella 1 + 3 grafici
    table_1_optimality_gap_summary(df)
    plot_2_lower_bound_error(df, output_dir)
    plot_3_rpd_by_distribution(df, output_dir)
    plot_4_rpd_vs_machines(df, output_dir)
    
    print("[INFO] Tutti i plot workhorse generati con successo!")


def table_1_optimality_gap_summary(df):
    """
    Tabella riassuntiva dell'Optimality Gap (Istanze Piccole).
    Filtra per Status == 'HEURISTIC_OPT_GAP'.
    Calcola statistiche accademiche: Run Totali, Hit Rate, Gap Medio, Gap Massimo.
    Stampa in formato Markdown per inserimento diretto in tesi.
    """
    print("[INFO] Generazione Tabella 1: Optimality Gap Summary (Istanze Piccole)...")
    
    df_filtered = df[df['Status'] == 'HEURISTIC_OPT_GAP'].copy()
    
    if df_filtered.empty:
        print("[WARNING] Nessun dato con Status 'HEURISTIC_OPT_GAP' trovato.")
        return None
    
    # Calcolo statistiche per ogni N
    summary = df_filtered.groupby('N').agg(
        Run_Totali=('Gap', 'count'),
        Hit_Count=('Gap', lambda x: (x == 0.0).sum()),
        Gap_Medio=('Gap', 'mean'),
        Gap_Max=('Gap', 'max')
    ).reset_index()
    
    # Calcolo Hit Rate percentuale
    summary['Hit_Rate'] = (summary['Hit_Count'] / summary['Run_Totali']) * 100
    
    # Riordina e rinomina colonne per output finale
    result = summary[['N', 'Run_Totali', 'Hit_Rate', 'Gap_Medio', 'Gap_Max']].copy()
    result.columns = ['N', 'Run Totali', 'Hit Rate (%)', 'Gap Medio (%)', 'Gap Massimo (%)']
    
    # Stampa in formato Markdown
    print("\n" + "="*70)
    print("TABELLA OPTIMALITY GAP - ISTANZE PICCOLE (Formato Markdown)")
    print("="*70 + "\n")
    print(result.to_markdown(index=False, floatfmt=(".0f", ".0f", ".1f", ".4f", ".4f")))
    print("\n" + "="*70)
    
    return result


def plot_2_lower_bound_error(df, output_dir):
    """
    Andamento dell'Errore del Lower Bound (Istanze Piccole).
    Filtra per Status == 'OPTIMAL' (BnB).
    Gap rappresenta la distanza dell'ottimo dal lower bound.
    """
    print("[INFO] Generazione Plot 2: Lower Bound Error (Istanze Piccole)...")
    
    df_filtered = df[df['Status'] == 'OPTIMAL'].copy()
    
    if df_filtered.empty:
        print("[WARNING] Nessun dato con Status 'OPTIMAL' trovato.")
        return
    
    # Setup stile (dimensioni ridotte per Overleaf)
    sns.set_style("whitegrid")
    plt.figure(figsize=(6, 3.5))
    
    # Colori per numero di macchine
    palette = {2: '#2E86C1', 4: '#E74C3C', 5: '#28B463', 10: '#F39C12', 20: '#9B59B6'}
    
    # Calcola media per (N, M)
    df_avg = df_filtered.groupby(['N', 'M'])['Gap'].mean().reset_index()
    
    # Line plot raggruppato per M (marker ridotti per figura compatta)
    for m in sorted(df_avg['M'].unique()):
        subset = df_avg[df_avg['M'] == m].sort_values('N')
        color = palette.get(m, '#333333')
        plt.plot(subset['N'], subset['Gap'], 
                marker='o', linewidth=1.5, markersize=5,
                label=f'M = {m}', color=color,
                markerfacecolor='white', markeredgewidth=1.5, markeredgecolor=color)
    
    # Titolo e etichette (font ridotti per figura compatta)
    plt.title('Deviazione del Lower Bound dall\'Ottimo Reale\n(Istanze Piccole - Branch & Bound)', 
              fontsize=10, fontweight='bold')
    plt.xlabel('Dimensione Istanza (N)', fontsize=9)
    plt.ylabel('Gap Ottimo - Lower Bound (%)', fontsize=9)
    
    # Griglia e legenda
    plt.grid(True, alpha=0.3)
    plt.legend(title='Macchine', fontsize=8, title_fontsize=9, loc='upper left')
    
    # Limiti Y per visibilità
    plt.ylim(bottom=0)
    
    # Salvataggio PNG e PDF
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "workhorse_2_lower_bound_error.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: workhorse_2_lower_bound_error.pdf")
    plt.close()


def plot_3_rpd_by_distribution(df, output_dir):
    """
    Boxplot dell'RPD per Distribuzione (Istanze Grandi).
    Filtra per Status == 'HEURISTIC_RPD'.
    Confronta uniform vs job_correlated.
    """
    print("[INFO] Generazione Plot 3: RPD by Distribution (Istanze Grandi)...")
    
    df_filtered = df[df['Status'] == 'HEURISTIC_RPD'].copy()
    
    if df_filtered.empty:
        print("[WARNING] Nessun dato con Status 'HEURISTIC_RPD' trovato.")
        return
    
    # Setup stile (dimensioni ridotte per Overleaf)
    sns.set_style("whitegrid")
    plt.figure(figsize=(7, 4))
    
    # Colori per distribuzione
    palette = {'uniform': '#DC143C', 'job_correlated': '#2E8B57'}
    
    # Boxplot con hue per distribuzione
    ax = sns.boxplot(
        data=df_filtered, 
        x='N', 
        y='Gap',
        hue='Distribution',
        palette=palette,
        flierprops={'marker': 'o', 'markersize': 5, 'alpha': 0.5}
    )
    
    # Titolo e etichette (font ridotti per figura compatta)
    plt.title('Relative Percentage Deviation (RPD) per Distribuzione\n(Istanze Grandi - Scalabilità Algoritmo)', 
              fontsize=10, fontweight='bold')
    plt.xlabel('Dimensione Istanza (N)', fontsize=9)
    plt.ylabel('RPD (%)', fontsize=9)
    
    # Griglia e legenda
    plt.grid(True, alpha=0.3, axis='y')
    plt.legend(title='Distribuzione', fontsize=8, title_fontsize=9, loc='upper left')
    
    # Salvataggio PNG e PDF
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "workhorse_3_rpd_distribution.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: workhorse_3_rpd_distribution.pdf")
    plt.close()


def plot_4_rpd_vs_machines(df, output_dir):
    """
    Scatterplot dell'RPD vs Macchine M (Istanze Grandi).
    Filtra per Status == 'HEURISTIC_RPD'.
    Mostra come l'RPD aumenta con il numero di macchine.
    """
    print("[INFO] Generazione Plot 4: RPD vs Machines Scatterplot (Istanze Grandi)...")
    
    df_filtered = df[df['Status'] == 'HEURISTIC_RPD'].copy()
    
    if df_filtered.empty:
        print("[WARNING] Nessun dato con Status 'HEURISTIC_RPD' trovato.")
        return
    
    # Setup stile (dimensioni ridotte per Overleaf)
    sns.set_style("whitegrid")
    plt.figure(figsize=(6, 4))
    
    # Colori per distribuzione
    palette = {'uniform': '#DC143C', 'job_correlated': '#2E8B57'}
    
    # Scatterplot con jitter per visualizzare sovrapposizioni
    ax = sns.stripplot(
        data=df_filtered, 
        x='M', 
        y='Gap',
        hue='Distribution',
        palette=palette,
        alpha=0.6,
        size=8,
        jitter=0.2,
        dodge=True
    )
    
    # Aggiungi anche boxplot trasparente per mostrare la tendenza
    sns.boxplot(
        data=df_filtered, 
        x='M', 
        y='Gap',
        hue='Distribution',
        palette=palette,
        boxprops={'alpha': 0.3},
        showcaps=True,
        showfliers=False,
        whiskerprops={'alpha': 0.3},
        legend=False
    )
    
    # Titolo e etichette (font ridotti per figura compatta)
    plt.title('RPD vs Numero di Macchine (M)\n(Istanze Grandi - Impatto Lower Bound)', 
              fontsize=10, fontweight='bold')
    plt.xlabel('Numero di Macchine (M)', fontsize=9)
    plt.ylabel('RPD (%)', fontsize=9)
    
    # Griglia e legenda
    plt.grid(True, alpha=0.3, axis='y')
    
    # Rimuovi legenda duplicata e mantieni solo una
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles[:2], labels[:2], title='Distribuzione', fontsize=8, title_fontsize=9, loc='upper left')
    
    # Annotazione esplicativa
    plt.annotate('RPD aumenta con M\n(Lower Bound si degrada)', 
                 xy=(0.95, 0.95), xycoords='axes fraction',
                 fontsize=8, ha='right', va='top',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))
    
    # Salvataggio PNG e PDF
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "workhorse_4_rpd_vs_machines.pdf"), bbox_inches='tight')
    print("[SUCCESS] Salvato: workhorse_4_rpd_vs_machines.pdf")
    plt.close()

