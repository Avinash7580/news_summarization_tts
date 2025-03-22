import gradio as gr
from news_scraper import scrape_news


def get_news_sentiment(company_name):
    """Fetch news articles, analyze sentiment, and generate Hindi TTS."""

    articles, sentiment_report, hindi_audio_file = scrape_news(company_name)

    if not articles:
        return "⚠️ No articles found!", {}, "No audio available"

    # Format articles for display
    formatted_articles = [
        f"**📰 {article['title']}**\n📖 {article['summary']}\n🔗 [Read more]({article['url']})\n"
        f"😊 **Sentiment:** {article['sentiment']} (Confidence: {article['confidence']})"
        for article in articles
    ]

    # Create output text
    output_text = "\n\n".join(formatted_articles)

    return output_text, sentiment_report, hindi_audio_file


# Create Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 📰 News Sentiment Analysis App")
    gr.Markdown("Enter a company name to fetch news and analyze sentiment.")

    company_input = gr.Textbox(label="Enter Company Name (e.g., Tesla)")
    submit_button = gr.Button("Analyze News")

    output_text = gr.Markdown(label="News Articles & Sentiment")
    sentiment_chart = gr.JSON(label="Sentiment Distribution")
    audio_output = gr.Audio(label="Hindi Sentiment Summary", type="filepath")

    submit_button.click(get_news_sentiment, inputs=[company_input],
                        outputs=[output_text, sentiment_chart, audio_output])

# Launch Gradio App
if __name__ == "__main__":
    demo.launch(share=True)
