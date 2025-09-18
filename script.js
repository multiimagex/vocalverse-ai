document.getElementById("generateBtn").addEventListener("click", async () => {
  const text = document.getElementById("ttsText").value.trim();
  const voice = document.getElementById("voiceSelect").value;
  const audioPlayer = document.getElementById("audioPlayer");

  if (!text) {
    alert("Please enter some text!");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, voice })
    });

    if (!response.ok) throw new Error("TTS request failed");

    const blob = await response.blob();
    const audioURL = URL.createObjectURL(blob);
    audioPlayer.src = audioURL;
    audioPlayer.play();
  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong. Check if Flask server is running.");
  }
});
