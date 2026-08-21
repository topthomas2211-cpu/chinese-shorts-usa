from pathlib import Path
import uuid

from config import TEMP_DIR, OUTPUT_DIR
from services.transcription import LocalTranscriber
from services.script_generator import generate_script
from services.tts import generate_voice
from services.video_processor import create_short


def process_video(
    video_path: str,
    style: str,
    voice: str,
):

    job_id = uuid.uuid4().hex

    audio_path = Path(TEMP_DIR) / f"{job_id}_voice.mp3"
    output_path = Path(OUTPUT_DIR) / f"{job_id}_short.mp4"

    try:
        # 1. Chinese video -> local transcription
        transcriber = LocalTranscriber(
            model_size="small",
            device="cpu",
            compute_type="int8",
        )

        transcript = transcriber.transcribe(
            video_path
        )

        if not transcript:
            raise RuntimeError(
                "Could not detect speech in the video."
            )

        # 2. ONE script only
        script = generate_script(
            transcript,
            style,
        )

        # 3. Selected female voice
        generate_voice(
            script,
            voice,
            str(audio_path),
        )

        # 4. FFmpeg rendering
        create_short(
            video_path,
            str(audio_path),
            str(output_path),
        )

        return {
            "transcript": transcript,
            "script": script,
            "output": str(output_path),
        }

    finally:
        # Temporary narration file cleanup
        if audio_path.exists():
            audio_path.unlink(missing_ok=True)
