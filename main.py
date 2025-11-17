from __future__ import annotations

import argparse

from src.airalloc.data import load_instance
from src.airalloc.decoder import decode_chromosome
from src.airalloc.fitness import compute_metrics
from src.airalloc.genetic.algorithm import run_ga


def parse_args():
    p = argparse.ArgumentParser(description="AirAlloc GA prototype")
    p.add_argument("--airports", default="data/airports.csv")
    p.add_argument("--routes", default="data/routes.csv")
    p.add_argument("--aircraft", default="data/aircraft.csv")
    p.add_argument("--demand", default="data/demand.csv")
    p.add_argument("--pop", type=int, default=60)
    p.add_argument("--genes", type=int, default=40)
    p.add_argument("--generations", type=int, default=50)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main():
    args = parse_args()
    inst = load_instance(args.airports, args.routes, args.aircraft, args.demand)
    best, score = run_ga(
        inst,
        pop_size=args.pop,
        n_genes=args.genes,
        generations=args.generations,
        seed=args.seed,
    )
    schedules = decode_chromosome(best, inst)
    m = compute_metrics(schedules, inst)
    print("Melhor fitness:", score)
    print("Métricas:", m)


if __name__ == "__main__":
    main()
