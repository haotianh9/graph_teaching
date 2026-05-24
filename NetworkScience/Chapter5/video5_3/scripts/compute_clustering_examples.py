from pathlib import Path

import networkx as nx
import pandas as pd
from networkx.algorithms import approximation as approx


DATA_DIR = Path(__file__).resolve().parents[3] / "Data"


def simple_undirected(graph):
    graph = nx.Graph(graph)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph.remove_nodes_from(list(nx.isolates(graph)))
    return graph


def average_degree(graph):
    return 2 * graph.number_of_edges() / graph.number_of_nodes()


def average_clustering_review_value(graph):
    if graph.number_of_nodes() <= 6000:
        return nx.average_clustering(graph)
    return approx.average_clustering(graph, trials=3000, seed=7)


def load_celegans():
    frame = pd.read_excel(DATA_DIR / "celegans_connectome.xlsx")
    chemical_synapses = frame[frame["Type"] == "S"]
    graph = nx.from_pandas_edgelist(
        chemical_synapses,
        source="Neuron 1",
        target="Neuron 2",
        create_using=nx.DiGraph(),
    )
    return simple_undirected(graph)


def load_facebook():
    return simple_undirected(nx.read_edgelist(DATA_DIR / "facebook_combined.txt", nodetype=int))


def load_collaboration():
    graph = nx.read_gml(DATA_DIR / "cond-mat-2005" / "cond-mat-2005.gml", label="id")
    return simple_undirected(graph)


def main():
    examples = [
        ("C. elegans", load_celegans()),
        ("Facebook", load_facebook()),
        ("Collaboration", load_collaboration()),
    ]

    for name, graph in examples:
        k_mean = average_degree(graph)
        matched_m = max(1, round(k_mean / 2))
        ba_graph = nx.barabasi_albert_graph(graph.number_of_nodes(), matched_m, seed=17)
        c_real = average_clustering_review_value(graph)
        c_ba = average_clustering_review_value(ba_graph)
        print(
            f"{name}: "
            f"N={graph.number_of_nodes()} "
            f"E={graph.number_of_edges()} "
            f"<k>={k_mean:.2f} "
            f"matched_m={matched_m} "
            f"C_real={c_real:.4f} "
            f"C_BA={c_ba:.4f}"
        )


if __name__ == "__main__":
    main()
