console.log("📣 chatbot.js loaded!");
document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatWindow = document.getElementById("chat-window");

  const quizButton = document.getElementById("generate-quiz");
  const quizInput = document.getElementById("quiz-input");
  const quizOutput = document.getElementById("quiz-output");

  const fileUpload = document.getElementById("file-upload");
  const fileContent = document.getElementById("file-content");

  // Chat form
  if (chatForm) {
    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (!message) return;

      chatWindow.innerHTML += `<div class="mb-2"><strong>You:</strong> ${message}</div>`;
      chatInput.value = "";

      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer YOUR_OPENAI_KEY_HERE`
        },
        body: JSON.stringify({
          model: "gpt-3.5-turbo",
          messages: [{ role: "user", content: message }]
        })
      });

      const data = await response.json();
      const reply = data.choices?.[0]?.message?.content || "Sorry, no reply.";
      chatWindow.innerHTML += `<div class="mb-2"><strong>Bot:</strong> ${reply}</div>`;
      chatWindow.scrollTop = chatWindow.scrollHeight;
    });
  }

  // Quiz button
  if (quizButton) {
    quizButton.addEventListener("click", async () => {
      const text = quizInput.value.trim();
      if (!text) return;

      const response = await fetch("/generate-quiz", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ text })
      });

      const data = await response.json();
      quizOutput.innerText = data.quiz;
    });
  }

  // File upload
  if (fileUpload) {
    fileUpload.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/upload-file", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      fileContent.innerText = data.content;
    });
  }
});
