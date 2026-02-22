#!/usr/bin/env python3
"""
Script principale per eseguire tutti gli esperimenti del progetto di scheduling
Garantisce massima riproducibilità seguendo best practice accademiche

Usage:
    python run_experiments.py --all                # Tutti gli esperimenti
    python run_experiments.py --pilot              # Solo esperimenti pilot
    python run_experiments.py --config pilot_a     # Esperimento specifico
    python run_experiments.py --generate-plots     # Solo grafici (da dati esistenti)
    
Autore: Leonardo Pinterpe
Corso: Algorithm Engineering
Data: Febbraio 2026
"""

import argparse
import os
import sys
import time
import datetime
import importlib

# Aggiungi src al path per gli import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from runner import run_experiment
from path_utils import get_results_paths

# Import plotting modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'plotting'))

plot_pilot_a = importlib.import_module('plot_pilot_a')
plot_pilot_b = importlib.import_module('plot_pilot_b')
plot_pilot_c = importlib.import_module('plot_pilot_c')
plot_validation = importlib.import_module('plot_validation')
plot_workhorse = importlib.import_module('plot_workhorse')

# Configurazioni disponibili
EXPERIMENT_CONFIGS = {
    'pilot_a': 'experiments/config_pilot_a.json',
    'pilot_b': 'experiments/config_pilot_b.json', 
    'pilot_c': 'experiments/config_pilot_c.json',
    'validation': 'experiments/config_validation.json',
    'workhorse': 'experiments/workhorse_config.json'
}

PLOT_MODULES = {
    'pilot_a': plot_pilot_a,
    'pilot_b': plot_pilot_b,
    'pilot_c': plot_pilot_c, 
    'validation': plot_validation,
    'workhorse': plot_workhorse
}

def print_header(title):
    """Stampa header formattato per sezioni"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def run_single_experiment(experiment_name):
    """Esegue un singolo esperimento con logging completo"""
    if experiment_name not in EXPERIMENT_CONFIGS:
        print(f"❌ Esperimento '{experiment_name}' non trovato!")
        print(f"   Disponibili: {list(EXPERIMENT_CONFIGS.keys())}")
        return False
    
    config_path = EXPERIMENT_CONFIGS[experiment_name]
    
    if not os.path.exists(config_path):
        print(f"❌ File configurazione {config_path} non trovato!")
        return False
    
    print(f"🚀 Avvio Esperimento: {experiment_name}")
    print(f"📄 Configurazione: {config_path}")
    
    start_time = time.time()
    try:
        run_experiment(config_path)
        elapsed = time.time() - start_time
        print(f"✅ Esperimento {experiment_name} completato in {elapsed:.1f}s")
        return True
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Esperimento {experiment_name} fallito dopo {elapsed:.1f}s: {e}")
        return False

def generate_plots(experiment_list=None):
    """Genera tutti i grafici specificati"""
    if experiment_list is None:
        experiment_list = list(PLOT_MODULES.keys())
    
    print_header("🎨 GENERAZIONE GRAFICI")
    
    for exp_name in experiment_list:
        if exp_name not in PLOT_MODULES:
            print(f"⚠️  Plot per '{exp_name}' non disponibile")
            continue
            
        print(f"📊 Generazione plot: {exp_name}")
        try:
            PLOT_MODULES[exp_name].plot()
            print(f"✅ Plot {exp_name} generato")
        except Exception as e:
            print(f"❌ Errore plot {exp_name}: {e}")

def check_environment():
    """Verifica che l'ambiente sia configurato correttamente"""
    print_header("🔍 VERIFICA AMBIENTE")
    
    # Controlla dipendenze
    required_packages = ['pandas', 'matplotlib', 'seaborn', 'numpy']
    missing = []
    
    for pkg in required_packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg}: installato")
        except ImportError:
            missing.append(pkg)
            print(f"❌ {pkg}: mancante")
    
    if missing:
        print(f"\n⚠️  Installa dipendenze mancanti con:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    # Controlla struttura directory
    required_dirs = [
        'data/dataset_exam',
        'results/generated/csv',
        'results/generated/plots'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory: {dir_path}")
        else:
            print(f"❌ Directory mancante: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            print(f"   → Creata automaticamente")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Esecutore principale per esperimenti di scheduling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  python run_experiments.py --all                 # Tutti gli esperimenti + plot
  python run_experiments.py --pilot               # Solo esperimenti pilot
  python run_experiments.py --config pilot_a      # Solo pilot_a
  python run_experiments.py --generate-plots      # Solo plot (da risultati esistenti)
  
Output:
  - CSV: results/generated/csv/
  - Grafici: results/generated/plots/
  - Log: Timestamp nei nomi file per evitare sovrapposizioni
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Esegui tutti gli esperimenti e genera plot')
    parser.add_argument('--pilot', action='store_true', 
                       help='Esegui solo esperimenti pilot (a,b,c)')
    parser.add_argument('--config', type=str,
                       help='Esegui esperimento specifico')
    parser.add_argument('--generate-plots', action='store_true',
                       help='Genera solo grafici (senza rieseguire esperimenti)')
    parser.add_argument('--check-env', action='store_true',
                       help='Verifica solo configurazione ambiente')

    args = parser.parse_args()

    # Header principale
    print_header(f"🧪 SCHEDULING EXPERIMENTS - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Se nessun argomento, mostra help
    if not any([args.all, args.pilot, args.config, args.generate_plots, args.check_env]):
        parser.print_help()
        return
    
    # Verifica ambiente
    if not check_environment():
        print("❌ Ambiente non configurato correttamente. Risolvi i problemi sopra.")
        return
    
    if args.check_env:
        print("✅ Ambiente verificato con successo!")
        return

    # Esecuzione esperimenti
    experiments_to_run = []
    
    if args.all:
        experiments_to_run = list(EXPERIMENT_CONFIGS.keys())
    elif args.pilot:
        experiments_to_run = ['pilot_a', 'pilot_b', 'pilot_c']
    elif args.config:
        if args.config in EXPERIMENT_CONFIGS:
            experiments_to_run = [args.config]
        else:
            print(f"❌ Configurazione '{args.config}' non trovata!")
            print(f"   Disponibili: {list(EXPERIMENT_CONFIGS.keys())}")
            return
    
    # Esegui esperimenti
    if experiments_to_run:
        print_header("🧪 ESECUZIONE ESPERIMENTI")
        
        success_count = 0
        total_start = time.time()
        
        for exp_name in experiments_to_run:
            if run_single_experiment(exp_name):
                success_count += 1
        
        total_elapsed = time.time() - total_start
        print(f"\n📊 Riepilogo: {success_count}/{len(experiments_to_run)} esperimenti riusciti")
        print(f"⏱️  Tempo totale: {total_elapsed:.1f}s")
    
    # Genera plot
    if args.all or args.pilot or args.generate_plots:
        plot_experiments = experiments_to_run if experiments_to_run else list(PLOT_MODULES.keys())
        generate_plots(plot_experiments)
    
    # Messaggio finale
    print_header("🎉 COMPLETATO")
    print("📁 Controlla i risultati in:")
    print("   • results/generated/csv/     : File CSV risultati")
    print("   • results/generated/plots/   : Grafici PDF")
    print("   • results/reference/         : Risultati originali (sola lettura)")

if __name__ == "__main__":
    main()