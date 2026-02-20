import argparse
import json
import os
import csv
import time
import glob
import random
import re

# Assicurati che questi import funzionino con la tua struttura
from instance import Instance
from algorithms import BranchAndBound, IteratedGreedy, PureBruteForce

def parse_filename(filename):
    """
    Estrae i metadati dal nome file: inst_N_M_Dist_Seed.txt
    Usa regex per gestire robustamente distribuzioni con underscore (es. job_correlated).
    """
    # Pattern: inst_<N>_<M>_<distribuzione>_<seed>.txt
    # La distribuzione può contenere underscore (es. job_correlated)
    pattern = r'^inst_(\d+)_(\d+)_(.+)_(\d+)\.txt$'
    match = re.match(pattern, filename)
    
    if not match:
        print(f"⚠️ Warning: Skip file anomalo '{filename}': formato non riconosciuto")
        return None
    
    try:
        n = int(match.group(1))
        m = int(match.group(2))
        dist = match.group(3)
        seed = int(match.group(4))
        
        return {"n": n, "m": m, "dist": dist, "seed": seed}
    except Exception as e:
        print(f"⚠️ Warning: Skip file anomalo '{filename}': {e}")
        return None

def run_experiment(config_path):
    # 1. Carica Configurazione
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print(f"🚀 Avvio Esperimento: {config['experiment_name']}")
    print(f"📄 Configurazione: {config_path}")
    
    # 2. Setup Output CSV
    output_file = config['output_file']
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Header del CSV
    fieldnames = ["Experiment", "Dist", "N", "M", "Replica", "Seed", "Algo", "Params", "Time", "Obj", "Status", "Gap", "Nodes"]
    file_exists = os.path.isfile(output_file)
    
    # 3. Scansione del "Magazzino Dati" (Dataset esistente)
    dataset_root = os.path.join("data", "dataset_exam")
    if not os.path.exists(dataset_root):
        print(f"❌ Errore: Cartella dati '{dataset_root}' non trovata. Lancia generator.py prima!")
        return

    # Trova tutti i file .txt ricorsivamente
    all_files = glob.glob(os.path.join(dataset_root, "**/*.txt"), recursive=True)
    
    # Ordinamento NUMERICO (non alfabetico!) per N, M, Seed
    def sort_key(filepath):
        meta = parse_filename(os.path.basename(filepath))
        if meta:
            return (meta['n'], meta['m'], meta['dist'], meta['seed'])
        return (float('inf'), float('inf'), '', 0)  # File anomali in fondo
    
    all_files.sort(key=sort_key)
    
    # Parametri target dal JSON
    target_n = config['parameters'].get('n_values', [])
    target_m = config['parameters'].get('m_values', [])
    target_dist = config['parameters'].get('distributions', [])
    
    count = 0
    skipped = 0
    
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()

        for filepath in all_files:
            filename = os.path.basename(filepath)
            meta = parse_filename(filename)
            
            if not meta: continue
            
            # --- FILTRO INTELLIGENTE ---
            # Se l'istanza su disco non è richiesta dal JSON, la saltiamo.
            if meta['n'] not in target_n: 
                skipped += 1
                continue
            if meta['m'] not in target_m: 
                skipped += 1
                continue
            if meta['dist'] not in target_dist: 
                skipped += 1
                continue
            
            count += 1
            print(f"[{count}] Processing {meta['n']}x{meta['m']} {meta['dist']} (Seed {meta['seed']})...")
            
            # Calcola replica dal seed (5 repliche per configurazione, seed parte da 2024)
            replica = (meta['seed'] - 2024) % 5
            
            # Seleziona timer appropriato per micro/macro-benchmarking
            use_wall_clock = config.get('measure_wall_clock', False)
            timer_func = time.perf_counter if use_wall_clock else time.process_time
            timer_name = "Wall" if use_wall_clock else "CPU"
            
            # Carica Istanza
            inst = Instance(filepath)
            lb = inst.get_theoretical_lower_bound()
            
            # --- SEZIONE ALGORITMI (Dinamica) ---
            algo_conf = config.get('algorithms', {})
            
            # A. BRUTE FORCE (Solo se richiesto nel JSON)
            if algo_conf.get('brute_force', False):
                bf = PureBruteForce(inst)
                start = timer_func()
                obj, nodes = bf.solve()
                elapsed = timer_func() - start
                
                writer.writerow({
                    "Experiment": config['experiment_name'],
                    "Dist": meta['dist'], "N": meta['n'], "M": meta['m'], "Replica": replica, "Seed": meta['seed'],
                    "Algo": "BF", "Params": "Exact",
                    "Time": elapsed, "Obj": obj, "Status": "OPTIMAL", "Gap": 0.0, "Nodes": nodes
                })

            # B. BRANCH & BOUND (Solo N<=20: dominio esatto)
            # Per N>20 il B&B va in timeout sistematico: lo saltiamo per non sprecare CPU.
            bnb_best_obj = None  # Usato dall'IG per calcolare l'Optimality Gap (N<=20)
            if 'branch_and_bound' in algo_conf:
                bb_opts = algo_conf['branch_and_bound']
                if meta['n'] > 20:
                    print(f"  -> BnB skipped (N={meta['n']} > 20, heuristic domain)")
                else:
                    t_lim = bb_opts.get('time_limit', 60)
                    bnb = BranchAndBound(inst, time_limit=t_lim)

                    start = timer_func()
                    obj, nodes, status = bnb.solve()
                    elapsed = timer_func() - start

                    # BnB gap è sempre vs Lower Bound (misura qualità del lower bound)
                    gap = (obj - lb)/lb * 100 if lb > 0 else 0
                    writer.writerow({
                        "Experiment": config['experiment_name'],
                        "Dist": meta['dist'], "N": meta['n'], "M": meta['m'], "Replica": replica, "Seed": meta['seed'],
                        "Algo": "BnB", "Params": f"TL={t_lim}s",
                        "Time": elapsed, "Obj": obj, "Status": status, "Gap": gap, "Nodes": nodes
                    })
                    # Salva il risultato ottimo (solo se trovato) come riferimento per l'IG
                    if status == "OPTIMAL":
                        bnb_best_obj = obj

            # C. ITERATED GREEDY (Supporta Tuning e liste di configurazioni)
            if 'iterated_greedy' in algo_conf:
                ig_opts = algo_conf['iterated_greedy']
                # Se nel JSON è un oggetto singolo, lo trasformiamo in una lista di 1 elemento
                configs_to_run = [ig_opts] if isinstance(ig_opts, dict) else ig_opts
                
                for cfg in configs_to_run:
                    t_lim = cfg.get('time_limit', 1.0)
                    d = cfg.get('d', 4)
                    T = cfg.get('T_lambda', 0.5)
                    
                    # --- DECORRELAZIONE SEED (Cruciale) ---
                    # Usiamo il seed dell'istanza + costante fissa per l'algoritmo
                    algo_seed = meta['seed'] + 12345
                    
                    ig = IteratedGreedy(inst, time_limit=t_lim, d=d, T_lambda=T)
                    
                    start = timer_func()
                    # Passiamo il seed derivato
                    obj, iterations, _ = ig.solve(seed=algo_seed) 
                    elapsed = timer_func() - start
                    
                    # Gap a due regimi:
                    # N<=20 + BnB ottimo disponibile -> Optimality Gap (IG vs soluzione ottima)
                    # N>20 (o BnB in timeout) -> RPD vs Lower Bound teorico
                    if meta['n'] <= 20 and bnb_best_obj is not None:
                        gap = (obj - bnb_best_obj) / bnb_best_obj * 100 if bnb_best_obj > 0 else 0
                        gap_label = "OPT_GAP"
                    else:
                        gap = (obj - lb) / lb * 100 if lb > 0 else 0
                        gap_label = "RPD"

                    writer.writerow({
                        "Experiment": config['experiment_name'],
                        "Dist": meta['dist'], "N": meta['n'], "M": meta['m'], "Replica": replica, "Seed": meta['seed'],
                        "Algo": "IG", "Params": f"d={d},T={T},t={t_lim}s",
                        "Time": elapsed, "Obj": obj, "Status": f"HEURISTIC_{gap_label}", "Gap": gap, "Nodes": iterations
                    })
            
            # Scrittura su disco immediata (sicurezza contro crash)
            csvfile.flush()

    print(f"\n✅ Completato. Processate {count} istanze. Ignorate {skipped} (non matchavano il config).")
    print(f"📊 Risultati salvati in: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="Percorso del file .json di configurazione")
    args = parser.parse_args()
    
    run_experiment(args.config)