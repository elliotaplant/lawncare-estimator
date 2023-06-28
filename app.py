from flask import Flask, request
import openai

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['audio_file']  # May need to get this as a list?
    # assume audio file is in the correct format
    response = openai.Whisper.asr(file.read())
    return response['choices'][0]['transcript'], 200
