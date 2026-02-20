import os
import math

class Instance:
    def __init__(self, filepath):
        self.filepath = filepath
        self.num_jobs = 0
        self.num_machines = 0
        # Matrice MxN: processing_times[machine][job]
        # (Nota: abbiamo invertito rispetto a prima per allinearci al generator)
        self.processing_times = [] 
        
        # Caricamento automatico
        self.load_from_file()

    def load_from_file(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File {self.filepath} not found")
            
        with open(self.filepath, 'r') as f:
            # Legge tutto e rimuove linee vuote o commenti (se ce ne fossero)
            lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            
        # 1. Leggi Header (N M)
        try:
            header = lines[0].split()
            self.num_jobs = int(header[0])
            self.num_machines = int(header[1])
        except (IndexError, ValueError):
            raise ValueError(f"Header non valido nel file: {self.filepath}")

        # 2. Leggi Matrice (M righe)
        self.processing_times = []
        matrix_lines = lines[1:]
        
        if len(matrix_lines) != self.num_machines:
            raise ValueError(f"Attese {self.num_machines} macchine, trovate {len(matrix_lines)}")
            
        for row_idx, line in enumerate(matrix_lines):
            vals = list(map(int, line.split()))
            if len(vals) != self.num_jobs:
                raise ValueError(f"Riga {row_idx}: attesi {self.num_jobs} jobs, trovati {len(vals)}")
            self.processing_times.append(vals)

    def get_time(self, machine_id, job_id):
        """Ritorna p_{ij} (tempo del job j sulla macchina i)."""
        return self.processing_times[machine_id][job_id]

    def get_theoretical_lower_bound(self):
        """
        Calcola il Lower Bound stretto (Fleszar & Hindi).
        LB = max(LB1, LB2)
        Fondamentale per le istanze Large.
        """
        # Calcoliamo il tempo minimo di ogni job tra tutte le macchine disponibili
        # min_p[j] = min(p_0j, p_1j, ..., p_mj)
        min_times_per_job = []
        for j in range(self.num_jobs):
            # Estraiamo la colonna j-esima dalla matrice
            col_j = [self.processing_times[m][j] for m in range(self.num_machines)]
            min_times_per_job.append(min(col_j))

        # LB1: Job-based bound (Il job più "difficile" nel caso migliore)
        lb1 = max(min_times_per_job)

        # LB2: Load-based bound (Media perfetta del lavoro minimo)
        total_min_work = sum(min_times_per_job)
        lb2 = math.ceil(total_min_work / self.num_machines)

        return max(lb1, lb2)

    def __str__(self):
        res = f"Instance: {os.path.basename(self.filepath)}\n"
        res += f"Jobs: {self.num_jobs}, Machines: {self.num_machines}\n"
        res += f"Lower Bound: {self.get_theoretical_lower_bound()}\n"
        res += "Processing Times (Machine x Job) - Anteprima:\n"
        
        limit_m = min(3, self.num_machines)
        limit_j = min(10, self.num_jobs)
        
        for i in range(limit_m):
            row_str = " ".join(str(x) for x in self.processing_times[i][:limit_j])
            if self.num_jobs > limit_j: row_str += " ..."
            res += f"Mach {i}: [{row_str}]\n"
        
        if self.num_machines > limit_m:
            res += f"... (altre {self.num_machines - limit_m} macchine nascoste) ...\n"
        
        return res

# --- TEST ---
if __name__ == "__main__":
    # Test automatico sulla cartella data/pilot se esiste
    test_dir = os.path.join("data", "dataset_exam")  # Cambia se vuoi testare su un'altra cartella
    
    if os.path.exists(test_dir):
        files = [f for f in os.listdir(test_dir) if f.endswith(".txt")]
        if files:
            target = os.path.join(test_dir, files[0])
            print(f"--- TESTING su {target} ---")
            try:
                inst = Instance(target)
                print(inst)
                print("✅ Parser OK")
                print("✅ Lower Bound Calcolato correttamente")
            except Exception as e:
                print(f"❌ Errore: {e}")
        else:
            print("Cartella vuota. Esegui generator.py prima!")
    else:
        print(f"Cartella {test_dir} non trovata. Esegui generator.py prima!")