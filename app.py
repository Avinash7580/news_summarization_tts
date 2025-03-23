import gradio as gr
from utils import fetch_news, summarize_text, analyze_sentiment, comparative_analysis, generate_hindi_tts

def process_news(company_name):
    """Fetch, summarize, analyze sentiment, and generate Hindi TTS."""
    error, articles = fetch_news(company_name)
    if error:
        return error, "", "", "", "", "", ""

    news_results = []
    sentiments = []

    for article in articles[:2]:  # Process top 2 articles for UI clarity
        title = article.get("title", "No Title")
        summary = summarize_text(title)
        sentiment, score = analyze_sentiment(summary)
        sentiments.append(sentiment)
        news_results.append((title, summary, sentiment, score, article.get("url", "No URL")))

    sentiment_report = comparative_analysis(sentiments)
    tts_file = generate_hindi_tts(news_results[0][1])

    return (news_results[0][1], news_results[0][2], news_results[0][3], tts_file,
            news_results[1][1] if len(news_results) > 1 else "",
            news_results[1][2] if len(news_results) > 1 else "",
            news_results[1][3] if len(news_results) > 1 else "")


# ✅ Define Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# 📰 News Summarization, Sentiment Analysis & TTS")

    company_input = gr.Textbox(label="Enter Company Name")
    summarize_btn = gr.Button("Summarize & Analyze")

    summary_output1 = gr.Textbox(label="Summarized News 1", interactive=False)
    sentiment_label1 = gr.Textbox(label="Sentiment 1", interactive=False)
    sentiment_score1 = gr.Textbox(label="Sentiment Score 1", interactive=False)
    audio_output = gr.Audio(label="Hindi Text-to-Speech", interactive=False)

    summary_output2 = gr.Textbox(label="Summarized News 2 (Comparison)", interactive=False)
    sentiment_label2 = gr.Textbox(label="Sentiment 2 (Comparison)", interactive=False)
    sentiment_score2 = gr.Textbox(label="Sentiment Score 2", interactive=False)

    summarize_btn.click(
        process_news,
        inputs=[company_input],
        outputs=[
            summary_output1, sentiment_label1, sentiment_score1, audio_output,
            summary_output2, sentiment_label2, sentiment_score2
        ]
    )

# ✅ Launch Gradio App
if __name__ == "__main__":
    app.launch()
