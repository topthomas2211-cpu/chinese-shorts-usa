from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
APP_NAME="Chinese → USA Shorts Converter V2"
MAX_UPLOAD_MB=500
MAX_VIDEO_SECONDS=900
TEMP_DIR=BASE_DIR/"temp"
OUTPUT_DIR=BASE_DIR/"output"
MODELS_DIR=BASE_DIR/"models"
for p in (TEMP_DIR,OUTPUT_DIR,MODELS_DIR): p.mkdir(parents=True,exist_ok=True)

STYLE_OPTIONS={
 "storytelling":{"label":"🎬 Storytelling","description":"Natural American storytelling with a strong hook and satisfying ending."},
 "mystery":{"label":"🔍 Mystery / Curiosity","description":"Curiosity-driven narration with a reveal/payoff near the end."},
 "viral":{"label":"⚡ Fast Viral Explanation","description":"Fast, energetic American Shorts narration focused on retention and payoff."},
}
VOICE_OPTIONS={
 "female_natural":{"label":"👩 Female 1 — Natural Storyteller"},
 "female_energetic":{"label":"👩 Female 2 — Energetic Viral"},
 "female_calm":{"label":"👩 Female 3 — Calm Mystery"},
}
