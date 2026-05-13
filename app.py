from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string


app = Flask(__name__)

TARGET_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def scrape_books():
    response = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for item in soup.select("article.product_pod"):
        title_tag = item.select_one("h3 a")
        price_tag = item.select_one(".price_color")
        stock_tag = item.select_one(".availability")
        image_tag = item.select_one("img")

        books.append(
            {
                "title": title_tag.get("title", "").strip(),
                "price": price_tag.get_text(strip=True) if price_tag else "",
                "stock": stock_tag.get_text(" ", strip=True) if stock_tag else "",
                "link": urljoin(TARGET_URL, title_tag.get("href", "")),
                "image": urljoin(TARGET_URL, image_tag.get("src", "")) if image_tag else "",
            }
        )

    return books


@app.route("/")
def index():
    error = None
    books = []

    try:
        books = scrape_books()
    except Exception as exc:
        error = str(exc)

    return render_template_string(
        """
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Books to Scrape 목록</title>
  <style>
    body {
      margin: 0;
      background: #f4f6f8;
      color: #1f2933;
      font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", Arial, sans-serif;
    }
    main {
      max-width: 980px;
      margin: 0 auto;
      padding: 32px 18px 48px;
    }
    h1 {
      margin: 0 0 6px;
      font-size: 28px;
    }
    .source {
      margin: 0 0 24px;
      color: #5f6c7b;
    }
    .source a {
      color: #2563eb;
    }
    .error {
      padding: 14px;
      border: 1px solid #f0b4b4;
      border-radius: 8px;
      background: #fff5f5;
      color: #b42318;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
      gap: 16px;
    }
    .book {
      display: flex;
      flex-direction: column;
      min-height: 100%;
      overflow: hidden;
      border: 1px solid #dde3ea;
      border-radius: 8px;
      background: #fff;
      color: inherit;
      text-decoration: none;
    }
    .book img {
      width: 100%;
      height: 240px;
      object-fit: contain;
      background: #fafafa;
      border-bottom: 1px solid #edf0f3;
    }
    .info {
      display: flex;
      flex: 1;
      flex-direction: column;
      gap: 8px;
      padding: 12px;
    }
    .title {
      margin: 0;
      font-size: 15px;
      line-height: 1.4;
    }
    .price {
      margin-top: auto;
      font-size: 18px;
      font-weight: 800;
    }
    .stock {
      color: #16803c;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <main>
    <h1>Books to Scrape 책 목록</h1>
    <p class="source">
      스크래핑 대상:
      <a href="{{ target_url }}" target="_blank" rel="noreferrer">{{ target_url }}</a>
      · {{ books|length }}개 출력
    </p>

    {% if error %}
      <div class="error">{{ error }}</div>
    {% else %}
      <div class="grid">
        {% for book in books %}
          <a class="book" href="{{ book.link }}" target="_blank" rel="noreferrer">
            <img src="{{ book.image }}" alt="{{ book.title }}">
            <div class="info">
              <p class="title">{{ book.title }}</p>
              <div class="price">{{ book.price }}</div>
              <div class="stock">{{ book.stock }}</div>
            </div>
          </a>
        {% endfor %}
      </div>
    {% endif %}
  </main>
</body>
</html>
        """,
        books=books,
        error=error,
        target_url=TARGET_URL,
    )


if __name__ == "__main__":
    app.run(debug=False, port=5000)
