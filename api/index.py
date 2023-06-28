import requests
import json
import uuid
import threading
from flask import Flask, jsonify, request, render_template, send_file
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
import gridfs

CONNECTION_STRING = "mongodb+srv://meet2005pokar:BUhCWuglqb4tCP4E@cluster0.tnvbure.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(CONNECTION_STRING)


db = client['db']
fs = gridfs.GridFS(db)
d_col = db['data']
u_col = db['upscale']

prompt:str = ""
negative:str=""
model:str="art"
token=None
version:str="35s5hfwn9n78gb06"
counts:int=1

from flask_cors import CORS

app = Flask(__name__)   
CORS(app)


def call(prompt:str="",neg="",model="art",token:str=None,version:str="35s5hfwn9n78gb06"):
    print(prompt)
    print(neg)
    print(model)
    print(token)
    print(version)
    url = "https://api.craiyon.com/v3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "version": version,
        "token": token,
        "model": model,
        "negative_prompt": neg
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response)
    print(response.json())
    append_to_json(response.json()['images'],"data.json",model,prompt,neg)

def append_to_json(data_list,filename,model,prompt,neg):
    global d_col,u_col

    for i in data_list:
        data = {
            'file':i,
            'prompt':prompt,
            'neg':neg,
            'model':model
        }
        if('data' in filename):
            d_col.insert_one(data)
        else:
            u_col.insert_one(data)

        # col.update_one(document_query, {'$set': {'data' if 'data' in filename else 'upscale': [i,model,prompt,neg]}}, upsert=True)

def remove_to_json(data_list,filename):
    global d_col,u_col

    # col.delete_many({'_id': '64995bd76eb506bb6b9cb95f', 'data.0' if 'data' in filename else 'upscale.0': {'$in': data_list}})

    if('data' in filename):
        d_col.delete_many({'file': {'$in': data_list}})
    else:
        u_col.delete_many({'file': {'$in': data_list}})

    # # Read existing data from the JSON file
    # with open(filename, "r") as file:
    #     existing_data = json.loads(file.read())

    # for item in data_list:
    #     for data in existing_data:
    #         if(item == data[0]):
    #             existing_data.remove(data)

    # # Save the updated data back to the file
    # with open(filename, "w") as file:
    #     json.dump(existing_data, file, indent=4)
    #     file.close()

def upgrade(image_id: str = "", prompt: str = "", version: str = "", model: str = "", negative_prompt: str = "",token: str = None):
    print(f"image_id = {image_id}")
    print(f"prompt = {prompt}")
    print(f"version = {version}")
    print(f"token = {token}")
    print(f"model = {model}")
    print(f"negative_prompt = {negative_prompt}")
    url = "https://api.craiyon.com/upscale"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Content-Type": "application/json"
    }

    body = {
        "image_id": "img.craiyon.com/"+image_id,
        "prompt": prompt,
        "version": version,
        "token": token,
        "model": model,
        "negative_prompt": negative_prompt
    }
    response = requests.post(url, json=body, headers=headers)
    print(response.status_code)
    print(response.json())
    append_to_json(response.json()["images"],"upgraded.json",model,prompt,negative_prompt)
    remove_to_json([image_id],"data.json")

@app.route("/upgrade", methods=["POST"])
def toUpgrade():
    global token,version
    image_id = request.json.get('image_id', '')
    print(image_id)
    docs = d_col.find_one({'file': image_id})
    thread = threading.Thread(target=upgrade, args=(image_id, docs['prompt'], version, docs['model'], docs['neg'], token))
    thread.start()
    return "ok"
    # remove_to_json([image_id],"data.json")

key = str(uuid.uuid4())
@app.route("/pass",methods=['POST'])
def password():
    global key
    pas = request.json.get("code","")
    if(pas == "123"):
        return jsonify(key)
    else: return jsonify("")

@app.route("/")
def home():
    global key
    name = request.args.get('code','')
    if (name == key):
        return render_template('new.html')
    else:
        return render_template('pass.html')

