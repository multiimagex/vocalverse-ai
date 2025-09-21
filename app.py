from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from TTS.api import TTS

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure random key
CORS(app, supports_credentials=True)

# Mock Database (replace with real DB in production)
users = {}

# Coqui TTS model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")  # Example model

# Free trial limit per user (in memory)
trial_limit = {}


# ---------------- AUTH ROUTES ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return jsonify({"success": False, "message": "User already exists!"}), 400

    users[email] = {
        "password": generate_password_hash(password),
        "usage": 0
    }
    return jsonify({"success": True, "message": "Signup successful! Please login."})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.get(email)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Invalid email or password!"}), 401

    session["user"] = email
    return jsonify({"success": True, "message": "Login successful!", "email": email})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True, "message": "Logged out successfully!"})


# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET"])
def profile():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    email = session["user"]
    user = users[email]
    return jsonify({
        "success": True,
        "email": email,
        "usage": user["usage"]
    })


# ---------------- TTS GENERATION ----------------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("text")

    # Free trial for guest
    if "user" not in session:
        if trial_limit.get("guest", 0) >= 1:
            return jsonify({"success": False, "message": "Free trial over. Please login."}), 403
        trial_limit["guest"] = trial_limit.get("guest", 0) + 1

    else:
        email = session["user"]
        users[email]["usage"] += 1

    output_path = "static/output.wav"
    tts.tts_to_file(text=text, file_path=output_path)

    return jsonify({"success": True, "audio": output_path})


if __name__ == "__main__":
    app.run(debug=True)
