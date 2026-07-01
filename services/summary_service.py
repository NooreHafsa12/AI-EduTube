import re
from collections import Counter

STOPWORDS = set("""
the is are was were a an and or but if then this that to of in on for with as by from it be at
we you they he she i my your our their has have had will would can could should about into
video
""".split())


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.replace("\n", " "))
    return [s.strip() for s in sentences if len(s.strip()) > 30]


def get_keywords(text, limit=15):
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    words = [w for w in words if w not in STOPWORDS]
    return [w for w, count in Counter(words).most_common(limit)]


def generate_summary(transcript, summary_type):
    sentences = split_sentences(transcript)
    keywords = get_keywords(transcript)

    if not sentences:
        return "Not enough transcript text found to generate summary."

    if summary_type == "short":
        return " ".join(sentences[:5])

    if summary_type == "detailed":
        return "\n\n".join(sentences[:12])

    if summary_type == "key concepts":
        return "\n".join(["• " + word.title() for word in keywords])

    return "\n".join(["• " + sentence for sentence in sentences[:10]])