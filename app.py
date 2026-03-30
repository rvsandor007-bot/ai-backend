from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def generate_image(image_file, seed, width, height):
    img_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image",
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "init_image": img_base64,
            "prompt": "Transform the uploaded photo into a semi-realistic caricature, preserve identity, slightly exaggerate facial features, realistic skin texture, natural lighting, sharp details",
            "negative_prompt": "different person, distorted face, low quality, unrealistic features",
            "seed": seed,
            "cfg_scale": 8,
            "steps": 40,
            "image_strength": 0.35,
            "width": width,
            "height": height
        }
    )

    return response.json()


@app.route("/preview", methods=["POST"])
def preview():
    image = request.files["image"]
    result = generate_image(image, seed=12345, width=512, height=512)
    return jsonify(result)


@app.route("/highres", methods=["POST"])
def highres():
    image = request.files["image"]
    result = generate_image(image, seed=12345, width=1024, height=1024)
    return jsonify(result)


@app.route("/")
def home():
    return "Backend is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
