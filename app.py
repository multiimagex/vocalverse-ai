from flask import Flask, request, jsonify, send_file
from TTS.api import TTS
import os
import uuid
from pydub import AudioSegment

app = Flask(__name__)

# 🔹 Create output folder if not exists
OUTPUT_DIR = "outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 🔹 Voice configuration (age group + gender)
VOICES = {
    "child_male": "tts_models/en/vctk/vits",
    "child_female": "tts_models/en/ljspeech/tacotron2-DDC",
    "young_male": "tts_models/en/vctk/vits",
    "young_female": "tts_models/en/ljspeech/tacotron2-DDC",
    "middle_male": "tts_models/en/vctk/vits",
    "middle_female": "tts_models/en/ljspeech/tacotron2-DDC",
    "elderly_male": "tts_models/en/vctk/vits",
    "elderly_female": "tts_models/en/ljspeech/tacotron2-DDC",
}

def chunk_text(text, max_length=500):
    """Split large text into smaller chunks"""
    words = text.split()
    chunks, current = [], []
    count = 0
    for word in words:
        if count + len(word) > max_length:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.append(word)
        count += len(word) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks

@app.route("/api/tts", methods=["POST"])
def generate_tts():
    try:
        data = request.json
        text = data.get("text")
        age = data.get("age")
        gender = data.get("gender")

        if not text or not age or not gender:
            return jsonify({"error": "Missing required parameters"}), 400

        # 🔹 Select model
        voice_key = f"{age.lower()}_{gender.lower()}"
        if voice_key not in VOICES:
            return jsonify({"error": "Invalid voice selection"}), 400

        model_name = VOICES[voice_key]
        tts = TTS(model_name)

        # 🔹 Process chunks
        chunks = chunk_text(text)
        final_audio = None
        for i, chunk in enumerate(chunks):
            temp_file = os.path.join(OUTPUT_DIR, f"temp_{uuid.uuid4()}.wav")
            tts.tts_to_file(text=chunk, file_path=temp_file)

            segment = AudioSegment.from_wav(temp_file)
            final_audio = segment if final_audio is None else final_audio + segment
            os.remove(temp_file)

        # 🔹 Save final audio
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(OUTPUT_DIR, filename)
        final_audio.export(file_path, format="mp3")

        return jsonify({"success": True, "file": f"/download/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
