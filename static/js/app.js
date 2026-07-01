document.addEventListener("DOMContentLoaded", () => {
  const videoForm = document.querySelector("#videoForm");
  const videoUrlInput = document.querySelector("#videoUrl");
  const summaryOutput = document.querySelector("#summaryOutput");
  const submitBtn = document.querySelector("#generateSummaryBtn");

  const videoThumbnail = document.querySelector("#videoThumbnail");
  const videoTitle = document.querySelector("#videoTitle");
  const channelName = document.querySelector("#channelName");
  const videoDuration = document.querySelector("#videoDuration");

  const flashcardsContainer = document.querySelector("#flashcardsContainer");
  const flashcardCounter = document.querySelector("#flashcardCounter");
  const prevFlashcardBtn = document.querySelector("#prevFlashcardBtn");
  const nextFlashcardBtn = document.querySelector("#nextFlashcardBtn");

  const quizContainer = document.querySelector("#quizContainer");
  const quizProgressFill = document.querySelector("#quizProgressFill");

  const quickPdfBtn = document.querySelector("#quickPdfBtn");
  const downloadPdfBtn = document.querySelector("#downloadPdfBtn");
  const copySummaryBtn = document.querySelector("#copySummaryBtn");

  let flashcards = [];
  let currentFlashcard = 0;

  let quiz = [];
  let currentQuiz = 0;
  let score = 0;

  let materialReady = false;
  let currentSummaryText = "";

  const savedUrl = StudyMate.getVideoUrl();

  if (videoUrlInput && savedUrl) {
    videoUrlInput.value = savedUrl;
  }

  if (!videoForm) return;

  videoForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const videoUrl = videoUrlInput.value.trim();

    if (!videoUrl) {
      StudyMate.showToast("Please enter a YouTube video URL", "error");
      return;
    }

    StudyMate.saveVideoUrl(videoUrl);
    StudyMate.setLoading(submitBtn, true, "Analyzing video...");

    try {
      const data = await StudyMate.postData("/analyze", {
        video_url: videoUrl
      });

      if (!data.success) {
        materialReady = false;
        StudyMate.showToast(data.error || "Unable to analyze video", "error");
        return;
      }

      materialReady = true;

      renderVideoInfo(data.video_info);
      renderSummary(data.summary);

      flashcards = data.flashcards || [];
      currentFlashcard = 0;
      renderFlashcard();

      quiz = data.quiz || [];
      currentQuiz = 0;
      score = 0;
      renderQuiz();

      StudyMate.showToast("Study material generated successfully", "success");
      document.querySelector("#summarySection")?.scrollIntoView({
       behavior: "smooth",
       block: "start"
});
    } catch (error) {
      materialReady = false;
      StudyMate.showToast(error.message, "error");
    } finally {
      StudyMate.setLoading(submitBtn, false);
    }
  });

  function renderVideoInfo(info) {
    if (!info) return;

    if (videoThumbnail && info.thumbnail) {
      videoThumbnail.innerHTML = `<img src="${info.thumbnail}" alt="Video thumbnail">`;
    }

    if (videoTitle) {
      videoTitle.textContent = info.title || "YouTube Video";
    }

    if (channelName) {
      channelName.textContent = info.channel || "YouTube Channel";
    }

    if (videoDuration) {
      videoDuration.textContent = info.duration || "Duration";
    }
  }

  function renderSummary(summary) {
    if (!summaryOutput) return;

    currentSummaryText = summary || "";

    if (!summary) {
      summaryOutput.innerHTML = `
        <div class="empty-state">
          <h3>No summary generated</h3>
          <p>Please try another video.</p>
        </div>
      `;
      return;
    }

    const points = summary
      .split("\n")
      .filter((line) => line.trim() !== "")
      .map((line) => line.replace(/^[-•*]\s*/, ""));

    summaryOutput.innerHTML = `
      <div class="summary-card">
        <h3>Generated Summary</h3>
        <ul>
          ${points.map((point) => `<li>${point}</li>`).join("")}
        </ul>
      </div>
    `;
  }

  function renderFlashcard() {
    if (!flashcardsContainer) return;

    if (!flashcards.length) {
      flashcardsContainer.innerHTML = `
        <div class="empty-state">
          <h3>No flashcards generated</h3>
          <p>Please try another video.</p>
        </div>
      `;
      if (flashcardCounter) flashcardCounter.textContent = "0 / 0";
      return;
    }

    const card = flashcards[currentFlashcard];

    if (flashcardCounter) {
      flashcardCounter.textContent = `${currentFlashcard + 1} / ${flashcards.length}`;
    }

    flashcardsContainer.innerHTML = `
      <div class="flashcard-view" id="activeFlashcard">
        <div class="flashcard-inner">
          <div class="flashcard-front">
            <h3>Question</h3>
            <p>${card.question || card.front || "Question not available"}</p>
          </div>

          <div class="flashcard-back">
            <h3>Answer</h3>
            <p>${card.answer || card.back || "Answer not available"}</p>
          </div>
        </div>
      </div>
    `;

    const activeCard = document.querySelector("#activeFlashcard");
    activeCard.addEventListener("click", () => {
      activeCard.classList.toggle("flipped");
    });
  }

  if (prevFlashcardBtn) {
    prevFlashcardBtn.addEventListener("click", () => {
      if (!flashcards.length) return;

      currentFlashcard =
        currentFlashcard === 0 ? flashcards.length - 1 : currentFlashcard - 1;

      renderFlashcard();
    });
  }

  if (nextFlashcardBtn) {
    nextFlashcardBtn.addEventListener("click", () => {
      if (!flashcards.length) return;

      currentFlashcard =
        currentFlashcard === flashcards.length - 1 ? 0 : currentFlashcard + 1;

      renderFlashcard();
    });
  }

  function renderQuiz() {
    if (!quizContainer) return;

    if (!quiz.length) {
      quizContainer.innerHTML = `
        <div class="empty-state">
          <h3>No quiz generated</h3>
          <p>Please try another video.</p>
        </div>
      `;
      if (quizProgressFill) quizProgressFill.style.width = "0%";
      return;
    }

    if (currentQuiz >= quiz.length) {
      renderQuizResult();
      return;
    }

    const q = quiz[currentQuiz];
    const progress = ((currentQuiz + 1) / quiz.length) * 100;

    if (quizProgressFill) {
      quizProgressFill.style.width = `${progress}%`;
    }

    quizContainer.innerHTML = `
      <div class="quiz-card-pro">
        <div class="quiz-meta">
          <span>Question ${currentQuiz + 1} / ${quiz.length}</span>
          <span>Score: ${score}</span>
        </div>

        <h3>${q.question}</h3>

        <div class="quiz-options">
          ${(q.options || [])
            .map(
              (option) => `
              <label class="quiz-option-pro">
                <input type="radio" name="quizOption" value="${option}">
                <span>${option}</span>
              </label>
            `
            )
            .join("")}
        </div>

        <div class="quiz-actions">
          <button id="submitAnswerBtn" class="btn-primary" type="button">
            Submit
          </button>
        </div>
      </div>
    `;

    document.querySelector("#submitAnswerBtn").addEventListener("click", () => {
      const selected = document.querySelector("input[name='quizOption']:checked");

      if (!selected) {
        StudyMate.showToast("Please select an option", "error");
        return;
      }

      const correctAnswer = q.answer || q.correct_answer;

      if (selected.value === correctAnswer) {
        score++;
        StudyMate.showToast("Correct ✅", "success");
      } else {
        StudyMate.showToast(`Wrong ❌ Correct: ${correctAnswer}`, "error");
      }

      currentQuiz++;

      setTimeout(() => {
        renderQuiz();
      }, 900);
    });
  }

  function renderQuizResult() {
    const percent = Math.round((score / quiz.length) * 100);

    let message = "Good try!";
    if (percent >= 80) message = "Excellent 🎉";
    else if (percent >= 60) message = "Nice work 👍";

    if (quizProgressFill) {
      quizProgressFill.style.width = "100%";
    }

    quizContainer.innerHTML = `
      <div class="result-card">
        <h3>${message}</h3>
        <p>Your Score</p>
        <h2>${score} / ${quiz.length}</h2>

        <button id="retryQuizBtn" class="btn-primary" type="button">
          Retry Quiz
        </button>
      </div>
    `;

    document.querySelector("#retryQuizBtn").addEventListener("click", () => {
      currentQuiz = 0;
      score = 0;
      renderQuiz();
    });
  }

  function downloadPdf() {
    if (!materialReady) {
      StudyMate.showToast("Please analyze a video first", "error");
      return;
    }

    window.location.href = "/download-pdf";
  }

  if (quickPdfBtn) {
    quickPdfBtn.addEventListener("click", downloadPdf);
  }

  if (downloadPdfBtn) {
    downloadPdfBtn.addEventListener("click", downloadPdf);
  }

  if (copySummaryBtn) {
    copySummaryBtn.addEventListener("click", async () => {
      if (!currentSummaryText) {
        StudyMate.showToast("No summary to copy", "error");
        return;
      }

      try {
        await navigator.clipboard.writeText(currentSummaryText);
        StudyMate.showToast("Summary copied", "success");
      } catch {
        StudyMate.showToast("Unable to copy summary", "error");
      }
    });
  }
});