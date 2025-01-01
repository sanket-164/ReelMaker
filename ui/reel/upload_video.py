import os
import base64
import yt_dlp
import streamlit as st
from datetime import datetime
from moviepy.editor import VideoFileClip

from video_processing import video_to_audio, transcribe_audio
from utils.constants import UPLOAD_DIR, AUDIO_DIR, TEXT_DIR, REEL_DIR
from utils.database import create_connection


def upload_video_page():
    try:
        # Format the datetime to a string
        unique_file_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directory if it doesn't exist
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(AUDIO_DIR, exist_ok=True)
        os.makedirs(TEXT_DIR, exist_ok=True)
        os.makedirs(REEL_DIR, exist_ok=True)

        # Define different file paths
        uploaded_file_path = os.path.join(UPLOAD_DIR, unique_file_name + ".mp4")
        audio_file_path = os.path.join(AUDIO_DIR, unique_file_name + ".mp3")
        text_file_path = os.path.join(TEXT_DIR, unique_file_name + ".txt")

        # Streamlit app
        st.title("Select Video for Processing")

        # Upload video file
        uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

        video_url = st.text_input(label="Video URL")

        if video_url and (uploaded_file is not None):
            st.error("Either provide Video URL or Choose a video")
        elif video_url or uploaded_file is not None:
            st.session_state["upload_video"] = True
            if video_url:
                my_bar = st.progress(10, "Downloading...")

                ydl_opts = {
                    "format": "bestaudio+bestvideo",
                    "outtmpl": uploaded_file_path,
                    "merge_output_format": "mp4",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    my_bar.progress(30, "Downloading...")

                    info_dict = ydl.extract_info(video_url, download=False)
                    title = info_dict.get("title", "No Title Found")

                    my_bar.progress(70, f"Downloading {title}...")
                    ydl.download([video_url])

                my_bar.progress(100, text=f"Downloading {title}...")
                my_bar.empty()

            elif uploaded_file is not None:

                # Save the uploaded video file
                with open(uploaded_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            if VideoFileClip(uploaded_file_path).duration < 120:
                st.error("Video duration must be greater than 2 minutes.")
            else:
                # Initializing session variables for reel generation
                st.session_state["unique_file_name"] = unique_file_name
                st.session_state["uploaded_file_path"] = uploaded_file_path
                st.session_state["audio_file_path"] = audio_file_path
                st.session_state["text_file_path"] = text_file_path

                # Extracting the audio from video
                video_to_audio(uploaded_file_path, audio_file_path)

                # Transcribing the audio file to text
                st.session_state["transcribed_text"] = transcribe_audio(
                    audio_file_path, text_file_path
                )

        if st.session_state["uploaded_file_path"] is not None:

            # Display the Selected video
            st.text("Selected Video")
            st.video(st.session_state["uploaded_file_path"])

            # Display the extracted audio
            st.text("Extracted audio")
            st.audio(st.session_state["audio_file_path"])

            with open(st.session_state["text_file_path"], "rb") as file:
                # Encode the file content to Base64
                base64_encoded = base64.b64encode(file.read())

                st.text("Transcribed text")
                st.markdown(
                    f"""
                        <a href="data:text/plain;base64,{base64_encoded.decode('utf-8')}" class="button-link" download="{unique_file_name}.txt">
                            <button class="download-button">
                                Download Transcription
                            </button>
                        </a>
                        """,
                    unsafe_allow_html=True,
                )

            conn = create_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO clips (user_id, file_name, no_of_clips, duration)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, file_name) DO NOTHING;
            """,
                (
                    st.session_state["user_id"],
                    st.session_state["unique_file_name"],
                    0,
                    st.session_state["video_duration"],
                ),
            )

            conn.commit()
            cursor.close()
            conn.close()

            st.subheader(
                "Video is processed go to Generate Reel section",
                anchor=False,
            )

    except Exception as e:
        st.error(f"Error: {e}")


# upload_video_page()
