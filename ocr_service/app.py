from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no file"}), 400
    img = Image.open(f.stream).convert("RGB")
    text = pytesseract.image_to_string(img, lang="spa+eng")
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
