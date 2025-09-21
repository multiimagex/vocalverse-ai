document.addEventListener("DOMContentLoaded", () => {
  // =================== TTS SYSTEM ===================
  let freeTrialUsed = localStorage.getItem("freeTrialUsed") || false;

  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", async (e) => {
      if (form.id === "loginForm" || form.id === "signupForm") return; // skip auth forms
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

  // =================== LOGIN ===================
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      try {
        const response = await fetch("http://localhost:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });

        const result = await response.json();
        document.getElementById("loginMessage").innerText = result.message;

        if (result.success) {
          localStorage.setItem("isLoggedIn", true);
          window.location.href = "playground.html";
        }
      } catch (err) {
        console.error("Login error:", err);
      }
    });
  }

  // =================== SIGNUP ===================
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      try {
        const response = await fetch("http://localhost:5000/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, password })
        });

        const result = await response.json();
        document.getElementById("signupMessage").innerText = result.message;

        if (result.success) {
          window.location.href = "login.html";
        }
      } catch (err) {
        console.error("Signup error:", err);
      }
    });
  }
});