@app.route("/upload")
def upload():
    global key
    name = request.args.get('code','')
    if (name == key):
        return render_template('upload.html')
    else:
        return render_template('pass.html')

@app.route("/data")
def data():
    global d_col
    # with open ("data.json") as d:
    #     data = d.read()
    #     d.close()
    # try:
    data = []
    all_docs = d_col.find()
    for doc in all_docs:
        if('model' in doc):
            data.append([doc['file'],doc['model'],doc['prompt'],doc['neg']])
    return jsonify(data)
    # except Exception as e:print(e)
    # Print the data of the 'prompt' field
    # for d in data:
    #     print(d)
    return jsonify(data)

@app.route("/upgraded")
def upgraded():
    global u_col
    # with open ("upgraded.json") as d:
    #     data = d.read()
    #     d.close()
    data = []
    all_docs = u_col.find()
    for doc in all_docs:
        data.append([doc['file'],doc['model'],doc['prompt'],doc['neg']])
    return jsonify(data)

@app.route("/load")
def load():
    global prompt,version,model,token,negative,counts
    return jsonify({'prompt':prompt,"version":version,'model':model,'token':token,'negative':negative,"count":counts})

@app.route("/save", methods=["POST"])
def save():
    global prompt,version,model,token,negative,counts
    model = (request.json.get('model', ''))
    negative = (request.json.get('negative', ''))
    prompt = (request.json.get('prompt', ''))
    counts = int(request.json.get('count', 1))
    for i in (prompt.split('\n')):
        if(i!=''):
            threads = []
            for n in range(counts):
                thread = threading.Thread(target=call, args=(i,negative,model,token,version))
                threads.append(thread)
                thread.start()
    return "ok"

@app.route("/delete", methods=["POST"])
def delete():
    mode = (request.json.get('mode'))
    if(mode == "upscale"):
        # with open("upgraded.json", 'w') as file:
        #     data = []
        #     json.dump(data, file)
        #     file.close()
        u_col.delete_many({})
    elif(mode == "generate"):
        d_col.delete_many({})
        # with open("data.json", 'w') as file:
        #     data = []
        #     json.dump(data, file)
        #     file.close()
    return jsonify("ok")

@app.route('/image/<image_name>')
def retrieve_and_send_image(image_name):
    global db,fs
    collection = db['caption']
    document = collection.find_one({'image_name': image_name})
    if document:
        image_id = document['image_id']
        image = fs.get(image_id)
        return send_file(image, mimetype='image/png')  # Adjust mimetype based on your image type
    else:
        return 'Image not found'

@app.route('/caption',methods=['POST'])
def captions():
    global db
    coll = db['caption']
    data = {}
    all_docs = coll.find({'status':'wait'})
    for doc in all_docs:
        data[doc['image_name']] = doc['caption']
    return jsonify(data)
    
@app.route('/uploadDanger')
def danger():
    global db
    img = request.json.get("image",'')
    coll = db['caption']
    result = coll.update_one({'image_name': img}, {'$set': {'status': 'danger'}})
    if result.modified_count > 0:
        return jsonify('ok')
    else:
        return jsonify({'Image not found'})

@app.route('/uploadRecaption')
def recaptions():
    global db
    img = request.json.get("image",'')
    coll = db['caption']
    result = coll.update_one({'image_name': img}, {'$set': {'status': 'recaption'}})
    if result.modified_count > 0:
        return jsonify('ok')
    else:
        return jsonify({'Image not found'})


@app.route('/uploaddone')
def uploaddone():
    global db
    img = request.json.get("image",'')
    coll = db['caption']
    result = coll.update_one({'image_name': img}, {'$set': {'status': 'done'}})
    if result.modified_count > 0:
        return jsonify('ok')
    else:
        return jsonify({'Image not found'})

prompt = "The female bollywood actress's captivating journey led her to a whimsical garden with her beautiful face smiling, bursting with vibrant blooms and delightful creatures. Envision her childlike wonder and genuine happiness, as she discovers a hidden nook and playfully strikes a cute pose, leaving her fans in awe."

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
