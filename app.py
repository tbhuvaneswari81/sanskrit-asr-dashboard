import streamlit as st
import whisper
import os
import re

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Sanskrit ASR Evaluation Dashboard",
    layout="wide"
)

st.title("ॐ Sanskrit ASR Evaluation Dashboard")

# -------------------------------------------------
# LOAD WHISPER MODEL
# -------------------------------------------------

@st.cache_resource
def load_model():
    return whisper.load_model("large-v3")


# -------------------------------------------------
# SETTINGS
# -------------------------------------------------

st.sidebar.header("Settings")

data_path = st.sidebar.text_input(
    "Audio/Text Directory Path",
    "./data"
)

# -------------------------------------------------
# FIND AUDIO FILES
# -------------------------------------------------

if not os.path.exists(data_path):

    st.error(f"Directory not found: {data_path}")
    st.stop()

audio_files = [
    f for f in os.listdir(data_path)
    if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))
]

text_files = [
    f for f in os.listdir(data_path)
    if f.lower().endswith(".txt")
]

if not audio_files:

    st.error("No audio files found in the data folder.")
    st.stop()

# -------------------------------------------------
# SELECT AUDIO
# -------------------------------------------------

selected_audio = st.selectbox(
    "Select Audio File",
    audio_files
)

audio_path = os.path.join(
    data_path,
    selected_audio
)

# -------------------------------------------------
# AUDIO SOURCE
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🔊 Audio Source")

    st.audio(audio_path)

    st.write(f"Loaded: `{selected_audio}`")


# -------------------------------------------------
# TRANSCRIPTION
# -------------------------------------------------

with col2:

    st.subheader("ॐ Sanskrit ASR Transcript Output")

    if st.button("🎙️ Transcribe Sanskrit Audio"):

        with st.spinner(
            "Transcribing Sanskrit audio using Whisper large-v3..."
        ):

            try:

                model = load_model()

                result = model.transcribe(
                    audio_path,
                    language="sa",
                    fp16=False
                )

                transcript = result["text"].strip()

                # Remove unwanted HTML tags if present
                transcript = re.sub(
                    r"<[^>]+>",
                    "",
                    transcript
                ).strip()

                if transcript:

                    st.success("Transcription completed!")

                    st.text_area(
                        "Sanskrit Transcript",
                        transcript,
                        height=200
                    )

                    # Character count
                    character_count = len(
                        transcript.replace(" ", "")
                    )

                    # Word count
                    word_count = len(
                        transcript.split()
                    )

                    st.write(
                        f"**Character Count:** {character_count}"
                    )

                    st.write(
                        f"**Word Count:** {word_count}"
                    )

                    # Save transcription
                    output_file = os.path.join(
                        data_path,
                        selected_audio.rsplit(".", 1)[0]
                        + "_transcript.txt"
                    )

                    with open(
                        output_file,
                        "w",
                        encoding="utf-8"
                    ) as f:

                        f.write(transcript)

                    st.success(
                        f"Saved to: {output_file}"
                    )

                else:

                    st.warning(
                        "Whisper returned an empty transcript."
                    )

            except Exception as e:

                st.error(
                    f"Transcription error: {e}"
                )

# -------------------------------------------------
# GROUND TRUTH
# -------------------------------------------------

st.subheader("📝 Ground Truth (Optional Reference)")

reference_file = selected_audio.rsplit(".", 1)[0] + "_ref.txt"

reference_path = os.path.join(
    data_path,
    reference_file
)

if os.path.exists(reference_path):

    with open(
        reference_path,
        "r",
        encoding="utf-8"
    ) as f:

        reference_text = f.read().strip()

    st.text_area(
        "Reference Text",
        reference_text,
        height=150
    )

else:

    st.info(
        f"Tip: Add `{reference_file}` to see accuracy metrics."
    )