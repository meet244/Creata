import requests
import json
from flask import Flask, jsonify, request, render_template


app = Flask(__name__)
app.static_folder = "static"
app.static_url_path = "/static"


# @app.before_request
# def check_origin():
#     allowed_origins = ["https://creata.vercel.app",'creata.vercel.app']
#     origin = request.headers.get("Origin")
#     if origin == None : origin = request.headers.get("Host")
#     print(origin)
#     if origin not in allowed_origins:
#         return render_template('allow.html')  # Forbidden

@app.route("/")
def home():
    return render_template("new.html")


@app.route("/save", methods=["POST"])
def save():

    reqUrl = "https://api.craiyon.com/v3"

    headersList = {
        "Accept": "*/*",
        "User-Agent": request.headers.get("User-Agent"),
        "Content-Type": "application/json",
    }

    payload = json.dumps(
        {
            "prompt": "wild peacock in sky",
            "version": "c4ue22fb7kb6wlac",
            "token": None,
            "model": "art",
            "negative_prompt": "",
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
