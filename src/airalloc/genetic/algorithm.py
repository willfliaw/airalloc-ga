from __future__ import annotations

import random
from typing import List, Tuple

from ..data import Instance
from ..decoder import decode_chromosome
from ..fitness import compute_metrics, fitness
from ..models import Gene
from .operators import mutate, one_point_crossover, tournament


def init_population(
    size: int,
    n_genes: int,
    aircraft_ids: List[str],
    airports: List[str],
    seed: int | None = None,
) -> List[List[Gene]]:
    rnd = random.Random(seed)
    pop: List[List[Gene]] = []
    for _ in range(size):
        chrom = []
        for __ in range(n_genes):
            o = rnd.choice(airports)
            d_choices = [x for x in airports if x != o]
            d = rnd.choice(d_choices)
            dep = rnd.randint(6 * 60, 22 * 60)  # 06:00–22:00
            chrom.append(
                Gene(
                    aircraft_id=rnd.choice(aircraft_ids), origin=o, dest=d, dep_time=dep
                )
            )
        pop.append(chrom)
    return pop


def evaluate_population(pop: List[List[Gene]], inst: Instance) -> List[float]:
    scores = []
    for chrom in pop:
        schedules = decode_chromosome(chrom, inst)
        m = compute_metrics(schedules, inst)
        scores.append(fitness(m))
    return scores


def run_ga(
    inst: Instance,
    pop_size=60,
    n_genes=40,
    generations=50,
    cx_prob=0.8,
    mut_prob=0.1,
    seed: int | None = None,
) -> Tuple[List[Gene], float]:
    rnd = random.Random(seed)
    aircraft_ids = list(inst.aircraft.keys())
    airports = list(inst.airports.keys())

    pop = init_population(pop_size, n_genes, aircraft_ids, airports, seed=seed)
    scores = evaluate_population(pop, inst)

    for _ in range(generations):
        new_pop: List[List[Gene]] = []
        while len(new_pop) < pop_size:
            p1 = tournament(pop, scores, k=3)
            p2 = tournament(pop, scores, k=3)
            if rnd.random() < cx_prob:
                o1, o2 = one_point_crossover(p1, p2)
            else:
                o1, o2 = p1, p2
            mutate(o1, mut_prob, aircraft_ids, airports)
            mutate(o2, mut_prob, aircraft_ids, airports)
            new_pop.extend([o1, o2])
        pop = new_pop[:pop_size]
        scores = evaluate_population(pop, inst)

    best_idx = min(range(len(pop)), key=lambda i: scores[i])
    return pop[best_idx], scores[best_idx]
