import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from openaihelper import OpenAiHelper
from service import ask_question

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

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
    return jsonify(ask_question(openaihelper, prompt))


def create_app():
   return app

