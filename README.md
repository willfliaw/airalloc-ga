<h1 align="center">🛫 AirAlloc-GA (WIP)</h1>
<h3 align="center">Aircraft Allocation via Genetic Algorithms</h3>

<p align="center">
  <strong>Authors:</strong> Davi Valério · Diogo Silva · Eduardo Cabrera · William Liaw<br>
  <strong>Discipline:</strong> PSI3472 – Concepção e Implementação de Sistemas Eletrônicos Inteligentes<br>
  <strong>Institution:</strong> Escola Politécnica da Universidade de São Paulo (EPUSP)
</p>

## 📘 Overview

**AirAlloc-GA** is an elegant, modular Python project designed to explore the use of **Genetic Algorithms (GA)** for the **allocation of aircraft** to scheduled national flight demands.
The system models airports, routes, fleets, and passenger demand to generate feasible flight schedules that balance **capacity utilization, punctuality, and operational efficiency**.

Unlike exact optimization methods (e.g., Mixed-Integer Programming), this evolutionary approach efficiently searches large combinatorial spaces to produce **high-quality near-optimal solutions** within realistic computational limits.

## 🧩 Core Concepts

-   **Genotype:** Encodes potential flight assignments as sequences of _genes_, each representing a flight leg `(aircraft, origin, destination, departure_time)`.
-   **Phenotype:** Decoded operational plan ensuring spatial and temporal feasibility (correct airport transitions, turnaround times, etc.).
-   **Fitness:** Aggregated measure combining unmet demand, delay penalties, ferry flights, and infeasibilities into a single optimization score.

## 🗂️ Project Structure

```
airalloc/
│
├── src/airalloc/
│   ├── models.py         # Domain models (Airports, Routes, Aircraft, Genes)
│   ├── data.py           # Instance loading and synthetic data generator
│   ├── decoder.py        # Converts genotype → phenotype ensuring feasibility
│   ├── fitness.py        # Fitness calculation and evaluation metrics
│   ├── visualize.py      # Route network visualization (optional)
│   └── genetic/
│       ├── operators.py  # Selection, crossover, and mutation operators
│       └── algorithm.py  # Main GA loop and evolutionary flow
│
├── data/                 # Example CSV datasets (airports, routes, etc.)
├── tests/                # Unit tests for smoke validation
├── main.py               # Entry point for running experiments
├── pyproject.toml        # Project configuration
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/willfliaw/airalloc-ga.git
cd airalloc-ga
pip install -e .
```

## 🚀 Usage

Example execution with custom parameters:

```bash
python main.py --seed 42 --generations 50 --pop 60
```

### Parameters

| Argument        | Description                     | Default |
| --------------- | ------------------------------- | ------- |
| `--pop`         | Population size                 | 60      |
| `--genes`       | Genes per chromosome            | 40      |
| `--generations` | Number of generations           | 50      |
| `--seed`        | Random seed for reproducibility | 42      |

## 📊 Metrics & Fitness Evaluation

The **fitness function** aggregates the main operational metrics:

-   **Demand satisfaction (%):** share of total passenger demand served.
-   **Average delay (min):** mean departure deviation from target schedule.
-   **Fleet utilization:** total flight vs. ground time.
-   **Ferry flights:** repositioning without passengers.
-   **Operational cost proxy:** weighted penalty score.

Lower fitness values indicate better solutions.

## 🖼️ Visualization (optional)

The module `visualize.py` provides a simple **route network graph** using NetworkX and Matplotlib, helping to illustrate airport connectivity and flight routes.

Example:

```python
from src.airalloc.visualize import plot_network
plot_network(instance, schedules)
```

## 🧠 Future Extensions

-   3D/animated visualization of fleet movements
-   Multi-objective Pareto optimization

## 🧾 License

This project is released under the **MIT License**.
Feel free to use, modify, and extend it for research or academic purposes.
