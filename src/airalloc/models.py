from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Minutes = int  # minutos desde 00:00


@dataclass(frozen=True)
class Airport:
    code: str


@dataclass(frozen=True)
class Route:
    origin: str
    dest: str
    duration_min: int  # minutos de voo
    slot_from: int  # primeira decolagem possível (min)
    slot_to: int  # última decolagem possível (min)


@dataclass(frozen=True)
class Aircraft:
    id: str
    capacity: int
    base: str
    turnaround_min: int


@dataclass(frozen=True)
class DemandEntry:
    route_key: Tuple[str, str]
    dep_time: int  # centro da janela (min)
    window: int  # meia-largura da janela (min)
    pax: int


@dataclass(frozen=True)
class Gene:
    aircraft_id: str
    origin: str
    dest: str
    dep_time: int  # tempo desejado de decolagem (min)


@dataclass
class Leg:
    gene: Gene
    act_dep: int
    act_arr: int
    feasible: bool
