document.addEventListener("DOMContentLoaded", () => {
  const quizBtn = document.querySelector("#generateQuizBtn");
  const quizContainer = document.querySelector("#quizContainer");
  const submitQuizBtn = document.querySelector("#submitQuizBtn");
  const resultBox = document.querySelector("#quizResult");
  const videoUrlInput = document.querySelector("#videoUrl");

  let quizData = [];

  const savedUrl = StudyMate.getVideoUrl();

  if (videoUrlInput && savedUrl) {
    videoUrlInput.value = savedUrl;
  }

  if (!quizBtn) return;

  quizBtn.addEventListener("click", async () => {
    const videoUrl = videoUrlInput?.value.trim() || StudyMate.getVideoUrl();

    if (!videoUrl) {
      StudyMate.showToast("Please enter a YouTube video URL", "error");
      return;
    }

    StudyMate.saveVideoUrl(videoUrl);
    StudyMate.setLoading(quizBtn, true, "Generating quiz...");

    try {
      const data = await StudyMate.postData("/generate-quiz", {
        video_url: videoUrl
      });

      quizData = data.quiz || [];

      if (!quizData.length) {
        quizContainer.innerHTML = `<p>No quiz questions generated.</p>`;
        return;
      }

      quizContainer.innerHTML = quizData
        .map(
          (q, index) => `
          <div class="quiz-card fade-in">
            <h4>Q${index + 1}. ${q.question}</h4>

            ${q.options
              .map(
                (option) => `
                <label class="quiz-option">
                  <input 
                    type="radio" 
                    name="question-${index}" 
                    value="${option}"
                  />
                  <span>${option}</span>
                </label>
              `
              )
              .join("")}
          </div>
        `
        )
        .join("");

      if (submitQuizBtn) {
        submitQuizBtn.style.display = "inline-flex";
      }

      if (resultBox) {
        resultBox.innerHTML = "";
      }

      StudyMate.showToast("Quiz generated successfully");
    } catch (error) {
      StudyMate.showToast(error.message, "error");
    } finally {
      StudyMate.setLoading(quizBtn, false);
    }
  });

  if (submitQuizBtn) {
    submitQuizBtn.addEventListener("click", () => {
      let score = 0;

      quizData.forEach((q, index) => {
        const selected = document.querySelector(
          `input[name="question-${index}"]:checked`
        );

        if (selected && selected.value === q.answer) {
          score++;
        }
      });

      resultBox.innerHTML = `
        <div class="result-card fade-in">
          <h3>Your Score</h3>
          <p>${score} / ${quizData.length}</p>
        </div>
      `;

      StudyMate.showToast("Quiz submitted");
    });
  }
});