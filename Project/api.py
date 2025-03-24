from flask import Flask, request, jsonify
from utils import scrape_news, perform_sentiment_analysis, generate_tts

app = Flask(__name__)

@app.route('/get_news', methods=['GET'])
def get_news():
    company = request.args.get('company')
    news = scrape_news(company)
    return jsonify(news)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    news_data = request.json
    result = perform_sentiment_analysis(news_data)
    return jsonify(result)

@app.route('/generate_tts', methods=['POST'])
def generate_tts():
    text = request.json.get("text")
    audio = generate_tts(text)
    return audio, 200, {'Content-Type': 'audio/mpeg'}

if __name__ == '__main__':
    app.run(debug=True)
