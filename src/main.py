
from algorithms.pso.pso import ParticlesSwarm
from graph.matrix_graph import MatrixGraph
from io import StringIO
from pathlib import Path
import numpy as np
import streamlit as st


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


st.set_page_config(layout="centered")
st.title('Задача коммивояжера')
n_iter = st.number_input('Количество итераций', min_value=0, value=200)
n_particles = st.number_input('Количество частиц', min_value=0, value=150)

threshold = st.slider('Порог перестановки', 0.0, 1.0, 0.7, 0.01)

neighborhood_size = st.slider(
    'Размер окрестности частицы', 0.0, 1.0, 0.1, 0.01)

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
solve_button = st.button('Найти решение')
if uploaded_file and solve_button:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    lines = stringio.read()

    matrix = get_matrix_from_file(lines.split('\n'))
    graph = MatrixGraph(np.array(matrix))
    pso = ParticlesSwarm(
        graph, n_iter, n_particles, threshold, neighborhood_size)

    pso.execute()
    best_particle = pso.get_best_solution()

    st.write(best_particle.best_solution)
    st.write(best_particle.best_score)
