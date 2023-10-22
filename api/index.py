import requests
import json
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)
app.static_folder = "static"
app.static_url_path = "/static"

@app.route("/")
def home():
    return render_template("new.html")


@app.route("/save", methods=["POST"])
def save():

    prompt = request.json.get("prompt")
    model = request.json.get("model")
    negative = request.json.get("negative")
    
    origin = request.headers.get("Host")
    if origin == "creata.vercel.app":
        return "",400

    reqUrl = "https://api.craiyon.com/v3"

    headersList = {
        "Accept": "*/*",
        "User-Agent": request.headers.get("User-Agent"),
        "Content-Type": "application/json",
    }

    payload = json.dumps(
        {
            "prompt": prompt,
            "version": "c4ue22fb7kb6wlac",
            "token": None,
            "model": model,
            "negative_prompt": negative,
        }
    )

    response = requests.post(reqUrl, data=payload, headers=headersList)

    response = requests.post(reqUrl, data=payload, headers=headersList)
    print(response)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return "",502


@app.route("/upgrade", methods=["POST"])
def upgrade():

    origin = request.headers.get("Host")
    if origin == "creata.vercel.app":
        return "",400

    image_id = request.json.get("image_id", "")
    model = request.json.get("model", "")
    prompt = request.json.get("prompt", "")

    reqUrl = "https://api.craiyon.com/upscale"

    headersList = {
        "Accept": "*/*",
        "User-Agent": request.headers.get("User-Agent"),
        "Content-Type": "application/json",
    }

    payload = json.dumps(
        {
            "image_id": "img.craiyon.com/" + image_id,
            "prompt": prompt,
            "version": "c4ue22fb7kb6wlac",
            "token": None,
            "model": model,
            "negative_prompt": ""
        }
    )

    response = requests.post(reqUrl, data=payload, headers=headersList)

    print(response)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return ""


prompt = "The female bollywood actress's captivating journey led her to a whimsical garden with her beautiful face smiling, bursting with vibrant blooms and delightful creatures. Envision her childlike wonder and genuine happiness, as she discovers a hidden nook and playfully strikes a cute pose, leaving her fans in awe."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
