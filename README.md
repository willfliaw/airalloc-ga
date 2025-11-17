<h1 align="center">🛫 AirAlloc-GA (WIP)</h1>
<h3 align="center">Aircraft Allocation via Genetic Algorithms</h3>

<p align="center">
  <strong>Authors:</strong> Davi Valério · Diogo Silva · Eduardo Cabrera · William Liaw<br>
  <strong>Discipline:</strong> PSI3472 – Concepção e Implementação de Sistemas Eletrônicos Inteligentes<br>
  <strong>Institution:</strong> Escola Politécnica da Universidade de São Paulo (EPUSP)
</p>

## 📘 Overview

**AirAlloc-GA** is an elegant and modular Python project designed to study the use of **Genetic Algorithms (GA)** for the **allocation of aircraft** to national flight demands.
The system models airports, routes, fleets, and passenger demand to generate feasible flight schedules that balance **capacity utilization, punctuality, and operational efficiency**.

Unlike exact optimization approaches (e.g., Mixed-Integer Programming), this evolutionary method efficiently explores large combinatorial spaces to produce **high-quality near-optimal solutions** within practical computational limits.

## 🧩 Core Concepts

- **Genotype:** Encodes potential flight assignments as ordered sequences of *genes*, each representing a flight leg
  `Gene = (aircraft_id, origin, destination, departure_time)`.

- **Phenotype:** Decoded operational plan ensuring spatial and temporal feasibility
  (correct airport transitions, turnaround times, slot constraints).

- **Fitness:** Aggregated scalar score combining unmet demand, delay penalties, ferry flights, and structural infeasibilities.
  Lower values correspond to better overall performance.

## 🗂️ Project Structure

```

airalloc/
│
├── src/airalloc/
│   ├── models.py         # Domain entities (Airport, Route, Aircraft, Gene, etc.)
│   ├── data.py           # Data loading utilities and synthetic dataset generator
│   ├── decoder.py        # Genotype → phenotype conversion (feasibility checks)
│   ├── fitness.py        # Metric aggregation and fitness computation
│   ├── visualize.py      # Network visualization using NetworkX + Matplotlib
│   └── genetic/
│       ├── operators.py  # Selection, crossover, mutation operators
│       └── algorithm.py  # Core GA evolutionary loop
│
├── data/                 # Example CSV datasets (airports, routes, aircraft, demand)
├── tests/                # Basic smoke tests
├── main.py               # CLI entry point for experiments
├── pyproject.toml        # Build configuration and dependencies
└── README.md

````

## ⚙️ Environment Setup with Conda

### 1️⃣ Install or Update Conda
Download **Miniconda** or **Anaconda**, then verify:
```bash
conda --version
conda update -n base -c defaults conda
````

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/willfliaw/airalloc-ga.git
cd airalloc-ga
```

### 3️⃣ Create a Virtual Environment

Create a clean environment with Python 3.10 (or newer):

```bash
conda create -n airalloc python=3.10
```

### 4️⃣ Activate the Environment

```bash
conda activate airalloc
```

### 5️⃣ Install Dependencies

Install the package in editable mode (recommended for development):

```bash
pip install -e .
```

This installs all dependencies listed in **`pyproject.toml`** (`pandas`, `numpy`, `matplotlib`, `networkx`, etc.).

## 🚀 Usage

Example run with custom parameters:

```bash
python main.py --seed 42 --generations 50 --pop 60
```

| Argument        | Description                    | Default |
| --------------- | ------------------------------ | ------- |
| `--pop`         | Population size                | 60      |
| `--genes`       | Number of genes per chromosome | 40      |
| `--generations` | Number of generations          | 50      |
| `--seed`        | Random seed (reproducibility)  | 42      |

## 📊 Metrics & Fitness Evaluation

The **fitness function** aggregates the key operational metrics:

| Metric                      | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| **Demand Satisfaction (%)** | Percentage of passenger demand effectively served    |
| **Average Delay (min)**     | Mean deviation between desired and actual departures |
| **Fleet Utilization**       | Total flight versus ground time ratio                |
| **Ferry Flights**           | Number of repositioning legs without passengers      |
| **Operational Cost Proxy**  | Weighted penalty score combining all above           |

These indicators form the *objective landscape* evaluated by the GA—
solutions with **lower fitness values** represent more efficient and feasible schedules.

## 🖼️ Visualization (Optional)

`visualize.py` provides a simple route-network graph using **NetworkX** + **Matplotlib**, illustrating airport connectivity and flight legs.

```python
from src.airalloc.visualize import plot_network
plot_network(instance, schedules)
```

## 🧠 Future Extensions

* Multi-objective (Pareto-front) optimization
* Stochastic demand modeling and robustness analysis
* 3D/animated visualization of fleet trajectories

## 🧾 License

Released under the **MIT License** — free for academic and research use.
