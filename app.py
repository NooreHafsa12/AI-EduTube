from flask import Flask, render_template, request, jsonify, send_file, session
from config import Config

from services.transcript_service import get_transcript
from services.youtube_service import get_video_info
from services.summary_service import generate_summary
from services.flashcard_service import generate_flashcards
from services.quiz_service import generate_quiz
from services.pdf_service import create_pdf
from services.cache_service import save_video_data, get_video_data, clear_video_data

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    video_url = data.get("video_url", "").strip()

    if not video_url:
        return jsonify({"success": False, "error": "Please enter a YouTube URL."})

    transcript, transcript_error = get_transcript(video_url)

    if not transcript:
        return jsonify({"success": False, "error": transcript_error})

    video_info = get_video_info(video_url)

    summary = generate_summary(transcript, "bullet points")
    flashcards = generate_flashcards(transcript)
    quiz = generate_quiz(transcript)

    save_video_data(session, {
        "video_url": video_url,
        "video_info": video_info,
        "transcript": transcript,
        "summary": summary,
        "flashcards": flashcards,
        "quiz": quiz
    })

    return jsonify({
        "success": True,
        "video_info": video_info,
        "summary": summary,
        "flashcards": flashcards,
        "quiz": quiz
    })


@app.route("/summary", methods=["POST"])
def summary():
    data = request.get_json()
    summary_type = data.get("summary_type", "bullet points")

    cached = get_video_data(session)

    if not cached:
        return jsonify({"success": False, "error": "Analyze a video first."})

    result = generate_summary(cached["transcript"], summary_type)
    cached["summary"] = result
    save_video_data(session, cached)

    return jsonify({"success": True, "summary": result})


@app.route("/download-pdf")
def download_pdf():
    cached = get_video_data(session)

    if not cached:
        return "No study material found. Analyze a video first."

    path = create_pdf(
        cached.get("video_info", {}),
        cached.get("summary", ""),
        cached.get("flashcards", []),
        cached.get("quiz", [])
    )

    return send_file(path, as_attachment=True)


@app.route("/clear")
def clear():
    clear_video_data(session)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)