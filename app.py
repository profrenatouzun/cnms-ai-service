from flask import Flask, request, abort, jsonify

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
    prompy = request.json['prompt']

    return jsonify({'prompt': prompt})
