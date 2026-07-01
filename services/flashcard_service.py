import re
import random


STOPWORDS = {
    "the", "is", "are", "was", "were", "and", "or", "to", "of", "in", "for",
    "with", "this", "that", "you", "your", "from", "about", "will", "can",
    "have", "has", "they", "their", "there", "what", "when", "how", "why"
}


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if 55 <= len(s.strip()) <= 260]


def extract_keywords(sentence):
    words = re.findall(r"\b[A-Za-z][A-Za-z0-9+#.-]*\b", sentence)
    words = [w for w in words if len(w) > 3 and w.lower() not in STOPWORDS]
    return words[:4]


def make_question(sentence, index):
    keywords = extract_keywords(sentence)

    if keywords:
        main = keywords[0]
        templates = [
            f"What does the video explain about {main}?",
            f"Why is {main} important according to the video?",
            f"What key point is mentioned about {main}?",
            f"How does the video describe {main}?"
        ]
        return templates[index % len(templates)]

    return f"What is the important point explained in this part of the video?"


def generate_flashcards(transcript):
    transcript = clean_text(transcript)
    sentences = split_sentences(transcript)

    selected = []
    seen = set()

    for sentence in sentences:
        key = sentence[:60].lower()
        if key not in seen:
            selected.append(sentence)
            seen.add(key)

        if len(selected) == 10:
            break

    flashcards = []

    for index, sentence in enumerate(selected):
        flashcards.append({
            "question": make_question(sentence, index),
            "answer": sentence
        })

    if not flashcards:
        flashcards.append({
            "question": "What is the main idea explained in the video?",
            "answer": transcript[:350]
        })

    return flashcards