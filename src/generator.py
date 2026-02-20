import random
import os
import shutil

def generate_instance_unrelated(n_jobs, n_machines, seed, dist_type, base_dir):
    """
    Genera istanza R||Cmax: Matrice M x N.
    Rispettando i requisiti: No commenti, No Header #, Formato rigoroso.
    """
    random.seed(seed)
    
    # Crea il percorso includendo la categoria (small/large) e la distribuzione
    os.makedirs(base_dir, exist_ok=True)
    
    filename = f"inst_{n_jobs}_{n_machines}_{dist_type}_{seed}.txt"
    filepath = os.path.join(base_dir, filename)
    
    matrix = []
    # 1. UNIFORM
    if dist_type == "uniform":
        for _ in range(n_machines):
            row = [random.randint(10, 100) for _ in range(n_jobs)]
            matrix.append(row)
                
    # 2. JOB-CORRELATED (Stress test per R||Cmax)
    elif dist_type == "job_correlated":
        # Tempi base per ogni job (eterogeneità dei job)
        base_times = [random.randint(20, 100) for _ in range(n_jobs)]
        for _ in range(n_machines):
            # Ogni macchina ha una variazione specifica sul job (eterogeneità macchine)
            row = [max(1, t + random.randint(-15, 15)) for t in base_times]
            matrix.append(row)
    
    with open(filepath, "w") as f:
        # Riga 1: N M (Senza commenti)
        f.write(f"{n_jobs} {n_machines}\n")
        # Righe successive: Matrice M x N
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")
            
    return filepath

if __name__ == "__main__":
    BASE_DIR = os.path.join("data", "dataset_exam")
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    
    BASE_SEED = 2024 # Cambiamo seed per marcare il dataset "pulito"
    seed_counter = BASE_SEED
    REPLICAS = 5 
    
    # CONFIGURAZIONE WORKHORSE (Superset per tutti i Pilot A, B, C)
    # Small: N=[8..26], M=[2..4] (Confronto B&B vs IG - Pilot A)  
    # Large: N=[30..500], M=[4..20] (Scalabilità IG - Pilot B, C)
    CONFIGS = [
        ([8, 10, 12, 14, 16, 18, 20, 22, 24, 26], [2, 4], "small"),
        ([30, 50, 100, 200, 500], [4, 5, 10, 20], "large")
    ]
    
    DISTRIBUTIONS = ["uniform", "job_correlated"]
    count = 0
    
    print("🚀 Generazione Dataset Finale per R||Cmax...")

    for n_list, m_list, tag in CONFIGS:
        for n in n_list:
            for m in m_list:
                # REQUISITO CRITICO: Salta casi banali
                if n <= m:
                    continue
                
                for dist in DISTRIBUTIONS:
                    # Cartella specifica per esperimento e distribuzione
                    current_dir = os.path.join(BASE_DIR, tag, dist)
                    for _ in range(REPLICAS):
                        generate_instance_unrelated(n, m, seed_counter, dist, current_dir)
                        seed_counter += 1
                        count += 1

    print(f"\n✅ Fatto! Generati {count} file in '{BASE_DIR}'.")
    print(f"Struttura creata:")
    print(f" - {os.path.join(BASE_DIR, 'small')} (Confronto Esatto/Euristico)")
    print(f" - {os.path.join(BASE_DIR, 'large')} (Stress test Euristico)")