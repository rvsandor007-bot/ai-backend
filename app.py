from flask import Flask, request, send_file
import requests
import os
from io import BytesIO

app = Flask(__name__)

API_KEY = os.getenv("STABILITY_API_KEY")

@app.route("/")
def home():
    return "Backend fut 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        image = request.files["image"]

        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/edit/image-to-image",
            headers={
                "Authorization": f"Bearer {API_KEY}",
            },
            files={
                "init_image": ("image.png", image, "image/png"),
            },
            data={
                "prompt": "realistic caricature, keep identity, same face, slightly exaggerated features, natural skin, same background, high detail",
                "negative_prompt": "different person, distorted face, blurry, low quality",
                "strength": 0.3,
                "output_format": "png"
            }
        )

        if response.status_code != 200:
            return {"error": response.text}, 500

        return send_file(
            BytesIO(response.content),
            mimetype="image/png"
        )

    except Exception as e:
        return {"error": str(e)}, 500


app.run(host="0.0.0.0", port=3000)
