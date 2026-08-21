from pathlib import Path
import asyncio
import edge_tts


VOICE_MAP = {
    "female_natural": "en-US-JennyNeural",
    "female_energetic": "en-US-AriaNeural",
    "female_calm": "en-US-SaraNeural",
}


async def _generate(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+5%",
        volume="+0%",
    )
    await communicate.save(output_path)


def generate_voice(
    text: str,
    voice_id: str,
    output_path: str,
) -> str:

    voice = VOICE_MAP.get(
        voice_id,
        VOICE_MAP["female_natural"],
    )

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    asyncio.run(
        _generate(
            text,
            voice,
            output_path,
        )
    )

    return output_path
