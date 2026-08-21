import re


STYLE_INSTRUCTIONS = {
    "storytelling": """
Write natural American-English Shorts narration.
Start with a strong hook.
Use simple spoken English.
Build the story clearly.
End with a satisfying payoff.
""",
    "mystery": """
Write natural American-English Shorts narration.
Create curiosity immediately.
Reveal information gradually.
Keep tension throughout.
End with a strong reveal or payoff.
""",
    "viral": """
Write fast, energetic American-English Shorts narration.
Use short spoken sentences.
Start with an attention-grabbing hook.
Remove unnecessary details.
Keep the pacing suitable for YouTube Shorts.
""",
}


def clean_script(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"^```.*?```$", "", text, flags=re.S)
    return text.strip()


def generate_script(transcript: str, style: str) -> str:
    """
    Temporary local script generator.

    This version does not require an API key.
    Gemini integration can be plugged into this same interface later.
    """

    if not transcript.strip():
        raise ValueError("No transcript was produced.")

    instruction = STYLE_INSTRUCTIONS.get(style, STYLE_INSTRUCTIONS["viral"])

    sentences = re.split(r"(?<=[.!?。！？])\s*", transcript)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return transcript.strip()

    # Keep the script short enough for Shorts.
    selected = sentences[:12]

    opening = {
        "storytelling": "Here's what happened.",
        "mystery": "But here's the part nobody expected.",
        "viral": "You won't believe what happened next.",
    }.get(style, "Here's what happened.")

    body = " ".join(selected)

    return clean_script(
        f"{opening} {instruction.strip()} {body}"
    )
