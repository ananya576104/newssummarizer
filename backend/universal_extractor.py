from newspaper import Article
from bs4 import BeautifulSoup
import requests
from langdetect import detect
import re

def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup(['script', 'style', 'footer', 'header', 'nav'])]
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])
    return re.sub(r'\s+', ' ', text).strip()

def extract_article(url):
    try:
        print("📰 Trying newspaper3k...")
        article = Article(url)
        article.download()
        article.parse()
        if len(article.text.strip()) > 100:
            return article.title, article.text
    except Exception as e:
        print(f"⚠️ Newspaper3k failed: {e}")

    try:
        print("🧹 Trying fallback HTML extraction...")
        response = requests.get(url, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string.strip() if soup.title else "Untitled"
        text = clean_html(html)
        return title, text
    except Exception as e:
        print(f"❌ Fallback HTML extraction failed: {e}")
        return None, None

