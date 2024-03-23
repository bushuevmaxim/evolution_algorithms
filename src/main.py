
from algorithms.pso.pso import ParticlesSwarm
from graph.matrix_graph import MatrixGraph
from io import StringIO
from pathlib import Path
import numpy as np
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from time import sleep, time


def get_matrix_from_file(lines):
    matrix = []
    for line in lines:
        row = []
        for number in line.split(' '):
            if len(number) > 0:
                row.append(int(number))
        if len(row) > 0:
            matrix.append(row)
    return matrix


def get_edges(path):
    edges = []

    for i in range(len(path) - 1):
        node = path[i]

        edges.append((path[i], path[i + 1]))
    edges.append((path[-1], path[0]))
    print(edges)

    return edges


def show_solutions(solutions):
    figure, ax = plt.subplots()
    empty = st.empty()
    graph_nx = nx.Graph()

    for solution in solutions:
        epoch = solution[0]
        path = solution[1]
        score = solution[2]
        edges = get_edges(path)

        graph_nx.add_edges_from(edges)
        plt.title(f'Epoch: {epoch} score - {score}')
        nx.draw(graph_nx, with_labels=True, font_weight='bold')

        with empty.container():
            st.pyplot(figure, use_container_width=True, clear_figure=True)

        graph_nx.clear_edges()
        sleep(1)


st.set_page_config(layout="centered")
st.title('Задача коммивояжера')
if 'solution_find' not in st.session_state:
    st.session_state.solution_find = False


n_iter = st.number_input('Количество итераций', min_value=0, value=100)
n_particles = st.number_input('Количество частиц', min_value=0, value=700)
threshold = st.slider('Порог перестановки', 0.0, 1.0, 0.64, 0.01)  # 0.8
neighborhood_size = st.slider(
    'Размер окрестности частицы', 0.0, 1.0, 1.0, 0.01)


uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
solve_button = st.button('Найти решение')

show_solution_best_particle = st.button(
    'Показать решения лучшего решения', disabled=not st.session_state.solution_find)
show_best_solutions = st.button(
    'Показать лучшие решения', disabled=not st.session_state.solution_find)

if not uploaded_file and solve_button:
    st.error('File not found!', icon="🚨")

if uploaded_file and solve_button:
    st.session_state.solution_find = False
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    lines = stringio.read()

    matrix = get_matrix_from_file(lines.split('\n'))
    graph = MatrixGraph(np.array(matrix))
    pso = ParticlesSwarm(
        graph, n_iter, n_particles, threshold, neighborhood_size)
    start = time()
    st.session_state.solution = pso.execute()
    end = time()
    st.session_state.solution_find = True

    st.success(
        f'Алгоритм нашел решение всего за {end - start} секунд со стоимостью {st.session_state.solution[0].best_score}!', icon="✅")
    st.rerun()


if show_solution_best_particle:
    show_solutions(st.session_state.solution[0].solutions)

if show_best_solutions:
    show_solutions(st.session_state.solution[1])
