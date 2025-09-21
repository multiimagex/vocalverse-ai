from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
from TTS.api import TTS

app = Flask(__name__)
CORS(app)

# =================== DATABASE ===================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

init_db()

# =================== SIGNUP ===================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Signup successful! Please login."})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already registered."})

# =================== LOGIN ===================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password."})

# =================== TTS ===================
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text")
    voice = data.get("voice")

    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    output_path = "output.wav"
    tts.tts_to_file(text=text, file_path=output_path)

    return send_file(output_path, mimetype="audio/wav", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)
