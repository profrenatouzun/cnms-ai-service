import os
from flask import Flask, request, abort, jsonify
from openaihelper import OpenAiHelper
from service import ask_question

app = Flask(__name__)


@app.route('/get-square', methods=['POST'])
def get_square():
    if not request.json or 'number' not in request.json:
        abort(400)
    num = request.json['number']

    return jsonify({'answer': num ** 2})

@app.route('/get-answer', methods=['POST'])
def get_answer():
    if not request.json or 'prompt' not in request.json:
        abort(400)
    prompt = request.json['prompt']

    openaihelper = OpenAiHelper(os.environ["OPENAI_API_KEY"],os.environ["OPENAI_API_ENDPOINT"],os.environ["OPENAI_API_VERSION"])
    return jsonify(ask_question(openaihelper, prompt))
