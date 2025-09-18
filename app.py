from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
from TTS.api import TTS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (frontend <-> backend)

# Load Coqui TTS model (CPU pe chalega, agar GPU hai to fast hoga)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

@app.route("/tts", methods=["POST"])
def tts_endpoint():
    try:
        data = request.json
        text = data.get("text", "").strip()
        voice = data.get("voice", "male_en")

        if not text:
            return {"error": "No text provided"}, 400

        # Temporary audio file generate karna
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tts.tts_to_file(text=text, file_path=tmpfile.name)
            return send_file(tmpfile.name, mimetype="audio/wav")

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    # Flask server run karega localhost pe port 5000 par
    app.run(host="127.0.0.1", port=5000)
