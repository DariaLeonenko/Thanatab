from backend.database import save_bookmark
from backend.parser import fetch_page_data
from backend.ai_model import classify_text


def process_bookmark(url: str) -> dict:
    result = fetch_page_data(url)

    if result["status"] == "active":
        category = classify_text(result["text"])
    else:
        category = "Без категории"

    bookmark_id = save_bookmark(
        url=result["url"],
        title=result["title"],
        raw_text=result["text"],
        category=category,
        status=result["status"],
    )

    return {
        **result,
        "id": bookmark_id,
        "category": category,
    }