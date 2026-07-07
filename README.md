# URL Shortener

A lightweight URL shortener built with Python, Flask, and SQLite.

## Features
- Converts long URLs into short, compact codes using base-62 encoding
- Duplicate detection — same URL always returns the same short code
- Input validation — only accepts valid HTTP/HTTPS URLs
- Instant browser redirect when a short link is clicked

## Tech Stack
- Python
- Flask (web framework)
- SQLite (database)

## How to Run
1. Clone the repository
2. Install dependencies: `pip install flask`
3. Run the app: `python app.py`
4. Open your browser and go to `http://127.0.0.1:5000`

## How it Works
1. Paste a long URL into the form and click Shorten
2. The app assigns a unique ID to the URL and converts it to a short code using base-62 encoding
3. Clicking the short link redirects you to the original URL
