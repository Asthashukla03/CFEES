const chatbotBtn = document.getElementById("chatbot-button");
const chatbox = document.getElementById("chatbox");
const chatInput = document.getElementById("chat-input");
const chatBody = document.getElementById("chat-body");

chatbotBtn.addEventListener("click", () => {
  chatbox.style.display = chatbox.style.display === "block" ? "none" : "block";
});

chatInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && chatInput.value.trim() !== "") {
    const userMsg = chatInput.value;
    chatBody.innerHTML += `<p><strong>You:</strong> ${userMsg}</p>`;
    chatInput.value = "";
    setTimeout(() => {
      getBotReply(userMsg);
    }, 600);
  }
});

document.getElementById("send-btn").addEventListener("click", function () {
  if (chatInput.value.trim() !== "") {
    const userMsg = chatInput.value;
    chatBody.innerHTML += `<p><strong>You:</strong> ${userMsg}</p>`;
    chatInput.value = "";
    setTimeout(() => {
      getBotReply(userMsg);
      chatBody.scrollTop = chatBody.scrollHeight;
    }, 600);
  }
});

function getBotReply(message) {
  const loading = document.createElement("p");
  loading.innerHTML = `<strong>Bot:</strong> <span class="loading">Thinking<span class="dots"></span></span>`;
  chatBody.appendChild(loading);

  let dotCount = 0;
  const dotsInterval = setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    loading.querySelector(".dots").textContent = ".".repeat(dotCount);
  }, 500);

  fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: message }),
  })
    .then((res) => res.json())
    .then((data) => {
      clearInterval(dotsInterval);
      loading.remove();
      typeBotResponse(data.response);
    })
    .catch(() => {
      clearInterval(dotsInterval);
      loading.remove();
      chatBody.innerHTML += `<p><strong>Bot:</strong> Oops! Server error.</p>`;
    });
}

function typeBotResponse(text) {
  let i = 0;
  const typing = setInterval(() => {
    if (i < text.length) {
      chatBody.innerHTML += text.charAt(i);
      i++;
    } else {
      clearInterval(typing);
      chatBody.innerHTML += "<br/>";
    }
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 20);
}

document.getElementById("darkToggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});