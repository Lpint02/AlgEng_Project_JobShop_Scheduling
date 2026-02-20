"""
Script di coordinamento per generare tutti i grafici del report finale
Esegue tutti i plot script e genera la documentazione
"""

import os
import sys
import importlib.util

def run_all_plots():
    """
    Esegue tutti gli script di plotting per il report finale
    """
    print("🚀 Generazione completa dei grafici per il report finale...")
    print("=" * 60)
    
    # Cambia alla directory plotting
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Lista degli script da eseguire
    scripts = [
        ("plot_validation.py", "Validazione: Micro-benchmarks (BF vs BnB)"),
        ("plot_pilot_a.py", "Pilot A: The Wall (Branch & Bound Timeout)"),
        ("plot_pilot_b.py", "Pilot B: Parameter Tuning (Heatmap)"),
        ("plot_pilot_c.py", "Pilot C: Convergence Analysis (Gap vs Time)"),
        ("plot_workhorse.py", "Workhorse: Campagna Sperimentale Finale")
    ]
    
    results = []
    
    for script, description in scripts:
        print(f"\n📊 {description}")
        print("-" * 50)
        
        try:
            if os.path.exists(script):
                # Carica il modulo usando importlib
                script_name = script.replace('.py', '')
                spec = importlib.util.spec_from_file_location(script_name, script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Chiama la funzione corretta (plot() o plot_all() per workhorse) 
                if script == "plot_workhorse.py":
                    module.plot_all()
                else:
                    module.plot()
                results.append((script, "✅ Successo"))
                print(f"✅ {script} completato")
            else:
                results.append((script, "❌ File non trovato"))
                print(f"❌ {script} non trovato")
                
        except Exception as e:
            results.append((script, f"❌ Errore: {str(e)[:50]}..."))
            print(f"❌ Errore in {script}: {e}")
    
    # Summary finale
    print(f"\n{'='*60}")
    print("📋 SUMMARY GENERAZIONE GRAFICI")
    print(f"{'='*60}")
    
    for script, status in results:
        print(f"{script:<30} {status}")
    
    print(f"\n📁 Grafici salvati in: ../../plots/")
    print("📄 Formati disponibili: .png (300dpi) e .pdf (vettoriale)")
    
    # Controlla se la cartella plots esiste e lista i file
    plots_dir = "../../plots"
    if os.path.exists(plots_dir):
        files = [f for f in os.listdir(plots_dir) if f.endswith(('.png', '.pdf'))]
        print(f"\n📊 File generati ({len(files)}):")
        for f in sorted(files):
            print(f"  - {f}")
    
    print("\n🎯 Setup completo per report finale!")

if __name__ == "__main__":
    run_all_plots()