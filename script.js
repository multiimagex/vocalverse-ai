document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("tts-form");
  const output = document.getElementById("audio-output");
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const profileSection = document.getElementById("profile-section");
  const logoutBtn = document.getElementById("logout-btn");

  // Handle TTS Generation
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = document.getElementById("text-input").value;

      const res = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      if (data.success) {
        output.src = data.audio;
        output.style.display = "block";
        output.play();
      } else {
        alert(data.message);
      }
    });
  }

  // Signup
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("signup-email").value;
      const password = document.getElementById("signup-password").value;

      const res = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      alert(data.message);
      if (data.success) window.location.href = "login.html";
    });
  }

  // Login
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value;
      const password = document.getElementById("login-password").value;

      const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      alert(data.message);
      if (data.success) window.location.href = "profile.html";
    });
  }

  // Profile
  if (profileSection) {
    (async () => {
      const res = await fetch("http://127.0.0.1:5000/profile", {
        method: "GET",
        credentials: "include",
      });
      const data = await res.json();
      if (data.success) {
        document.getElementById("profile-email").innerText = data.email;
        document.getElementById("profile-usage").innerText = data.usage;
      } else {
        alert("Please login first!");
        window.location.href = "login.html";
      }
    })();
  }

  // Logout
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      const res = await fetch("http://127.0.0.1:5000/logout", {
        method: "POST",
        credentials: "include",
      });
      const data = await res.json();
      alert(data.message);
      window.location.href = "login.html";
    });
  }
});
