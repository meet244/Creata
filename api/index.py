import requests
import json
import uuid
import threading
from flask import Flask, jsonify, request, render_template, send_file
# from pymongo.mongo_client import MongoClient
# from pymongo import MongoClient
# import gridfs
import time

prompt: str = ""
negative: str = ""
model: str = "art"
token = None
version: str = "35s5hfwn9n78gb06"
counts: int = 1

# from flask_cors import CORS

app = Flask(__name__)
app.static_folder = "static"
app.static_url_path = "/static"
# CORS(app)


# def call(
#     agent="",
#     prompt: str = "",
#     neg="",
#     model="art",
#     token: str = None,
#     version: str = "c4ue22fb7kb6wlac",
#     tri=4,
# ):
#     if tri == 0:
#         return "Sorry Unable to process request"
#     version = "c4ue22fb7kb6wlac"
#     print(prompt)
#     print(neg)
#     print(model)
#     print(token)
#     print(version)
#     print(agent)
#     url = "https://api.craiyon.com/v3"

#     if agent == "":
#         return "no agent"
#     # headers = {
#     #     "accept":'*/*',
#     #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
#     #     "Content-Type": "application/json"
#     # }
#     # headers={
#     #     "accept":'*/*',
#     #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/100.0",
#     #     "Content-Type": "application/json"
#     # }
#     headers = {"accept": "*/*", "User-Agent": agent, "Content-Type": "application/json"}

#     data = {
#         "prompt": prompt,
#         "version": version,
#         "token": token,
#         "model": model,
#         "negative_prompt": neg,
#     }

#     response = None

#     for i in range(tri):
#         response = requests.post(url, headers=headers, data=json.dumps(data))

#         print(response)
#         if response.status_code == 200:
#             print(response.json())
#             # return response.json()
#             # written(response.json())
#             break
#         else:
#             print(response)
#             print("retrying")
#             continue

#     return "failed"


@app.route("/")
def home():
    return render_template("new.html")


@app.route("/save", methods=["POST"])
def save():
    ans = {
        "ids": [
            "aHwvtIG9RqCmjhP4ea8Oag",
            "X3Bo5DqtRS2e3pQTs9piJQ",
            "uYA4jqIGTBif5uxD21-WYQ",
            "6VwjfYTSR7So4_WSQcowrA",
            "InOslRuNRaauvgwIWniTCA",
            "cwZWCwofQh-z5am14wTncA",
            "YzkYw9nbSEqrVzV4y99sqA",
            "kB1GLHjYR-2a3ADcqNPIaA",
            "z9psbvoIQp2GhNufrN9OLw",
        ],
        "images": [
            "2023-10-21/bf30f90339104f69ad3d5ecab0055170c14f3ed1.webp",
            "2023-10-21/c9d4c8805a384c8c86297c1172c83326c14f3ed2.webp",
            "2023-10-21/57d498fa58e845adb53c7cad90e6cca6c14f3ed1.webp",
            "2023-10-21/c1bbd45a33074f9399109326409f64dac14f3ed0.webp",
            "2023-10-21/156841075c8a403cabc4537f62cc3675c14f3ed2.webp",
            "2023-10-21/ec9039ba22eb4426a3f52a1bb5655339c14f3ed3.webp",
            "2023-10-21/42488aec50c045388352f054d6ca9d1ec14f3ed3.webp",
            "2023-10-21/45ae68dfc97841f098b8c4d76e414450c14f3ed1.webp",
            "2023-10-21/1e18e8fd374744ba94c53c0e0f2fdf78c14f3ed0.webp",
        ],
        "next_prompt": "shiny honeybee collecting nectar from a flower",
    }

    return jsonify(ans)

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

    # You can return the response content to the client
    response = requests.post(reqUrl, data=payload, headers=headersList)
    print(response)
    # You can return the response content to the client
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return ""

    # global prompt,version,model,token,negative,counts
    # model = (request.json.get('model', ''))
    # negative = (request.json.get('negative', ''))
    # prompt = (request.json.get('prompt', ''))
    # counts = int(request.json.get('count', 1))
    # for i in (prompt.split('\n')):
    #     if(i!=''):
    # r = call(prompt,negative,tri=10,agent=request.headers.get('User-Agent'))
    # threads = []
    #         for n in range(counts):
    #             thread = threading.Thread(target=call, args=(i,negative,model,token,version))
    #             threads.append(thread)
    #             thread.start()
    # thread = threading.Thread(target=call, args=(request.headers.get('User-Agent'),prompt,negative))
    # threads.append(thread)
    # thread.start()
    # thread.join()
    # return str("r")


@app.route("/upgrade", methods=["POST"])
def upgrade():

    return jsonify({'ids': ["5wkrfJ4eSoCwjcGVlEnOCw"], 'images': ["2023-10-21/86dc167d820a4bb98cba6102c590161a.webp"]})

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
