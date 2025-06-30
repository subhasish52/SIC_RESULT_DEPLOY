function addMessage(text, isError = false) {
  const messages = document.getElementById("messages");
  const p = document.createElement("p");
  p.textContent = text;
  if (isError) p.classList.add("error");
  messages.appendChild(p);
  messages.scrollTop = messages.scrollHeight;
}

async function submitSic() {
  const sicInput = document.getElementById("sicInput");
  const sic = sicInput.value.trim().toUpperCase();

  if (sic.length !== 8) {
    addMessage("Error: SIC must be exactly 8 characters.", true);
    return;
  }

  addMessage(`Fetching result for SIC: ${sic}...`);
  sicInput.value = "";

  // Show new circle loader
  document.getElementById("inline-loader").classList.remove("hidden");

  try {
    const response = await fetch("/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sic })
    });

    const data = await response.json();

    if (response.ok) {
      addMessage(data.message);
      const pdfViewer = document.getElementById("pdfViewer");
      pdfViewer.innerHTML = `<embed src="/downloads/${data.pdf}" type="application/pdf">`;
      pdfViewer.classList.add("active");
    } else {
      addMessage(`Error: ${data.error}`, true);
    }
  } catch (error) {
    addMessage(`Error: ${error.message}`, true);
  } finally {
    // Hide circle loader
    document.getElementById("inline-loader").classList.add("hidden");
  }
}

document.getElementById("sicInput").addEventListener("keypress", (e) => {
  if (e.key === "Enter") submitSic();
});
