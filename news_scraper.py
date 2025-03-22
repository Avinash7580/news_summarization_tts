import requests
from transformers import pipeline
from collections import Counter

# ✅ REPLACE WITH YOUR ACTUAL API KEY
NEWS_API_KEY = "75dcb0cfb47d4bbd9c8f9925fc8509b3"

# ✅ Load Sentiment Analysis Model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")


def analyze_sentiment(text):
    """Analyze sentiment of a given text and return label and confidence score."""
    if not text or text.strip() == "":
        return "NEUTRAL", 0.50  # Default neutral for empty summaries

    result = sentiment_pipeline(text)[0]
    return result['label'], round(result['score'], 2)


def scrape_news(company_name):
    """Fetches 10 latest news articles about a company and analyzes sentiment."""

    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    # ✅ ERROR HANDLING: Check if API key is valid
    if response.status_code == 401:
        print("❌ ERROR: Unauthorized API Key! Check your NewsAPI key.")
        return [], {"sentiment_distribution": {}, "summary": "No sentiment data available."}

    if response.status_code != 200:
        print(f"❌ ERROR: Failed to fetch news (Status: {response.status_code})")
        return [], {"sentiment_distribution": {}, "summary": "No sentiment data available."}

    data = response.json()

    if "articles" not in data or not data["articles"]:
        print("⚠️ No articles found!")
        return [], {"sentiment_distribution": {}, "summary": "No sentiment data available."}

    articles = data["articles"]
    news_list = []
    sentiments = []

    for article in articles[:10]:  # Limit to 10 articles
        title = article.get("title", "No Title")
        summary = article.get("description", "No Summary Available")
        url = article.get("url", "No URL")

        # ✅ Perform Sentiment Analysis on the Summary
        sentiment, confidence = analyze_sentiment(summary)
        sentiments.append(sentiment)

        news_list.append({
            "title": title,
            "summary": summary,
            "url": url,
            "sentiment": sentiment,
            "confidence": confidence
        })

    # ✅ Perform Comparative Sentiment Analysis
    sentiment_report = comparative_analysis(sentiments)

    return news_list, sentiment_report


def comparative_analysis(sentiments):
    """Analyzes sentiment distribution across all articles."""
    sentiment_counts = Counter(sentiments)

    return {
        "sentiment_distribution": dict(sentiment_counts),
        "summary": f"The company has {sentiment_counts.get('POSITIVE', 0)} positive, "
                   f"{sentiment_counts.get('NEGATIVE', 0)} negative, and "
                   f"{sentiment_counts.get('NEUTRAL', 0)} neutral news articles."
    }


# ✅ TESTING: Run script for a company (Example: Tesla)
if __name__ == "__main__":
    company = "Tesla"
    articles, sentiment_report = scrape_news(company)

    if not articles:
        print("⚠️ No articles found!")
    else:
        for article in articles:
            print(f"\n📰 Title: {article['title']}")
            print(f"📖 Summary: {article['summary']}")
            print(f"🔗 URL: {article['url']}")
            print(f"😊 Sentiment: {article['sentiment']} (Confidence: {article['confidence']})\n")

        print("\n📊 Comparative Sentiment Analysis:")
        print(f"🔹 Sentiment Distribution: {sentiment_report['sentiment_distribution']}")
        print(f"📢 Summary: {sentiment_report['summary']}")
