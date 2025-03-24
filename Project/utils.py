import requests
from textblob import TextBlob
import pyttsx3
import os

def scrape_news(company):
    api_key = "68d65e924b1b042b5ddba980a12ce0ae"  # Replace with your gNews API key
    url = f"https://gnews.io/api/v4/search?q={company}&lang=en&token={api_key}"
    
    response = requests.get(url)
    data = response.json()

    # Debugging output to check API response
    if response.status_code != 200:
        print("Error fetching news:", data)
        return [{"error": f"Failed to fetch news. Response: {data}"}]

    articles = data.get("articles", [])
    if not articles:
        return [{"error": "No articles found"}]

    return [{"title": a.get("title", "No Title"),
             "summary": a.get("description", "No Summary Available"),
             "link": a.get("url", "#")} for a in articles[:10]]

def perform_sentiment_analysis(news_data):
    if not news_data or "error" in news_data[0]:
        return {
            "articles": [],
            "final_summary": "No relevant news found for this company."
        }

    sentiment_results = []
    for article in news_data:
        summary = article.get("summary", "No summary available")
        blob = TextBlob(summary)
        sentiment = "Positive" if blob.sentiment.polarity > 0 else "Negative" if blob.sentiment.polarity < 0 else "Neutral"
        article["sentiment"] = sentiment
        sentiment_results.append(article)
    
    return {
        "articles": sentiment_results,
        "final_summary": "Overall sentiment analysis complete."
    }

def generate_tts(text):
    try:
        engine = pyttsx3.init()
        file_path = "output.mp3"
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        
        if os.path.exists(file_path):
            return open(file_path, "rb").read()
        else:
            print("Error: TTS file not generated")
            return None
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None
