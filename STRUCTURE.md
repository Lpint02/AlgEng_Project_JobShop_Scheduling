# Struttura della Repository - Progetto di Scheduling

```
Scheduling_Exam_Project/
├── data/                        # Dati di input (invarianti)
│   └── dataset_exam/
│       ├── small/
│       └── large/
├── experiments/                 # Configurazioni degli esperimenti
│   ├── config_pilot_a.json
│   ├── config_pilot_b.json
│   └── ...
├── src/                        # Codice sorgente
│   ├── __init__.py
│   ├── algorithms.py
│   ├── generator.py
│   ├── instance.py
│   ├── reproduce_single.py
│   ├── runner.py
│   └── plotting/
│       ├── __init__.py
│       ├── generate_all_plots.py
│       └── plot_*.py
├── results/                    # Risultati (separati per immutabilità)
│   ├── reference/             # Risultati originali (sola lettura per il prof)
│   │   ├── pilot_b_tuning.csv
│   │   ├── pilot_c_convergence.csv
│   │   ├── pilot_wall_results.csv
│   │   ├── validation_results.csv
│   │   └── workhorse_results.csv
│   └── generated/             # Nuove esecuzioni (auto-generati)
│       ├── csv/               # File CSV dei risultati
│       └── plots/             # Grafici generati
├── docs/                      # Documentazione del progetto
│   └── README.md              # Istruzioni complete
├── requirements.txt           # Dipendenze minimali
├── .gitignore                 # File da ignorare
└── run_experiments.py         # Script principale di esecuzione
```

## Vantaggi della struttura:
- **results/reference/**: Risultati immutabili per il professore
- **results/generated/**: Output dinamici riproducibili  
- **Separazione chiara**: Input fissi vs output variabili
- **Tracciabilità**: Ogni esecuzione genera timestamp nei file