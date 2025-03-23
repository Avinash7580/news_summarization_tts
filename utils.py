import requests
from transformers import pipeline
from gtts import gTTS
from collections import Counter
import os

NEWS_API_KEY = "75dcb0cfb47d4bbd9c8f9925fc8509b3"

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")


def fetch_news(company_name):
    """Fetches 10 latest news articles about a company."""
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 401:
        return "ERROR: Invalid API Key", []
    elif response.status_code != 200:
        return f"ERROR: Failed to fetch news (Status: {response.status_code})", []

    data = response.json()
    articles = data.get("articles", [])[:10]  # Limit to 10 articles
    return None, articles


def summarize_text(text):
    """Summarizes a given text."""
    if not text.strip():
        return "No summary available"
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]


def analyze_sentiment(text):
    """Analyze sentiment of a given text."""
    if not text.strip():
        return "NEUTRAL", 0.50
    result = sentiment_pipeline(text)[0]
    return result['label'], round(result['score'], 2)


def comparative_analysis(sentiments):
    """Analyzes sentiment distribution across articles."""
    sentiment_counts = Counter(sentiments)
    return {
        "sentiment_distribution": dict(sentiment_counts),
        "summary": f"{sentiment_counts.get('POSITIVE', 0)} positive, "
                   f"{sentiment_counts.get('NEGATIVE', 0)} negative, "
                   f"{sentiment_counts.get('NEUTRAL', 0)} neutral articles."
    }


def generate_hindi_tts(text):
    """Generates Hindi Text-to-Speech (TTS) audio."""
    if not text.strip():
        return "No audio available"

    tts = gTTS(text=text, lang="hi", slow=False)
    filename = "summary_audio.mp3"
    tts.save(filename)
    return filename
