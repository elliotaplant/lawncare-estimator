import os
import tempfile
from flask import Flask, request, send_from_directory
import openai
from queryable_index import QueryableIndex


openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder='public')

# Construct and initialize QueryableIndex
index = QueryableIndex("./saved_index")
index.initialize()


def transcribe_audio(file):
    file_extension = file.filename.rsplit('.', 1)[1]
    print(f"Transcribing {file.filename}")

    # Create a temporary file with the same extension as the uploaded file
    with tempfile.NamedTemporaryFile(suffix="." + file_extension, delete=False) as temp_file:
        temp_file.write(file.read())

    # Transcribe the audio file using the OpenAI Whisper API
    with open(temp_file.name, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)

    # Delete the temporary file
    os.remove(temp_file.name)

    print(f"Transcribed {file.filename}. Length: {len(response['text'])}")
    return response['text']


def create_estimate(prompt):
    print("Creating estimate for prompt:", prompt)

    # Ensure index is initialized
    if not index:
        raise ValueError("QueryableIndex not initialized.")

    # Use the QueryableIndex to process the prompt
    response = index.query(prompt)
    print(response)
    return str(response)


@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        file = request.files['audio_file']
        transcript = transcribe_audio(file)
        return transcript, 200
    except Exception as e:
        return str(e), 500


@app.route('/create-estimate', methods=['POST'])
def estimate():
    try:
        prompt = request.json['prompt']
        estimate = create_estimate(prompt)
        return estimate, 200
    except Exception as e:
        print(e)
        return {'error': str(e)}, 400


@app.route('/pipeline', methods=['POST'])
def pipeline():
    try:
        file = request.files['audio_file']
        transcript = transcribe_audio(file)

        # Put the transcription in the default prompt template
        prompt = (
            'Create a list of materials, labor and other work required '
            'to complete a job for the following transcript:'
            f'\n\n"{transcript}"\n\n'
            'Include calculations for all measurements and hours. '
            'The result will be given to an associate to combine with prices '
            'and create an estimate.'
        )

        # Use the filled template as a prompt to the QueryableIndex query
        estimate = create_estimate(prompt)
        return estimate, 200
    except Exception as e:
        print(e)
        return {'error': str(e)}, 400
