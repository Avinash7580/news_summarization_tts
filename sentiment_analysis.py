from transformers import pipeline

# Load the sentiment analysis model explicitly
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return result['label'], result['score']

# Test the function
sample_text = "Tesla's stock price is rising after a strong earnings report!"
label, score = analyze_sentiment(sample_text)

print(f"Sentiment: {label}, Confidence: {score:.2f}")