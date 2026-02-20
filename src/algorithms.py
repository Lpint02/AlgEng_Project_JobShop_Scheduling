import time
import math
import random
import copy

# =============================================================================
# 1. SHARED HEURISTIC (Greedy LPT - Deterministic)
# =============================================================================

def greedy_lpt_solve(instance):
    """
    Euristica costruttiva LPT (Longest Processing Time first).
    DETERMINISTICA: A parità di tempo medio, usa il Job ID per rompere i pareggi.
    
    Ritorna: (makespan, assignment)
    """
    n = instance.num_jobs
    m = instance.num_machines
    
    # 1. Calcola tempo medio per ogni job
    job_stats = []
    for j in range(n):
        avg_time = sum(instance.processing_times[i][j] for i in range(m)) / m
        job_stats.append((j, avg_time))
    
    # 2. Ordina decrescente (Job pesanti prima)
    # TIE-BREAKING RIGOROSO: 
    # Ordina per (MediaTempo, JobID). Se MediaTempo è uguale, il JobID (che è unico) decide.
    # Questo rende l'algoritmo indipendente dall'ordine di input nel file.
    sorted_jobs = sorted(job_stats, key=lambda x: (x[1], x[0]), reverse=True)
    
    machine_loads = [0] * m
    assignment = [-1] * n
    
    # 3. Assegnamento
    for job_info in sorted_jobs:
        job_id = job_info[0]
        
        best_machine = -1
        min_load_after = float('inf')
        
        # Tie-breaking anche sulle macchine: a parità di carico, prende la macchina con indice minore
        for machine in range(m):
            proc_time = instance.get_time(machine, job_id)
            curr_load = machine_loads[machine] + proc_time
            
            if curr_load < min_load_after:
                min_load_after = curr_load
                best_machine = machine
        
        assignment[job_id] = best_machine
        machine_loads[best_machine] += instance.get_time(best_machine, job_id)
        
    makespan = max(machine_loads)
    return makespan, assignment


# =============================================================================
# 2. EXACT ALGORITHM (Branch & Bound - Deterministic)
# =============================================================================

class BranchAndBound:
    def __init__(self, instance, time_limit=60):
        self.instance = instance
        self.time_limit = time_limit
        self.start_time = 0
        self.nodes_explored = 0
        self.timed_out = False
        
        self.best_makespan = float('inf')
        self.best_assignment = []

    def solve(self):
        # USARE PROCESS_TIME per misurare solo i cicli CPU (no Spotify/Chrome interference)
        self.start_time = time.process_time()
        self.nodes_explored = 0
        self.timed_out = False
        
        # 1. Hot Start
        ub, assign = greedy_lpt_solve(self.instance)
        self.best_makespan = ub
        self.best_assignment = list(assign)
        
        # 2. Ordinamento Job (LPT rule per il branching order)
        n = self.instance.num_jobs
        m = self.instance.num_machines
        
        jobs_with_index = []
        for j in range(n):
            avg_p = sum(self.instance.processing_times[i][j] for i in range(m)) / m
            jobs_with_index.append((j, avg_p))
            
        # TIE-BREAKING: Anche qui, usiamo il Job ID come seconda chiave
        sorted_jobs = sorted(jobs_with_index, key=lambda x: (x[1], x[0]), reverse=True)
        sorted_job_indices = [x[0] for x in sorted_jobs]

        # 3. Start Recursion
        initial_loads = [0] * m
        current_assignment = [-1] * n
        
        self._recursive_search(0, sorted_job_indices, initial_loads, current_assignment)
        
        status = "TIMEOUT" if self.timed_out else "OPTIMAL"
        return self.best_makespan, self.nodes_explored, status

    def _recursive_search(self, step_idx, sorted_jobs, current_loads, current_assignment):
        # Check Timeout ogni 1000 nodi usando process_time
        if self.nodes_explored % 1000 == 0:
            if (time.process_time() - self.start_time) > self.time_limit:
                self.timed_out = True
                return

        # Pruning Globale
        if max(current_loads) >= self.best_makespan:
            return

        # Caso Base: Foglia
        if step_idx == self.instance.num_jobs:
            current_max = max(current_loads)
            if current_max < self.best_makespan:
                self.best_makespan = current_max
                self.best_assignment = list(current_assignment)
            return

        self.nodes_explored += 1
        job_original_id = sorted_jobs[step_idx]
        
        for m in range(self.instance.num_machines):
            time_on_machine = self.instance.get_time(m, job_original_id)
            
            # Pruning Locale
            if current_loads[m] + time_on_machine >= self.best_makespan:
                continue

            # Do Move
            current_loads[m] += time_on_machine
            current_assignment[job_original_id] = m
            
            # Recurse
            self._recursive_search(step_idx + 1, sorted_jobs, current_loads, current_assignment)
            
            # Backtrack
            if self.timed_out: return
            current_loads[m] -= time_on_machine


# =============================================================================
# 3. META-HEURISTIC (Iterated Greedy - Stochastic & Encapsulated)
# =============================================================================

