from __future__ import annotations

import random
from typing import List, Tuple

from ..models import Gene


def tournament(pop: List[List[Gene]], scores: List[float], k: int = 3) -> List[Gene]:
    idxs = random.sample(range(len(pop)), k)
    best = min(idxs, key=lambda i: scores[i])
    return [Gene(**vars(g)) for g in pop[best]]


def one_point_crossover(
    p1: List[Gene], p2: List[Gene]
) -> Tuple[List[Gene], List[Gene]]:
    if len(p1) < 2 or len(p2) < 2:
        return p1.copy(), p2.copy()
    c = random.randint(1, min(len(p1), len(p2)) - 1)
    off1 = [Gene(**vars(g)) for g in (p1[:c] + p2[c:])]
    off2 = [Gene(**vars(g)) for g in (p2[:c] + p1[c:])]
    return off1, off2


def mutate(
    chrom: List[Gene], prob: float, aircraft_ids: List[str], airports: List[str]
) -> None:
    for i, g in enumerate(chrom):
        if random.random() < prob:
            r = random.random()
            if r < 0.33:
                chrom[i] = Gene(
                    aircraft_id=random.choice(aircraft_ids),
                    origin=g.origin,
                    dest=g.dest,
                    dep_time=g.dep_time,
                )
            elif r < 0.66:
                o = random.choice(airports)
                d = random.choice([x for x in airports if x != o])
                chrom[i] = Gene(
                    aircraft_id=g.aircraft_id, origin=o, dest=d, dep_time=g.dep_time
                )
            else:
                shift = random.randint(-15, 15)  # ±15 min
                chrom[i] = Gene(
                    aircraft_id=g.aircraft_id,
                    origin=g.origin,
                    dest=g.dest,
                    dep_time=max(0, g.dep_time + shift),
                )
