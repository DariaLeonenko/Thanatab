import sys
import os
import streamlit as st

# Видимость модуля backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Thanatab", layout="wide", page_icon= '😀😀')

st.title("Thanatab: Сортировщик вкладок")
st.write("Локальная система классификации инфо-шума и очистки закладок")

# Боковая панель
with st.sidebar:
    st.header("Импорт данных")
    uploaded_file = st.file_uploader("Загрузите HTML-файл закладок из браузера", type=["html"])

# Основная рабочая зона
url_input = st.text_input("Проверить один URL-адрес вручную:")
if st.button("Проанализировать ссылку"):
    if url_input:
        with st.spinner("Скачиваем и анализируем страницу..."):
            try:
                from backend.parser import fetch_page_data
                result = fetch_page_data(url_input)
                
                st.success(f"Заголовок страницы: {result['title']}")
                st.info(f"Статус ссылки: {result['status']}")
                
                if result['status'] == 'active':
                    st.text_area("Извлеченный текст (для ИИ):", result['text'][:500])
                else:
                    st.error("Не удалось получить текст. Возможно, ссылка битая или сайт заблокирован.")
            except ImportError:
                st.warning("Модуль парсера (parser.py) еще не готов или содержит ошибки кода.")
    else:
        st.warning("Пожалуйста, введите ссылку для проверки!")
