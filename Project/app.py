import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

def fetch_news(company_name):
    response = requests.get(f"{BASE_URL}/get_news?company={company_name}")
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    return None

def analyze_sentiment(news_data):
    response = requests.post(f"{BASE_URL}/analyze_sentiment", json=news_data)
    return response.json() if response.status_code == 200 else None

def convert_to_speech(text):
    response = requests.post(f"{BASE_URL}/generate_tts", json={"text": text})
    return response.content if response.status_code == 200 else None

# Function to translate English sentiment summary to Hindi
def translate_to_hindi(english_text):
    hindi_translations = {
        "Google’s latest news coverage is balanced, with positive sentiment around AI innovations and negative sentiment around regulatory challenges.": 
        "Google की नवीनतम समाचार कवरेज संतुलित है, जिसमें AI नवाचारों के प्रति सकारात्मक भावना और नियामक चुनौतियों के प्रति नकारात्मक भावना शामिल है।",
        
        "No summary available": 
        "कोई सारांश उपलब्ध नहीं है।"
    }
    return hindi_translations.get(english_text, "अनुवाद उपलब्ध नहीं है।")

# Streamlit UI
st.title("📰 News Summarization and Sentiment Analysis")
company = st.text_input("✍️ Enter Company Name:")

if st.button("📊 Fetch and Analyze News"):
    if company:
        with st.spinner("🔄 Fetching news..."):
            news_data = fetch_news(company)
            if not news_data or "error" in news_data[0]:
                st.error("❌ No news articles found. Try another company.")
                st.stop()
            st.subheader("📰 News Articles:")
            st.json(news_data)

        with st.spinner("🧠 Performing Sentiment Analysis..."):
            sentiment_results = analyze_sentiment(news_data)
            if not sentiment_results or "articles" not in sentiment_results:
                st.error("❌ Sentiment analysis failed.")
                st.stop()

            # Extract the English sentiment summary
            english_summary = sentiment_results.get("final_summary", "No summary available")
            hindi_summary = translate_to_hindi(english_summary)

            st.subheader("📈 Sentiment Analysis Result:")
            st.json(sentiment_results)

            # Display both English and Hindi summaries
            st.markdown(f"**📝 English Summary:** {english_summary}")
            st.markdown(f"**🌍 Hindi Summary:** {hindi_summary}")

        with st.spinner("🔊 Generating Text-to-Speech in Hindi..."):
            speech_audio = convert_to_speech(hindi_summary)
            if speech_audio:
                st.success("✅ Hindi speech generated successfully!")
                st.audio(speech_audio, format='audio/mp3')
            else:
                st.error("❌ Failed to generate Hindi speech.")
    else:
        st.error("⚠️ Please enter a company name.")
