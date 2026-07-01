const StudyMate = {
  qs: (selector) => document.querySelector(selector),
  qsa: (selector) => document.querySelectorAll(selector),

  showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 100);

    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },

  setLoading(button, isLoading, text = "Processing...") {
    if (!button) return;

    if (isLoading) {
      button.dataset.originalText = button.innerHTML;
      button.innerHTML = `<span class="spinner"></span> ${text}`;
      button.disabled = true;
    } else {
      button.innerHTML = button.dataset.originalText || "Submit";
      button.disabled = false;
    }
  },

  saveVideoUrl(url) {
    localStorage.setItem("studymate_video_url", url);
  },

  getVideoUrl() {
    return localStorage.getItem("studymate_video_url") || "";
  },

  clearVideoUrl() {
    localStorage.removeItem("studymate_video_url");
  },

  async postData(url, data) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error("Something went wrong. Please try again.");
    }

    return await response.json();
  }
};