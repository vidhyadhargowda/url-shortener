import sqlite3
from flask import Flask , redirect , request
def number_to_short_code(num):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_code = ""
    while num > 0:
        short_code = chars[num % 62] + short_code
        num //= 62
    return short_code if short_code else "a"

#print (number_to_short_code(1))  # Example usage
#print (number_to_short_code(100))  # Example usage
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")
   
def create_database():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE urls(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   long_url TEXT NOT NULL,
                   short_code TEXT UNIQUE NOT NULL
                )
            """)
    conn.commit()
    conn.close()

create_database()  # Create the database and table if they don't exist

def shorten_url(long_url):
    if not is_valid_url(long_url):
        return None
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT short_code FROM urls WHERE long_url = ?", (long_url,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return existing[0]
    cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (? , ?)", (long_url, ""))
    new_id = cursor.lastrowid
    short_code = number_to_short_code(new_id)
    cursor.execute("UPDATE urls SET short_code = ? where id = ?" , (short_code , new_id))
    conn.commit()
    conn.close()
    return short_code


#print(shorten_url("https://www.google.com"))  # Example usage

def get_long_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

short = shorten_url("https://anthropic.com")
print(f"Short code: {short}")
print(f"Redirects to: {get_long_url(short)}")
app = Flask(__name__ )
@app.route("/")
def home():
    return """
    <html>
        <body>
            <h1>URL Shortener</h1>
            <form action="/shorten" method="POST">
                <input type="text" name="long_url" placeholder="Enter a URL" size="50">
                <button type="submit">Shorten</button>
            </form>
            </body>
        </html>
        """
@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["long_url"]
    short_code = shorten_url(long_url)
    if short_code:
        short_link = request.host_url + short_code
        return f"<p>Your short link: <a href='{short_link}'>{short_link}</a></p>"
    else:
        return "<p>Invalid URL. Must start with http:// or https://</p>"
   
@app.route("/<short_code>")
def redirect_to_url(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        return redirect(long_url)
    else:
        return "Short code not found", 404
    
if __name__ == "__main__":
    app.run(debug = True)