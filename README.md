# Books Scraper Flask App

Simple Flask app that scrapes the first page of [Books to Scrape](https://books.toscrape.com/) and displays book titles, prices, stock status, images, and links.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Open http://127.0.0.1:5000.

## CSV Trend Graph

`plot_trend.py` reads a CSV file with `date` and `value` columns and saves a trend graph.

```bash
python3 plot_trend.py
```

The sample CSV is `data/sample_trend.csv`, and the default graph output is `output/trend.svg`.

To use another CSV or output path:

```bash
python3 plot_trend.py --input data/sample_trend.csv --output output/trend.svg
```
