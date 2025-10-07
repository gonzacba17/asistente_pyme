from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import os

app = Flask(__name__)

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/ocr', methods=['POST'])
def process_ocr():
    """Procesar imagen/PDF con OCR"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    try:
        # Leer imagen
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Aplicar OCR
        text = pytesseract.image_to_string(image, lang='spa')
        
        return jsonify({
            "filename": file.filename,
            "text": text,
            "length": len(text)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)