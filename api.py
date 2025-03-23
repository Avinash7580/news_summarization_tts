from flask import Flask, request, jsonify, send_file
from utils import fetch_news, summarize_text, analyze_sentiment, comparative_analysis, generate_hindi_tts

app = Flask(__name__)


@app.route("/")
def home():
    """Welcome message for API."""
    return jsonify({"message": "Welcome to the News Summarization & Sentiment Analysis API!"})


@app.route("/fetch_news", methods=["GET"])
def api_fetch_news():
    """API endpoint to fetch news articles for a given company."""
    company_name = request.args.get("company", default="Tesla", type=str)
    error, articles = fetch_news(company_name)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"company": company_name, "articles": articles})


@app.route("/summarize", methods=["POST"])
def api_summarize():
    """API endpoint to summarize a given text."""
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    summary = summarize_text(data["text"])
    return jsonify({"summary": summary})


@app.route("/analyze_sentiment", methods=["POST"])
def api_analyze_sentiment():
    """API endpoint to analyze sentiment of a given text."""
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    sentiment, confidence = analyze_sentiment(data["text"])
    return jsonify({"sentiment": sentiment, "confidence": confidence})


@app.route("/comparative_analysis", methods=["POST"])
def api_comparative_analysis():
    """API endpoint to analyze sentiment distribution across multiple texts."""
    data = request.json
    if "sentiments" not in data:
        return jsonify({"error": "Missing 'sentiments' in request"}), 400

    sentiment_report = comparative_analysis(data["sentiments"])
    return jsonify(sentiment_report)


@app.route("/generate_tts", methods=["POST"])
def api_generate_tts():
    """API endpoint to generate Hindi text-to-speech (TTS)."""
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    tts_file = generate_hindi_tts(data["text"])
    return send_file(tts_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
