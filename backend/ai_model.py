import ollama
import re

MODEL_NAME = "gemma:2b"


def classify_text(text: str) -> str:
    clean_text = text.strip()
    if not clean_text:
        return "Без категории"

    short_text = clean_text[:3000]

    prompt = f"""
Проанализируй текст и выведи строго одно или два слова — категорию этой статьи.
Примеры категорий: Программирование, Учеба, Наука, Технологии, Новости, Покупки, Фильмы, Игры, Работа, Здоровье, Развлечения.

Не пиши никаких лишних слов, пояснений и знаков препинания. Только 1-2 слова категории.

Текст статьи:
{short_text}
""".strip()

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1},
        )

        category = response["message"]["content"].strip()
        category = re.sub(r"[^\w\s-]", "", category, flags=re.UNICODE).strip()

        words = category.split()
        if len(words) > 2:
            category = " ".join(words[:2])

        return category.capitalize() if category else "Разное"

    except Exception as e:
        print(f"Ошибка Ollama: {e}")
        return "Разное"