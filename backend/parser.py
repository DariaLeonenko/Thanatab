import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_page_data(url: str) -> dict:
    clean_url = url.strip()

    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url

    try:
        response = requests.get(clean_url, headers=HEADERS, timeout=8)

        if response.status_code >= 400:
            return {
                "url": clean_url,
                "title": "Недоступная страница",
                "text": "",
                "status": "broken",
                "status_code": response.status_code,
            }

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        title = soup.title.get_text(strip=True) if soup.title else "Без названия"

        paragraphs = [
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if p.get_text(strip=True)
        ]
        raw_text = "\n".join(paragraphs)

        if not raw_text:
            raw_text = soup.get_text(separator=" ", strip=True)[:2000]

        return {
            "url": clean_url,
            "title": title,
            "text": raw_text,
            "status": "active",
            "status_code": response.status_code,
        }

    except Exception as e:
        return {
            "url": clean_url,
            "title": "Недоступный сайт",
            "text": "",
            "status": "broken",
            "status_code": None,
            "error": str(e),
        }