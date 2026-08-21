from pathlib import Path
from faster_whisper import WhisperModel


class LocalTranscriber:
    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, video_path: str) -> str:
        segments, info = self.model.transcribe(
            str(Path(video_path)),
            beam_size=5,
            vad_filter=True,
        )

        text = " ".join(segment.text.strip() for segment in segments)
        return text.strip()
