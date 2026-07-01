document.addEventListener("DOMContentLoaded", () => {
  const flashcardBtn = document.querySelector("#generateFlashcardsBtn");
  const flashcardsContainer = document.querySelector("#flashcardsContainer");
  const videoUrlInput = document.querySelector("#videoUrl");

  const savedUrl = StudyMate.getVideoUrl();

  if (videoUrlInput && savedUrl) {
    videoUrlInput.value = savedUrl;
  }

  if (!flashcardBtn) return;

  flashcardBtn.addEventListener("click", async () => {
    const videoUrl = videoUrlInput?.value.trim() || StudyMate.getVideoUrl();

    if (!videoUrl) {
      StudyMate.showToast("Please enter a YouTube video URL", "error");
      return;
    }

    StudyMate.saveVideoUrl(videoUrl);
    StudyMate.setLoading(flashcardBtn, true, "Creating flashcards...");

    try {
      const data = await StudyMate.postData("/generate-flashcards", {
        video_url: videoUrl
      });

      const cards = data.flashcards || [];

      if (!cards.length) {
        flashcardsContainer.innerHTML = `<p>No flashcards generated.</p>`;
        return;
      }

      flashcardsContainer.innerHTML = cards
        .map(
          (card, index) => `
          <div class="flashcard fade-in" data-index="${index}">
            <div class="flashcard-inner">
              <div class="flashcard-front">
                <h4>Question ${index + 1}</h4>
                <p>${card.question}</p>
              </div>
              <div class="flashcard-back">
                <h4>Answer</h4>
                <p>${card.answer}</p>
              </div>
            </div>
          </div>
        `
        )
        .join("");

      document.querySelectorAll(".flashcard").forEach((card) => {
        card.addEventListener("click", () => {
          card.classList.toggle("flipped");
        });
      });

      StudyMate.showToast("Flashcards created successfully");
    } catch (error) {
      StudyMate.showToast(error.message, "error");
    } finally {
      StudyMate.setLoading(flashcardBtn, false);
    }
  });
});