from __future__ import annotations

from typing import Dict
from typing import Dict as _Dict
from typing import List
from typing import List as _List
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx
import pandas as _pd

from .data import Instance
from .models import Leg


def _aggregate_flown_edges(
    schedules: Dict[str, List[Leg]],
) -> Dict[Tuple[str, str], int]:
    counts = {}
    for legs in schedules.values():
        for lg in legs:
            if not lg.feasible:
                continue
            key = (lg.gene.origin, lg.gene.dest)
            counts[key] = counts.get(key, 0) + 1
    return counts


def plot_network(inst: Instance, schedules: Dict[str, List[Leg]] | None = None):
    """
    Desenha a rede de rotas. Se `schedules` for fornecido, destaca as arestas efetivamente voadas
    com maior espessura proporcional ao número de pernas realizadas.
    (Não define cores explicitamente.)
    """
    G = nx.DiGraph()
    for (o, d), r in inst.routes.items():
        G.add_edge(o, d, duration=r.duration_min)

    pos = nx.spring_layout(G, seed=42)

    plt.figure()
    nx.draw(G, pos, with_labels=True, node_size=1200, arrows=True)
    edge_labels = {(u, v): f"{d['duration']}m" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if schedules:
        counts = _aggregate_flown_edges(schedules)
        edgelist, widths = [], []
        for (u, v), c in counts.items():
            if G.has_edge(u, v):
                edgelist.append((u, v))
                widths.append(1.5 + 0.8 * c)
        if edgelist:
            nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=widths, arrows=True)

    plt.title("Rede de Rotas (arestas voadas destacadas)")
    plt.show()


def _fmt_hhmm(m: int) -> str:
    h = (m // 60) % 24
    mi = m % 60
    return f"{h:02d}:{mi:02d}"


def schedules_to_dataframe(schedules: _Dict[str, _List[Leg]]) -> "_pd.DataFrame":
    """
    Converte os 'schedules' em um DataFrame ordenado e amigável:
    colunas: aeronave, origem, destino, dep(desejada/real), chegada(real), atraso(min), factível.
    """
    rows = []
    for ac_id, legs in schedules.items():
        for lg in legs:
            desired = lg.gene.dep_time
            delay = max(0, lg.act_dep - desired)
            rows.append(
                {
                    "Aeronave": ac_id,
                    "Origem": lg.gene.origin,
                    "Destino": lg.gene.dest,
                    "Dep. desejada": _fmt_hhmm(desired),
                    "Dep. real": _fmt_hhmm(lg.act_dep),
                    "Chegada": _fmt_hhmm(lg.act_arr),
                    "Atraso (min)": delay,
                    "Factível": "✓" if lg.feasible else "✗",
                }
            )
    if not rows:
        return _pd.DataFrame(
            columns=[
                "Aeronave",
                "Origem",
                "Destino",
                "Dep. desejada",
                "Dep. real",
                "Chegada",
                "Atraso (min)",
                "Factível",
            ]
        )
    df = _pd.DataFrame(rows)

    # Ordena por aeronave e horário real de partida
    def _to_min(s: str) -> int:
        h, m = map(int, s.split(":"))
        return h * 60 + m

    df["_sort_dep"] = df["Dep. real"].map(_to_min)
    df = (
        df.sort_values(by=["Aeronave", "_sort_dep"])
        .drop(columns=["_sort_dep"])
        .reset_index(drop=True)
    )
    return df
