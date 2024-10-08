from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API endpoints
RANDOM_QUOTE_API = "https://api.quotable.io/random"
AUTHOR_QUOTE_API = "https://api.quotable.io/quotes?author="

# Fetch random quote
def fetch_random_quote():
    try:
        response = requests.get(RANDOM_QUOTE_API, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random quote: {e}")
        return None

# Fetch quotes by author
def fetch_quotes_by_author(author):
    try:
        response = requests.get(f"{AUTHOR_QUOTE_API}{author}", verify=False)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quotes by author: {e}")
        return []

@app.route("/")
def index():
    quote = fetch_random_quote()
    return render_template("index.html", quote=quote)

@app.route("/search", methods=["POST"])
def search():
    author = request.form.get("author")
    quotes = fetch_quotes_by_author(author)
    return render_template("index.html", quotes=quotes, search_author=author)

if __name__ == "__main__":
    app.run(debug=True)
