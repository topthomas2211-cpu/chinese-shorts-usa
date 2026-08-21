import subprocess
from pathlib import Path


def run_ffmpeg(args):
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr[-4000:]
        )

    return result


def create_short(
    input_video: str,
    narration_audio: str,
    output_video: str,
):
    """
    Converts source video to 1080x1920 vertical format,
    adds the generated narration and light visual enhancement.
    """

    Path(output_video).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    filter_complex = (
        "[0:v]"
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "eq=contrast=1.04:saturation=1.06:brightness=0.01,"
        "format=yuv420p"
        "[v]"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_video,
        "-i",
        narration_audio,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        output_video,
    ]

    run_ffmpeg(command)

    return output_video
