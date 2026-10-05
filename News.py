import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout
from urllib.parse import urljoin


URL = "https://belta.by/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_news(limit=10):
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

    except Timeout:
        raise RuntimeError("Сайт слишком долго отвечает.")

    except RequestException as error:
        raise RuntimeError(f"Ошибка подключения к сайту: {error}")

    soup = BeautifulSoup(response.text, "lxml")

    articles = []
    links = soup.select('a[href*="/view/"]')

    for link in links:
        title = link.get_text(" ", strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        # Исключаем мировые новости
        if "/world/" in href:
            continue

        url = urljoin(URL, href)

        # Не добавляем одну и ту же новость повторно
        if any(article["url"] == url for article in articles):
            continue

        articles.append({
            "title": title,
            "url": url
        })

        if len(articles) >= limit:
            break

    if not articles:
        raise RuntimeError(
            "Белорусские новости не найдены. "
            "Возможно, структура сайта изменилась."
        )

    return articles