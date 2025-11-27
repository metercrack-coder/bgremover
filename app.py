from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

session = new_session("u2netp")  # fast model

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        img = Image.open(file.stream)

        output = remove(img, session=session)

        buf = io.BytesIO()
        output.save(buf, format="PNG")
        buf.seek(0)

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)