# Progetto di Scheduling - Algorithm Engineering 

[![Python](https://img.shields.io/badge/Python-3.14.0-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**Autore**: Leonardo Pinterpe

**Corso**: Algorithm Engineering  

**Anno Accademico**: 2025/2026   

## 📋 Descrizione

Progetto di ricerca su algoritmi di scheduling multiprocessore per minimizzazione del makespan. Il progetto implementa e confronta diversi algoritmi (Branch & Bound, Iterated Greedy, Brute Force) su istanze con diverse caratteristiche e distribuzioni.

## 🏗️ Struttura del Progetto

```
Scheduling_Exam_Project/
├── data/                        # Dataset di input (permanenti)
│   └── dataset_exam/           # Istanze organizzate per dimensione e tipo
├── experiments/                # Configurazioni JSON degli esperimenti
├── src/                        # Codice sorgente
│   ├── algorithms.py          # Implementazione algoritmi
│   ├── instance.py            # Gestione istanze
│   ├── runner.py              # Esecutore esperimenti
│   ├── path_utils.py          # Utility per percorsi riproducibili
│   └── plotting/              # Moduli per generazione grafici
├── results/                   # Risultati separati per immutabilità
│   ├── reference/            # Risultati originali (sola lettura prof)
│   └── generated/            # Nuove esecuzioni (riproducibili)
│       ├── csv/             # File CSV con timestamp  
│       └── plots/           # Grafici PNG/PDF con timestamp
├── docs/                     # Documentazione aggiuntiva
├── requirements.txt          # Dipendenze minimali
├── run_experiments.py        # Script principale esecuzione
└── README.md                # Questo file
```

## 🚀 Quick Start

### Prerequisiti
- **Git**: Installato e configurato
- **Python**: Versione 3.8 o superiore
- **Terminal**: PowerShell (Windows) o Bash (Linux/Mac)

### 1. Clone Repository e Setup Ambiente

```bash
# Clona la repository 
git clone https://github.com/Lpint02/Scheduling_Exam_Project.git

# Entra nella directory del progetto
cd Scheduling_Exam_Project

# Crea ambiente virtuale Python
python -m venv .venv

# Attiva ambiente (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# Attiva ambiente (Windows Command Prompt)
.venv\Scripts\activate
# Attiva ambiente (Linux/Mac) 
source .venv/bin/activate

# ⚠️ VERIFICA ATTIVAZIONE: Il prompt dovrebbe mostrare (.venv) all'inizio
# Se non vedi (.venv) nel prompt, prova:
# PowerShell con policy di esecuzione:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

# Verifica che pip punti all'ambiente virtuale
where pip
# Dovrebbe restituire: ...\Scheduling_Exam_Project\.venv\Scripts\pip.exe

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Verifica Configurazione

```bash
# Controlla che tutto sia configurato correttamente
python run_experiments.py --check-env

# 🔍 VERIFICA AGGIUNTIVA: Installazione packages nell'ambiente virtuale
pip show pandas
# Location dovrebbe essere: ...\Scheduling_Exam_Project\.venv\Lib\site-packages

pip list
# Dovresti vedere solo: pandas, matplotlib, seaborn, numpy + dipendenze

```

### 3. Esecuzione Esperimenti

```bash
# Esegui tutti gli esperimenti + genera grafici (può metterci 6 ore)
python run_experiments.py --all

# Solo esperimenti pilot (più veloce CONSIGLIATO)
python run_experiments.py --pilot

# Esperimento singolo
python run_experiments.py --config pilot_a

# Solo grafici (da risultati esistenti) 
python run_experiments.py --generate-plots
```

## 📊 Output e Risultati

### Struttura Output
- **CSV Results**: `results/generated/csv/` - File con timestamp per evitare sovrascritture
- **Grafici**: `results/generated/plots/` - PNG (alta risoluzione) + PDF (pubblicazione)
- **Riferimento**: `results/reference/` - Risultati originali immutabili

### Formato File Generati
```
pilot_a_results_20260221_143022.csv    # Timestamp: YYYYMMDD_HHMMSS
pilot_a_the_wall_20260221_143025.png
pilot_a_the_wall_20260221_143025.pdf
```

## 🔬 Esperimenti Implementati

| Esperimento | Descrizione | Obiettivo |
|-------------|-------------|-----------|
| **Pilot A** | "The Wall" - Timeout B&B con crescita istanze | Identificare soglia computazionale |
| **Pilot B** | Tuning parametri algoritmi | Ottimizzazione iperparametri |
| **Pilot C** | Convergenza vs Tempo | Analisi trade-off qualità/tempo |
| **Validation** | Validazione su istanze di controllo | Verifica robustezza algoritmi |
| **Workhorse** | Campagna sperimentale principale | Risultati finali pubblicabili |

## 🧪 Algoritmi Implementati

1. **Branch & Bound**: Algoritmo esatto con bounding intelligente
2. **Iterated Greedy**: Metaeuristica con perturbazioni controllate  
3. **Brute Force**: Enumerazione completa (solo istanze piccole)

### Caratteristiche Implementazione
- **Determinismo**: Tie-breaking rigoroso per riproducibilità
- **Robustezza**: Gestione timeout e out-of-memory
- **Efficienza**: Implementazione ottimizzata per grandi istanze

## 📈 Grafici Generati

Ogni esperimento produce visualizzazioni specifiche:

- **Pilot A**: Crescita esponenziale tempo vs dimensione istanza
- **Pilot B**: Heatmap prestazioni per tuning parametri
- **Pilot C**: Convergenza gap ottimalità vs tempo
- **Validation**: Confronto algoritmi su istanze di controllo
- **Workhorse**: Analisi completa con statistical boxplots

Tutti i grafici sono ottimizzati per pubblicazione accademica (LaTeX/Overleaf).

## 🔧 Configurazione Avanzata

### Modifica Esperimenti
File di configurazione in `experiments/` permettono customizzazione:
```json
{
  "experiment_name": "custom_test",
  "output_file": "results/generated/csv/custom_results.csv", 
  "parameters": {
    "n_values": [50, 100, 200],
    "m_values": [4, 8],
    "distributions": ["uniform", "job_correlated"],
    "replicas": 5
  },
  "algorithms": {
    "branch_and_bound": {"time_limit": 60},
    "iterated_greedy": {"iterations": 1000}
  }
}
```

## 🏛️ Riproducibilità Accademica

### Design Principles
- **Immutabilità**: Risultati originali preservati in `results/reference/`
- **Tracciabilità**: Timestamp su tutti i file generati
- **Separazione**: Input fissi vs output dinamici
- **Versioning**: Codice e configurazioni sotto controllo versione

### Garanzie
- Stesso codice + stessi dati = stessi risultati
- Nessuna sovrascrittura accidentale di risultati precedenti
- Ambiente riproducibile con `requirements.txt` minimale

## 📦 Dipendenze

Dipendenze di terze parti (vedi `requirements.txt`):
- `pandas >= 1.5.0` - Manipolazione dati CSV
- `matplotlib >= 3.6.0` - Grafici base  
- `seaborn >= 0.12.0` - Grafici statistici avanzati
- `numpy >= 1.24.0` - Calcoli numerici

Librerie Python standard utilizzate:
`os`, `time`, `csv`, `json`, `random`, `math`, `copy`, `argparse`, `datetime`

## 🚨 Troubleshooting

### Problemi Comuni

**Ambiente virtuale non attivo (Windows PowerShell)**:
Sintomo: Warning "You may have installed Python packages into your global environment"
```bash
# 1. Controlla se l'ambiente è attivo (dovresti vedere (.venv) nel prompt)
# 2. Se non attivo, abilita esecuzione scripts PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Riattiva ambiente
.\.venv\Scripts\Activate.ps1

# 4. Verifica che pip punti all'ambiente virtuale:
where pip
# Output atteso: ...\Scheduling_Exam_Project\.venv\Scripts\pip.exe

# 5. Se pip ancora globale, usa path assoluto:
.\.venv\Scripts\pip.exe install -r requirements.txt

# 6. VERIFICA SEPARAZIONE AMBIENTI:
# Con (.venv) attivo - dovresti vedere solo pacchetti progetto:
pip list
deactivate
# Senza (.venv) - dovresti vedere pacchetti diversi:  
pip list
```
**Nota**: Il warning VS Code a volte da falsi positivi su Windows anche con configurazione corretta.

**Errore import moduli**:
```bash
# Assicurati di eseguire dalla directory principale
cd Scheduling_Exam_Project  
python run_experiments.py --all
```

**Directory mancanti**:
```bash
# Lo script crea directory automaticamente, ma puoi forzare:
python run_experiments.py --check-env
```

**Dipendenze mancanti**:
```bash
# Reinstall completo
pip install -r requirements.txt --force-reinstall
```

**Out of memory su istanze grandi**:
- Modifica `time_limit` nei file JSON di configurazione
- Su macchine lente, riduci dimensioni istanze nei parametri

### Download Dataset
Se la cartella `data/dataset_exam/` è vuota:
```bash
python src/generator.py  # Genera dataset da configurazione
```

## 📞 Supporto

Per problemi di esecuzione:
1. Verifica ambiente con `python run_experiments.py --check-env`  
2. Controlla log di output per errori specifici
3. Consulta troubleshooting sopra

## 📄 Licenza e Citazioni

Progetto sviluppato per scopi didattici. 
Citazione algoritmi di riferimento disponibile nei commenti del codice.

---

