# Progetto di Scheduling - Algorithm Engineering 

[![Python](https://img.shields.io/badge/Python-3.14.0-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**Autore**: Leonardo Pinterpe

**Corso**: Algorithm Engineering  

**Anno Accademico**: 2025/2026   

## 📋 Descrizione

Progetto di ricerca su algoritmi di scheduling multiprocessore per minimizzazione del makespan. Il progetto implementa e confronta diversi algoritmi (Branch & Bound, Iterated Greedy, Brute Force) su istanze con diverse caratteristiche e distribuzioni.

## 🏗️ Struttura del Progetto

```
AlgEng_Scheduling_Project/
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
- **Python**: Versione 3.8+ (Linux: potrebbe essere necessario `python3-venv`)

## 🐧 Setup Linux/Mac

```bash
# Clona la repository
git clone https://github.com/Lpint02/AlgEng_Scheduling_Project.git
cd AlgEng_Scheduling_Project

# Crea ambiente virtuale Python  
python3 -m venv .venv

# Se errore "python: comando non trovato" o "ensurepip is not available":
sudo apt update && sudo apt install -y python3 python3-venv  # Debian/Ubuntu
# brew install python3  # macOS con Homebrew

# Attiva ambiente virtuale
source .venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Verifica installazione
python run_experiments.py --check-env
```

## 🪟 Setup Windows

### PowerShell (Raccomandato)
```powershell
# Clona la repository
git clone https://github.com/Lpint02/AlgEng_Scheduling_Project.git
cd AlgEng_Scheduling_Project

# Crea ambiente virtuale
python -m venv .venv

# Attiva ambiente virtuale
.\.venv\Scripts\Activate.ps1

# Se errore di ExecutionPolicy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

# Installa dipendenze  
pip install -r requirements.txt

# Verifica installazione
python run_experiments.py --check-env
```

### Command Prompt (Alternativa)
```cmd
# Dopo il clone e creazione venv:
.venv\Scripts\activate
pip install -r requirements.txt
python run_experiments.py --check-env
```

## 🧪 Esecuzione Esperimenti

```bash
# Mostra tutte le opzioni disponibili
python run_experiments.py --help

# Esegui tutti gli esperimenti + genera grafici (può richiedere diverse ore)
python run_experiments.py --all

# Solo esperimenti pilot (più veloce - CONSIGLIATO per test)
python run_experiments.py --pilot

# Esperimenti singoli
python run_experiments.py --config pilot_a      # Analisi "The Wall" 
python run_experiments.py --config pilot_b      # Tuning parametri
python run_experiments.py --config pilot_c      # Analisi convergenza
python run_experiments.py --config validation   # Solo validazione
python run_experiments.py --config workhorse    # Esperimento principale (puo richiedere diverse ore)

# Solo generazione grafici (da risultati esistenti) 
python run_experiments.py --generate-plots
```

## ✅ Verifica Installazione (Opzionale)

Ti consigliamo di verificare che l'ambiente sia configurato correttamente:

### Controlli Base
```bash
# Il prompt dovrebbe mostrare (.venv) quando l'ambiente è attivo
python run_experiments.py --check-env

# Verifica che pip punti all'ambiente virtuale
pip --version  # Dovrebbe mostrare path con .venv
```

### Controlli Dettagliati
```bash
# Verifica pacchetti nell'ambiente virtuale
pip list  # Solo pandas, matplotlib, seaborn, numpy + dipendenze

# Verifica installazione specifica
pip show pandas  # Location dovrebbe contenere .venv

# Su Windows PowerShell, verifica comando pip
Get-Command pip  # Dovrebbe puntare a .venv\Scripts\pip.exe
```

## 📊 Output e Risultati

### Struttura Output
- **CSV Results**: `results/generated/csv/` - File con timestamp per evitare sovrascritture
- **Grafici**: `results/generated/plots/` - PDF ottimizzati per pubblicazione
- **Riferimento**: `results/reference/` - Risultati originali immutabili

### Formato File Generati
```
pilot_a_results_20260221_143022.csv    # CSV: Timestamp YYYYMMDD_HHMMSS
pilot_a_the_wall.pdf                   # PDF: Nome fisso (sovrascrive)
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

### Problemi Comuni per Piattaforma

#### 🐧 Linux
```bash
# "python: comando non trovato"  
python3 -m venv .venv  # Usa python3 invece di python
source .venv/bin/activate

# "ensurepip is not available"
sudo apt update && sudo apt install python3 python3-venv  # Debian/Ubuntu
sudo dnf install python3 python3-pip  # Fedora/RHEL
```

#### 🪟 Windows
```powershell
# Ambiente virtuale non attivabile in PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

# Se pip punta ancora all'ambiente globale
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### Problemi Generali

**Errore import moduli**:
```bash
# Assicurati di eseguire dalla directory principale del progetto
cd AlgEng_Project_JobShop_Scheduling  
python run_experiments.py --check-env
```

**Dipendenze corrotte**:
```bash
pip install -r requirements.txt --force-reinstall
```

**Out of memory su istanze grandi**:
- Modifica `time_limit` nei file di configurazione JSON
- Riduci dimensioni istanze nei parametri per macchine lente

**Directory risultati mancanti**:
```bash
python run_experiments.py --check-env  # Crea directory automaticamente
```

### Note Aggiuntive

- **Dataset mancante**: Se `data/dataset_exam/` è vuoto, esegui `python src/generator.py`

## 📞 Supporto

Per problemi di esecuzione:
1. Verifica ambiente con `python run_experiments.py --check-env`  
2. Controlla log di output per errori specifici
3. Consulta troubleshooting sopra

## 📄 Licenza e Citazioni

Progetto sviluppato per scopi didattici. 
Citazione algoritmi di riferimento disponibile nei commenti del codice.

---

