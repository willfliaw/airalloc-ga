from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .data import Instance
from .models import Aircraft, Gene, Leg


def decode_chromosome(chromosome: List[Gene], inst: Instance) -> Dict[str, List[Leg]]:
    """Gera a programação por aeronave, checando conectividade espacial e temporal básica."""
    by_ac: Dict[str, List[Gene]] = defaultdict(list)
    for g in chromosome:
        by_ac[g.aircraft_id].append(g)
    for k in by_ac:
        by_ac[k].sort(key=lambda x: x.dep_time)

    schedules: Dict[str, List[Leg]] = defaultdict(list)
    for ac_id, genes in by_ac.items():
        ac: Aircraft = inst.aircraft[ac_id]
        cur_airport = ac.base
        cur_time = 0
        for g in genes:
            rkey = (g.origin, g.dest)
            if rkey not in inst.routes:
                schedules[ac_id].append(
                    Leg(g, max(cur_time, g.dep_time), max(cur_time, g.dep_time), False)
                )
                continue
            route = inst.routes[rkey]
            feasible = g.origin == cur_airport
            dep = max(cur_time, g.dep_time, route.slot_from)
            if dep > route.slot_to:
                feasible = False
            arr = dep + route.duration_min
            cur_airport = route.dest
            cur_time = arr + ac.turnaround_min
            schedules[ac_id].append(Leg(g, dep, arr, feasible))
    return schedules
