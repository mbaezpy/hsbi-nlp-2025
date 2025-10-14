# HSBI — Natural Language Processing (NLP) — 2025

Course repository for **HSBI NLP 2025**.  
Contains lab notebooks, helper scripts and utilities used during the course.

---

## Repository layout
```
├── labs/                     # Jupyter notebooks for each lab (Lab1, Lab2, …)
├── scripts/                  # environment installation script, etc.
├── utils/                    # helper scripts: dataset downloaders, etc.
└── README.md                 # this file
```

---

## Quick start (recommended)

> These instructions assume you have a Linux workstation or a cluster node with Conda available.
> If you use a remote cluster, follow the cluster guidelines (module load miniconda3, submit jobs, etc.).

1. **Clone the repository**

```bash
git clone https://github.com/your-org/hsbi-nlp-2025.git
cd hsbi-nlp-2025
```

2.	**Install the course environment**

The repository includes an installation script that creates the nlp-course conda environment and installs the required packages.

```bash
# run the installer (interactive script)
bash scripts/install_env.sh
```

If the script fails or you prefer to run steps manually, open scripts/install_env.sh and follow the commands it contains (it creates a conda env, installs PyTorch, transformers, datasets, nltk, spaCy, etc., and registers a Jupyter kernel).


3.	**Activate the environment (if not done by the script)**
```bash
conda activate nlp-course
```

4.	**Start JupyterLab**
Start a jupyter notebook in the cluster (following the YourAI dashboard instructions). If you're running it locally, you can launch jupyter lab in your terminal.

```bash
jupyter lab
# or, on a headless server:
jupyter lab --ip=0.0.0.0 --no-browser --port=8888
```