class IteratedGreedy:
    def __init__(self, instance, time_limit=60, d=4, T_lambda=0.5):
        self.instance = instance
        self.time_limit = time_limit
        self.d = d 
        self.T_lambda = T_lambda
        
        self.start_time = 0
        self.best_makespan = float('inf')
        self.best_assignment = []
        
        # Generatore locale (sarà inizializzato in solve)
        self.rng = None 

    def solve(self, seed=42):
        # INCAPSULAMENTO TOTALE DELLA CASUALITÀ
        # Creiamo un'istanza Random locale. Il global random di Python non viene toccato.
        self.rng = random.Random(seed)
        
        self.start_time = time.process_time() # CPU Time
        
        # 1. INITIALIZATION (Deterministica LPT)
        curr_makespan, curr_assign = greedy_lpt_solve(self.instance)
        curr_loads = self._calculate_loads(curr_assign)
        
        self.best_makespan = curr_makespan
        self.best_assignment = list(curr_assign)
        
        # Calcolo Temperatura (Fanjul-Peyro)
        total_proc_time = sum(sum(row) for row in self.instance.processing_times)
        n = self.instance.num_jobs
        m = self.instance.num_machines
        temperature = self.T_lambda * (total_proc_time / (10 * n * m))
        if temperature == 0: temperature = 0.1
        
        iter_count = 0
        
        # 2. MAIN LOOP
        while (time.process_time() - self.start_time) < self.time_limit:
            iter_count += 1
            
            destruct_assign = list(curr_assign)
            
            # --- A. DESTRUCTION (Uso self.rng) ---
            # sample estrae senza ripetizione
            removed_jobs = self.rng.sample(range(n), self.d)
            
            partial_loads = [0] * m
            for j in range(n):
                if j not in removed_jobs:
                    mach = destruct_assign[j]
                    partial_loads[mach] += self.instance.get_time(mach, j)
            
            # --- B. CONSTRUCTION ---
            for job in removed_jobs:
                best_m = -1
                best_makespan_increase = float('inf')
                
                current_Cmax = max(partial_loads)
                
                for mach in range(m):
                    p_time = self.instance.get_time(mach, job)
                    new_load = partial_loads[mach] + p_time
                    cost = max(current_Cmax, new_load)
                    
                    if cost < best_makespan_increase:
                        best_makespan_increase = cost
                        best_m = mach
                
                destruct_assign[job] = best_m
                partial_loads[best_m] += self.instance.get_time(best_m, job)
            
            # --- C. LOCAL SEARCH ---
            new_assign, new_makespan = self._local_search(destruct_assign, partial_loads)
            
            # --- D. ACCEPTANCE (Uso self.rng) ---
            accept = False
            delta = new_makespan - curr_makespan
            
            if delta < 0:
                accept = True
            else:
                prob = math.exp(-delta / temperature)
                # random() locale
                if self.rng.random() < prob:
                    accept = True
            
            if accept:
                curr_assign = new_assign
                curr_makespan = new_makespan
                curr_loads = self._calculate_loads(curr_assign)
                
                if curr_makespan < self.best_makespan:
                    self.best_makespan = curr_makespan
                    self.best_assignment = list(curr_assign)
                    
        return self.best_makespan, iter_count, "HEURISTIC"

    def _calculate_loads(self, assignment):
        loads = [0] * self.instance.num_machines
        for j, m in enumerate(assignment):
            loads[m] += self.instance.get_time(m, j)
        return loads

    def _local_search(self, assignment, loads):
        m = self.instance.num_machines
        curr_makespan = max(loads)
        
        # Macchina Critica
        # Nota: Qui l'ordine è deterministico (la prima che trova), ma la scelta dei job
        # da muovere sarà mescolata casualmente
        critical_machines = [i for i, load in enumerate(loads) if load == curr_makespan]
        critical_mach = critical_machines[0]
        
        jobs_on_critical = [j for j, mach in enumerate(assignment) if mach == critical_mach]
        
        # Shuffle locale (per non provare sempre lo stesso ordine)
        self.rng.shuffle(jobs_on_critical)
        
        for job in jobs_on_critical:
            time_on_critical = self.instance.get_time(critical_mach, job)
            
            for dest_mach in range(m):
                if dest_mach == critical_mach: continue
                
                time_on_dest = self.instance.get_time(dest_mach, job)
                
                new_load_critical = loads[critical_mach] - time_on_critical
                new_load_dest = loads[dest_mach] + time_on_dest
                
                if new_load_dest >= curr_makespan:
                    continue
                
                # Check veloce
                if max(new_load_dest, new_load_critical) < curr_makespan:
                     # Check completo per sicurezza (ci potrebbero essere altre macchine al max)
                    temp_loads = list(loads)
                    temp_loads[critical_mach] -= time_on_critical
                    temp_loads[dest_mach] += time_on_dest
                    
                    if max(temp_loads) < curr_makespan:
                        new_assignment = list(assignment)
                        new_assignment[job] = dest_mach
                        return new_assignment, max(temp_loads)
                    
        return assignment, curr_makespan
    

class PureBruteForce:
    def __init__(self, instance):
        self.instance = instance
        self.best_makespan = float('inf')
        self.nodes_visited = 0 # Contiamo i nodi per dimostrare l'esaustività

    def solve(self):
        self.best_makespan = float('inf')
        self.nodes_visited = 0
        initial_loads = [0] * self.instance.num_machines
        
        # Start recursion
        self._search(0, initial_loads)
        
        return self.best_makespan, self.nodes_visited

    def _search(self, job_idx, current_loads):
        self.nodes_visited += 1
        
        # CASO BASE: Foglia
        if job_idx == self.instance.num_jobs:
            current_max = max(current_loads)
            if current_max < self.best_makespan:
                self.best_makespan = current_max
            return

        # NESSUN PRUNING QUI! 
        # Esploriamo ciecamente ogni ramo, anche se fa schifo.
        
        for m in range(self.instance.num_machines):
            time_p = self.instance.get_time(m, job_idx)
            
            # Do move
            current_loads[m] += time_p
            
            # Recurse
            self._search(job_idx + 1, current_loads)
            
            # Backtrack
            current_loads[m] -= time_p
