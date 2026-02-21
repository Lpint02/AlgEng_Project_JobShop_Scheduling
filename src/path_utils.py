"""
Utility per gestire percorsi e timestamp per la riproducibilità
"""
import os
import datetime

def get_results_paths(experiment_name, create_dirs=True):
    """
    Genera percorsi per CSV e grafici con timestamp opzionale
    
    Args:
        experiment_name: Nome dell'esperimento (es. 'pilot_a')
        create_dirs: Se True, crea le directory se non esistono
    
    Returns:
        dict con 'csv_path', 'plots_dir', 'reference_csv', 'reference_plots_dir'
    """
    # Base directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    generated_dir = os.path.join(base_dir, "results", "generated")
    reference_dir = os.path.join(base_dir, "results", "reference")
    
    # Timestamp per evitare sovrascritture
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    paths = {
        # Percorsi per nuovi risultati (con timestamp)
        'csv_path': os.path.join(generated_dir, "csv", f"{experiment_name}_results_{timestamp}.csv"),
        'plots_dir': os.path.join(generated_dir, "plots"),
        'csv_dir': os.path.join(generated_dir, "csv"),
        
        # Percorsi di riferimento (dati originali del prof)
        'reference_csv': os.path.join(reference_dir, f"{experiment_name}_results.csv"),
        'reference_plots_dir': reference_dir
    }
    
    if create_dirs:
        os.makedirs(paths['csv_dir'], exist_ok=True)
        os.makedirs(paths['plots_dir'], exist_ok=True)
        os.makedirs(reference_dir, exist_ok=True)
    
    return paths

def get_latest_results_file(experiment_name):
    """
    Trova il file di risultati più recente per un esperimento
    Cerca prima in generated/, poi fallback su reference/
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Cerca in generated/ (ordinato per timestamp)
    generated_csv_dir = os.path.join(base_dir, "results", "generated", "csv")
    if os.path.exists(generated_csv_dir):
        csv_files = [f for f in os.listdir(generated_csv_dir) 
                     if f.startswith(experiment_name) and f.endswith('.csv')]
        if csv_files:
            # Ordina per timestamp (più recente primo)
            csv_files.sort(reverse=True)
            return os.path.join(generated_csv_dir, csv_files[0])
    
    # Fallback su reference/
    reference_file = os.path.join(base_dir, "results", "reference", f"{experiment_name}_results.csv")
    if os.path.exists(reference_file):
        return reference_file
    
    # Vecchia struttura per compatibilità
    old_file = os.path.join(base_dir, "results", f"{experiment_name}_results.csv")
    if os.path.exists(old_file):
        return old_file
    
    return None