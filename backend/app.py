from flask import Flask, request, jsonify
from summarize import summarize_text
from universal_extractor import extract_article
from translate import translate_text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    title, content = extract_article(url)
    if not content:
        return jsonify({'error': 'Failed to extract content'}), 500

    translated = translate_text(content)
    summary = summarize_text(translated)

    return jsonify({
        'title': title,
        'summary': summary
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
