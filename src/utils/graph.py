
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from time import sleep


def get_edges(path):
    edges = []

    for i in range(len(path) - 1):
        edges.append((path[i], path[i + 1]))
    edges.append((path[-1], path[0]))
    return edges


def show_solutions(solutions):
    figure, _ = plt.subplots()
    empty = st.empty()
    graph_nx = nx.Graph()
    print(solutions)
    for solution in solutions:
        epoch = solution[0]
        path = solution[1]
        score = solution[2]

        edges = get_edges(path)
        print(solution)
        print(edges)
        graph_nx.add_edges_from(edges)
        plt.title(f'Epoch: {epoch} score - {score}')
        nx.draw(graph_nx, with_labels=True, font_weight='bold')
        with empty.container():
            st.pyplot(figure, use_container_width=True, clear_figure=True)

        graph_nx.clear_edges()
        sleep(1)
