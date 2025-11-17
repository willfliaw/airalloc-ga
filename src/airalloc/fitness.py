from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from .data import Instance
from .models import Leg


def _bin10(t: int) -> int:
    return (t // 10) * 10


def evaluate_demands(
    schedules: Dict[str, List[Leg]], inst: Instance
) -> Dict[Tuple[str, str, int], int]:
    """Oferta de assentos por rota e partida (arredonda horários em bins de 10 min)."""
    supply = defaultdict(int)
    for ac_id, legs in schedules.items():
        cap = inst.aircraft[ac_id].capacity
        for lg in legs:
            if not lg.feasible:
                continue
            key = (lg.gene.origin, lg.gene.dest, _bin10(lg.act_dep))
            supply[key] += cap
    return supply


def compute_metrics(schedules: Dict[str, List[Leg]], inst: Instance) -> dict:
    supply = evaluate_demands(schedules, inst)
    unmet, delay_sum, offsched, ferries = 0, 0, 0, 0
    flight_count = 0

    for ac_id, legs in schedules.items():
        prev_dest = inst.aircraft[ac_id].base
        for lg in legs:
            flight_count += 1
            if not lg.feasible:
                offsched += 1
            if lg.gene.origin != prev_dest:
                ferries += 1
            if lg.feasible:
                delay_sum += max(0, lg.act_dep - lg.gene.dep_time)
            prev_dest = lg.gene.dest

    for d in inst.demands:
        offered = 0
        for dt in range(d.dep_time - d.window, d.dep_time + d.window + 1, 10):
            offered += supply.get((d.route_key[0], d.route_key[1], max(0, dt)), 0)
        unmet += max(0, d.pax - offered)

    total_pax = sum(d.pax for d in inst.demands)
    pct_served = 0.0 if total_pax == 0 else (1 - unmet / total_pax) * 100.0

    return {
        "pct_demanda_atendida": pct_served,
        "atraso_medio_min": 0.0 if flight_count == 0 else delay_sum / flight_count,
        "voos_fora_da_estrutura": offsched,
        "reposicionamentos": ferries,
        "total_pernas": flight_count,
        "demanda_nao_atendida": unmet,
    }


def fitness(metrics: dict, w_unmet=10.0, w_delay=0.05, w_ferry=0.5, w_off=2.0) -> float:
    """Menor é melhor (combinação linear de métricas)."""
    return (
        w_unmet * metrics["demanda_nao_atendida"]
        + w_delay * metrics["atraso_medio_min"] * metrics["total_pernas"]
        + w_ferry * metrics["reposicionamentos"]
        + w_off * metrics["voos_fora_da_estrutura"]
    )
