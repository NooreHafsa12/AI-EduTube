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
    return [s.strip() for s in sentences if 55 <= len(s.strip()) <= 240]


def extract_keywords(sentence):
    words = re.findall(r"\b[A-Za-z][A-Za-z0-9+#.-]*\b", sentence)
    words = [w for w in words if len(w) > 3 and w.lower() not in STOPWORDS]
    return words[:4]


def shorten(sentence):
    sentence = sentence.strip()
    return sentence if len(sentence) <= 130 else sentence[:127] + "..."


def make_wrong_options(correct, pool):
    wrongs = []

    for item in pool:
        if item != correct and item not in wrongs:
            wrongs.append(shorten(item))

        if len(wrongs) == 3:
            break

    while len(wrongs) < 3:
        wrongs.append("This statement is not the main point explained in the video.")

    return wrongs


def make_question(sentence, index):
    keywords = extract_keywords(sentence)

    if keywords:
        keyword = keywords[0]
        templates = [
            f"Which statement best matches what the video says about {keyword}?",
            f"What is explained about {keyword} in the video?",
            f"Which point is correct according to the video?",
            f"What should you remember from this part of the video?"
        ]
        return templates[index % len(templates)]

    return "Which statement best matches the video content?"


def generate_quiz(transcript):
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

    quiz = []

    for index, sentence in enumerate(selected):
        correct = shorten(sentence)

        pool = selected.copy()
        random.shuffle(pool)

        options = [correct] + make_wrong_options(sentence, pool)
        random.shuffle(options)

        quiz.append({
            "question": make_question(sentence, index),
            "options": options,
            "answer": correct
        })

    if not quiz:
        correct = shorten(transcript[:180])
        quiz.append({
            "question": "What is the video mainly about?",
            "options": [
                correct,
                "A topic unrelated to the video",
                "Only entertainment content",
                "Only personal opinions"
            ],
            "answer": correct
        })

    return quiz