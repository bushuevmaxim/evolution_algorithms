from io import StringIO
from time import time

import numpy as np
import streamlit as st
from algorithms import MachineEvolution
from PIL import Image, ImageOps
from utils import get_matrix_from_file, get_rgb_field, show_field_rgb

st.set_page_config(layout="centered")
st.title('Задача об искусственном муравье')
if 'solution_find' not in st.session_state:
    st.session_state.solution_find = False


n_epochs = st.number_input('Количество эпох', min_value=10, value=40)
n_states = st.number_input('Количество состояний', min_value=10, value=100)
n_cross = st.number_input('Количество скрещиваний', min_value=5, value=5)
n_population = st.number_input('Размер популяции', min_value=20, value=100)
mutation_probability = st.slider(
    'Вероятность мутации', 0.0, 1.0, 0.72, 0.01)
cross_probability = st.slider(
    'Вероятность скрещивания', 0.0, 1.0, 0.6, 0.01)
forward_probability  = st.slider(
    'Вероятность сделать шаг вперед, если чувствует пищу', 0.0, 1.0, 0.9, 0.01)
uploaded_file = st.file_uploader("Upload a text file", type=["txt", "png"])
solve_button = st.button('Найти решение')
 
if not uploaded_file and solve_button:
    st.error('File not found!', icon="🚨")
    
if uploaded_file:
    if uploaded_file.type == "text/plain":
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        lines = stringio.read()
        field = np.array(get_matrix_from_file(lines.split('\n')))
    elif uploaded_file.type == "image/png":
        image = Image.open(uploaded_file)
        
        gray_image = ImageOps.grayscale(image) 

        field = np.where(np.array(gray_image) > 1, 1, 0)
    else:
        st.error("Неверный формат файлв")
    indexes = np.where(field == 1)

    apples = [(i, j) for i, j in  zip(indexes[0], indexes[1])]
    n_apples =len(apples)

    st.text(f"Количество яблок на поле: {n_apples}")
    rgb_field = get_rgb_field(len(field), apples)
    fig =  show_field_rgb(rgb_field)
    st.pyplot(fig)
if uploaded_file and solve_button:
    st.session_state.solution_find = False
    
    algorithm = MachineEvolution(
        field,
        n_apples,
        n_states, n_cross, n_population, mutation_probability, cross_probability, forward_probability)
    
    start = time()
    algorithm.run(n_epochs)
    end = time()

    st.session_state.solution_find = True
    best_machine = algorithm.best_machine
    score, path, _ =  algorithm.get_machine_result(best_machine)
    st.success(
        f'Алгоритм нашел решение всего за {end - start} секунд со стоимостью {score}!', icon="✅")
    rgb_field = get_rgb_field(len(field), apples, path)
    fig =  show_field_rgb(rgb_field)
    st.pyplot(fig)


