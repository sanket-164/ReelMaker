import os
import math
import base64
import psycopg2
import streamlit as st

from utils.database import create_connection
from utils.constants import UPLOAD_DIR, AUDIO_DIR, TEXT_DIR, REEL_DIR


def download_button(label, file_path, filename):
    with open(file_path, "rb") as file:
        video_bytes = file.read()
        base64_encoded_video = base64.b64encode(video_bytes).decode("utf-8")

    st.markdown(
        f"""
            <a href="data:video/mp4;base64,{base64_encoded_video}" class="button-link" download="{filename}">
                <button class="download-button">
                    {label}
                </button>
            </a>
            """,
        unsafe_allow_html=True,
    )


def saved_reels_page():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM clips WHERE user_id = %s", (st.session_state["user_id"],)
        )
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        if len(records) == 0:
            st.title("You dont have any Reels yet")
        else:
            if st.session_state["view_videos"]:
                btn_label = "View Reels"
            else:
                btn_label = "View Videos"

            with st.columns([0.2, 0.6, 0.2])[1]:
                if st.button(label=btn_label, type="primary", use_container_width=True):
                    st.session_state["view_videos"] = not st.session_state["view_videos"]
                    st.rerun()

            if st.session_state["view_videos"]:

                rows = math.ceil(len(records) / 2)

                cells = []

                for i in range(rows):
                    cells.append(st.columns(2))

                index = 0

                for record in records:
                    video_file_path = os.path.join(UPLOAD_DIR, record[1] + ".mp4")
                    with cells[(index // 2)][index % 2]:

                        st.video(video_file_path)
                        if st.button(
                            label="Use Video", key=record[1], use_container_width=True
                        ):
                            st.session_state["unique_file_name"] = record[1]
                            st.session_state["uploaded_file_path"] = video_file_path
                            st.session_state["audio_file_path"] = os.path.join(
                                AUDIO_DIR, record[1] + ".mp3"
                            )
                            st.session_state["text_file_path"] = os.path.join(
                                TEXT_DIR, record[1] + ".txt"
                            )
                            st.session_state["video_duration"] = record[3]
                            st.toast("Video will be used to generate reel")
                    index = index + 1
            else:
                total_reels = 0
                for record in records:
                    total_reels = total_reels + record[2]

                rows = math.ceil(total_reels / 5)

                cells = []

                for i in range(rows):
                    cells.append(st.columns(5))

                index = 0

                for record in records:

                    user_id, file_name, no_of_reels, video_duration = record

                    for i in range(no_of_reels):

                        reel_name = f"{file_name}_reel_{i + 1}.mp4"
                        reel_path = os.path.join(REEL_DIR, reel_name)

                        with cells[(index // 5)][index % 5]:
                            st.video(reel_path)

                            download_button(
                                label="Download",
                                file_path=reel_path,
                                filename=reel_name,
                            )

                        index = index + 1

    except Exception as e:  
        st.error(f"Error: {e}")
