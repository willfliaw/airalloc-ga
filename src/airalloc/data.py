from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd

from .models import Aircraft, Airport, DemandEntry, Route


@dataclass
class Instance:
    airports: Dict[str, Airport]
    routes: Dict[Tuple[str, str], Route]
    aircraft: Dict[str, Aircraft]
    demands: List[DemandEntry]


def load_instance(
    airports_csv: str, routes_csv: str, aircraft_csv: str, demand_csv: str
) -> Instance:
    ap = {
        r["code"]: Airport(code=r["code"])
        for _, r in pd.read_csv(airports_csv).iterrows()
    }
    rt = {}
    for _, r in pd.read_csv(routes_csv).iterrows():
        key = (r["origin"], r["dest"])
        rt[key] = Route(
            origin=r["origin"],
            dest=r["dest"],
            duration_min=int(r["duration_min"]),
            slot_from=int(r["slot_from"]),
            slot_to=int(r["slot_to"]),
        )
    ac = {}
    for _, r in pd.read_csv(aircraft_csv).iterrows():
        ac[r["id"]] = Aircraft(
            id=r["id"],
            capacity=int(r["capacity"]),
            base=r["base"],
            turnaround_min=int(r["turnaround_min"]),
        )
    dm = []
    for _, r in pd.read_csv(demand_csv).iterrows():
        dm.append(
            DemandEntry(
                route_key=(r["origin"], r["dest"]),
                dep_time=int(r["dep_time"]),
                window=int(r["window"]),
                pax=int(r["pax"]),
            )
        )
    return Instance(ap, rt, ac, dm)


def minute(h: int, m: int) -> int:
    return h * 60 + m
