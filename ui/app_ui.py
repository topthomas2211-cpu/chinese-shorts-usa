import os
import tempfile
import streamlit as st

from config import (
    STYLE_OPTIONS,
    VOICE_OPTIONS,
    MAX_UPLOAD_MB,
)

from services.pipeline import process_video


def render_app():

    st.title("🎬 Chinese → USA Shorts Converter V2")

    st.caption(
        "Local-first Chinese video → American Shorts workflow"
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Chinese video",
        type=["mp4", "mov", "mkv", "webm"],
    )

    if uploaded_file is None:
        st.info("Upload a Chinese video to begin.")
        return

    size_mb = uploaded_file.size / (1024 * 1024)

    if size_mb > MAX_UPLOAD_MB:
        st.error(
            f"File is too large. Maximum: {MAX_UPLOAD_MB} MB."
        )
        return

    st.video(uploaded_file)

    st.subheader("1. Choose narration style")

    style = st.radio(
        "Style",
        options=list(STYLE_OPTIONS.keys()),
        format_func=lambda x: STYLE_OPTIONS[x]["label"],
    )

    st.caption(
        STYLE_OPTIONS[style]["description"]
    )

    st.subheader("2. Choose female voice")

    voice = st.radio(
        "Female voice",
        options=list(VOICE_OPTIONS.keys()),
        format_func=lambda x: VOICE_OPTIONS[x]["label"],
    )

    st.divider()

    if st.button(
        "🚀 Generate USA Short",
        type="primary",
        use_container_width=True,
    ):

        temp_path = None

        try:
            suffix = os.path.splitext(
                uploaded_file.name
            )[1] or ".mp4"

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as tmp:

                tmp.write(
                    uploaded_file.getbuffer()
                )

                temp_path = tmp.name

            with st.status(
                "Processing video...",
                expanded=True,
            ) as status:

                st.write(
                    "🎧 Transcribing Chinese audio locally..."
                )

                result = process_video(
                    temp_path,
                    style,
                    voice,
                )

                status.update(
                    label="✅ Processing complete!",
                    state="complete",
                )

            st.success(
                "Your USA Short is ready."
            )

            st.subheader("Generated script")

            st.write(
                result["script"]
            )

            st.download_button(
                label="⬇️ Download Final MP4",
                data=open(
                    result["output"],
                    "rb"
                ).read(),
                file_name="usa_short.mp4",
                mime="video/mp4",
                use_container_width=True,
            )

        except Exception as exc:
            st.error(
                f"Processing failed: {exc}"
            )

        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
