import os
import re
from datetime import datetime
from fpdf import FPDF


def clean_text(text):
    text = str(text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    return text.strip()


def create_pdf(video_info, summary, flashcards, quiz):
    os.makedirs("pdfs", exist_ok=True)

    filename = f"study_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join("pdfs", filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_fill_color(124, 92, 252)
    pdf.rect(0, 0, 210, 32, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 16, "AI StudyMate Pro", ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, "Smart YouTube Study Guide", ln=True, align="C")

    pdf.ln(16)

    pdf.set_text_color(20, 30, 50)
    pdf.set_font("Arial", "B", 15)
    pdf.multi_cell(0, 8, clean_text(video_info.get("title", "YouTube Video")))

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(90, 100, 120)
    pdf.cell(0, 8, "Channel: " + clean_text(video_info.get("channel", "Unknown")), ln=True)
    pdf.cell(0, 8, "Duration: " + clean_text(video_info.get("duration", "Unknown")), ln=True)

    pdf.ln(8)

    pdf.set_text_color(20, 30, 50)
    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 10, "Summary", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(45, 55, 75)

    for line in clean_text(summary).split("\n"):
        if line.strip():
            pdf.multi_cell(0, 7, "- " + line.strip())

    pdf.ln(6)

    pdf.set_text_color(20, 30, 50)
    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 10, "Flashcards", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(45, 55, 75)

    for index, card in enumerate(flashcards, 1):
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 7, f"Q{index}. {clean_text(card.get('question', ''))}")

        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, f"Answer: {clean_text(card.get('answer', ''))}")
        pdf.ln(3)

    pdf.ln(5)

    pdf.set_text_color(20, 30, 50)
    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 10, "Quiz", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(45, 55, 75)

    for index, q in enumerate(quiz, 1):
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 7, f"Q{index}. {clean_text(q.get('question', ''))}")

        pdf.set_font("Arial", "", 11)
        for option in q.get("options", []):
            pdf.multi_cell(0, 7, "- " + clean_text(option))

        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 7, "Correct Answer: " + clean_text(q.get("answer", "")))
        pdf.ln(3)

    pdf.output(path)
    return path