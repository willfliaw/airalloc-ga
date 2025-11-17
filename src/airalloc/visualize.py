from __future__ import annotations

from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx

from .data import Instance
from .models import Leg


def plot_network(inst: Instance, schedules: Dict[str, List[Leg]]):
    G = nx.DiGraph()
    for (o, d), r in inst.routes.items():
        G.add_edge(o, d, duration=r.duration_min)
    pos = nx.spring_layout(G, seed=42)
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_size=1200, arrows=True)
    edge_labels = {(u, v): f"{d['duration']}m" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Rede de Rotas (ilustrativa)")
    plt.tight_layout()
    plt.show()
