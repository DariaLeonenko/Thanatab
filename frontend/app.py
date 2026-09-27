<<<<<<< HEAD
=======
import os
import sys

import streamlit as st
<<<<<<< HEAD
# бэк вернись
# Видимость модуля backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
=======

# Добавление корневой директории в sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.database import get_bookmarks
from backend.service import process_bookmark
>>>>>>> 08443d5c09e22c8e5e75fc59c6d597d3af0c2a1a

st.set_page_config(page_title="Thanatab", layout="wide", page_icon= '😀😀')

st.title("Thanatab: Сортировщик вкладок")
st.write("Локальная система классификации инфо-шума и очистки закладок")

# Боковая панель
with st.sidebar:
    st.header("Импорт данных")
    uploaded_file = st.file_uploader(
        "Загрузите HTML-файл закладок из браузера", type=["html", "htm"]
    )

# Форма ввода единичной ссылки
url_input = st.text_input(
    "Проверить один URL-адрес вручную:",
    placeholder="https://example.com",
)

if st.button("Проанализировать и сохранить ссылку", type="primary"):
    if url_input.strip():
        with st.spinner("Загрузка страницы и генерация категории через Ollama..."):
            try:
                result = process_bookmark(url_input)

                if result["status"] == "active":
                    st.success("Страница успешно обработана и сохранена в БД.")
                    st.write(f"**Заголовок:** {result['title']}")
                    st.write(f"**Категория:** {result['category']}")

                    with st.expander("Извлеченный текст"):
                        st.text_area("Текст:", result["text"][:1000], height=150)
                else:
                    st.error("Страница недоступна. Статус сохранен как broken.")
                    if "error" in result:
                        st.caption(f"Ошибка: {result['error']}")

            except Exception as err:
                st.error(f"Сбой выполнения: {err}")
    else:
        st.warning("Введите корректный URL.")

st.divider()

# Вывод данных из SQLite
st.subheader("Сохраненные активные закладки")
records = get_bookmarks(status="active")

if records:
    st.dataframe(
        [
            {
                "ID": r["id"],
                "Название": r["title"],
                "Категория": r["category"],
                "URL": r["url"],
                "Дата": r["date_added"],
            }
            for r in records
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Активные записи в базе данных отсутствуют.")
>>>>>>> main
