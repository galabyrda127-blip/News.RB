from html import escape
from pathlib import Path
import webbrowser

from News import get_news


def create_html(news):
    html_file = Path(__file__).parent / "index.html"

    html = html_file.read_text(encoding="utf-8")

    news_cards = ""

    for number, article in enumerate(news, start=1):
        title = escape(article["title"])
        url = escape(article["url"], quote=True)

        news_cards += f"""
        <article class="news-card">
            <h2>{number}. {title}</h2>

            <div class="news-info">
                БЕЛТА
            </div>

            <a href="{url}" class="read-button" target="_blank" rel="noopener noreferrer">
                Читать новость →
            </a>
        </article>
        """

    start_marker = "<!-- NEWS_START -->"
    end_marker = "<!-- NEWS_END -->"

    start = html.find(start_marker)
    end = html.find(end_marker)

    if start == -1 or end == -1:
        raise RuntimeError(
            "В index.html не найдены специальные метки для новостей."
        )

    new_content = (
        html[:start + len(start_marker)]
        + "\n"
        + news_cards
        + "\n"
        + html[end:]
    )

    html_file.write_text(new_content, encoding="utf-8")

    return html_file


def main():
    try:
        news = get_news(10)

        html_file = create_html(news)

        webbrowser.open(html_file.resolve().as_uri())

        print("Новости успешно загружены!")
        print("Страница открыта в браузере.")

    except RuntimeError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()