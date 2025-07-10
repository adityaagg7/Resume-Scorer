const form = document.getElementById("resumeForm");
const resultArea = document.getElementById("resultArea");
const spinner = document.getElementById("spinner");
const message = document.getElementById("message");

function showSpinner(show) {
  spinner.classList.toggle("hidden", !show);
}

function showMessage(type, text) {
  message.textContent = text;
  message.className = "";
  message.classList.add(type === "error" ? "error" : "success");
  message.classList.add("show");
  message.classList.remove("hidden");

  setTimeout(() => {
    message.classList.add("hidden");
  }, 4000);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultArea.textContent = "";

  const formData = new FormData();
  const fileInput = document.getElementById("resumeFile");

  if (fileInput.files.length > 0) {
    formData.append("resume", fileInput.files[0]);
  }

  if (!formData.has("resume") ) {
    showMessage("error", "Please upload a file!");
    return;
  }

  showSpinner(true);

  try {
    const response = await fetch("https://b32907bddea5.ngrok-free.app/score", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    showSpinner(false);

    if (!response.ok) throw new Error(data.error || "Unknown error");

    resultArea.textContent = JSON.stringify(data, null, 2);
    showMessage("success", "Scored successfully!");
  } catch (err) {
    showSpinner(false);
    resultArea.textContent = "Error: " + err.message;
    showMessage("error", "Failed to score: " + err.message);
  }
});
