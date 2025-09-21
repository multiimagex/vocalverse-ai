document.addEventListener("DOMContentLoaded", () => {
  let freeTrialUsed = localStorage.getItem("freeTrialUsed") || false;

  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (freeTrialUsed && !localStorage.getItem("isLoggedIn")) {
        document.getElementById("loginPrompt").classList.remove("hidden");
        return;
      }

      const formData = new FormData(form);
      const text = formData.get("text");
      const voice = formData.get("voice") || formData.get("animalVoice");

      try {
        const response = await fetch("http://localhost:5000/tts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, voice })
        });

        const blob = await response.blob();
        const audioURL = URL.createObjectURL(blob);
        document.getElementById("audioPlayer").src = audioURL;

        if (!localStorage.getItem("isLoggedIn")) {
          localStorage.setItem("freeTrialUsed", true);
        }
      } catch (err) {
        console.error("Error generating voice:", err);
      }
    });
  });
});
