import os
import time
import json
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from OpenAiHelper import OpenAiHelper
from CloudAiService import CloudAiService

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
_ = load_dotenv(find_dotenv())

@app.route('/', methods=['GET'])
@cross_origin()
def getwwwroot():
    return 'CNMS AI Service running'

@app.route('/get-square', methods=['POST'])
@cross_origin()
def get_square():
    if not request.json or 'number' not in request.json:
        abort(400)
    num = request.json['number']

    return jsonify({'answer': num ** 2})

@app.route('/get-answer', methods=['POST'])
@cross_origin()
def get_answer():
    if not request.json or 'prompt' not in request.json:
        abort(400)
    prompt = request.json['prompt']

    openaihelper = OpenAiHelper(os.environ["OPENAI_API_KEY"],os.environ["OPENAI_API_ENDPOINT"],os.environ["OPENAI_API_VERSION"])
    service = CloudAiService(openaihelper=openaihelper)
    output = service.askQuestion(prompt)

    output["time"] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(f"log/prompts_{time.strftime('%Y%m%d')}.log", "a+", encoding='utf-8') as myfile:
        json.dump(output, myfile)
        myfile.write("\n")
    
    return jsonify(output)

def create_app():
   return app

