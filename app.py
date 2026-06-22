from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Languages mapping matching original app options
indian_langs = {
    "Hindi": "hi", "Marathi": "mr", "Bengali": "bn", "Gujarati": "gu",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Malayalam": "ml",
    "Punjabi": "pa", "Urdu": "ur", "English": "en"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request data"}), 400
            
        text = data.get('text', '').strip()
        src_lang_name = data.get('src_lang', 'English')
        dest_lang_name = data.get('dest_lang', 'Hindi')
        
        if not text:
            return jsonify({"error": "Text to translate is empty"}), 400
            
        src_code = indian_langs.get(src_lang_name)
        dest_code = indian_langs.get(dest_lang_name)
        
        if not src_code or not dest_code:
            return jsonify({"error": f"Invalid languages specified: {src_lang_name} to {dest_lang_name}"}), 400
            
        # Perform translation using deep_translator
        translated = GoogleTranslator(source=src_code, target=dest_code).translate(text)
        return jsonify({"translated_text": translated})
        
    except Exception as e:
        app.logger.error(f"Translation backend exception: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) so it's accessible within the local network and tunnel
    app.run(host='0.0.0.0', port=5000, debug=True)
