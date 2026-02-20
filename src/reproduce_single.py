import time
from instance import Instance
from generator import generate_instance
from algorithms import IteratedGreedy

# --- DATI PRESI DALLA RIGA DEL CSV ---
TARGET_N = 12
TARGET_M = 4
TARGET_DIST = "job_correlated"
TARGET_SEED = 66
# -------------------------------------

def reproduce():
    print(f"🔄 Riproduzione Istanza N={TARGET_N}, Seed={TARGET_SEED}...")
    
    # 1. RIGENERA L'ISTANZA (Esattamente identica a quella dell'esperimento)
    # Nota: il percorso file è temporaneo, ma il contenuto sarà bit-per-bit uguale
    path = generate_instance(TARGET_N, TARGET_M, TARGET_SEED, TARGET_DIST, base_dir="data/repro")
    inst = Instance(path)
    print(f"   Istanza generata. LB Teorico: {inst.get_theoretical_lower_bound()}")

    # 2. CONFIGURA L'ALGORITMO
    # Assicurati che questi parametri siano gli stessi del config.json usato!
    ig = IteratedGreedy(inst, time_limit=1.0, d=4, T_lambda=0.5)

    # 3. ESEGUI L'ALGORITMO
    # IMPORTANTE: Qui applichiamo la logica del seed.
    # Se nel runner hai usato "seed=current_seed", qui metti TARGET_SEED.
    # Se nel runner hai usato il fix (current_seed + 99999), mettilo anche qui!
    
    # Caso A (Senza fix):
    algo_seed = TARGET_SEED 
    # Caso B (Con fix decorrelazione):
    # algo_seed = TARGET_SEED + 99999 
    
    print(f"🧠 Avvio IG con Algo_Seed={algo_seed}...")
    start = time.perf_counter()
    sol, obj, iterations = ig.solve(seed=algo_seed)
    elapsed = time.perf_counter() - start

    print("-" * 30)
    print(f"✅ RISULTATO RIPRODOTTO: {obj}")
    print(f"⏱️  Tempo: {elapsed:.4f}s")
    print(f"📊 Iterazioni: {iterations}")
    print("-" * 30)

if __name__ == "__main__":
    reproduce()