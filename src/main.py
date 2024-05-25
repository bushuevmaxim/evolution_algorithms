
import streamlit as st

MAIN_PAGE_TITLE = "Эволюционные алгоритмы"

st.set_page_config(MAIN_PAGE_TITLE)

st.sidebar.success("Выберите задачу")

st.title('Эволюционные алгоритмы')

st.image('image.png', caption='Artificial ant eats an apple', use_column_width=True)