import os
import math
import base64
import streamlit as st

from video_processing import analyze_text, cut_video

from utils.constants import REEL_DIR, RESOLUTIONS_STR, RESOLUTIONS_PIXEL
from utils.database import create_connection


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


def reel_generation_page():
    try:
        # Check uploaded file exist or not
        if st.session_state["uploaded_file_path"] == None:
            st.title("Upload a Video First")
        else:

            # Display the Selected video
            st.text("Selected Video")
            st.video(st.session_state["uploaded_file_path"])

            selectbox_options = ["Resolution"] + RESOLUTIONS_STR

            resolution = st.selectbox(
                label="NOTE: Higher resolutions take longer to load and process.",
                options=selectbox_options,
            )

            if resolution != "Resolution":

                res_width, res_height = RESOLUTIONS_PIXEL[
                    RESOLUTIONS_STR.index(resolution)
                ]

                # Analyze Text to get important intervals for reel generation
                intervals = analyze_text(st.session_state["text_file_path"])

                reel_intervals = []

                for timestamp in intervals:
                    if (
                        (timestamp[1] - timestamp[0] >= 20)
                        and 0 <= timestamp[0]
                        and timestamp[1] <= st.session_state["video_duration"]
                    ):
                        reel_intervals.append([timestamp[0], timestamp[1]])

                total_intervals = len(reel_intervals)

                st.subheader(f"Estimated {total_intervals} Reel of the Video")

                rows = math.ceil(total_intervals / 3)

                cells = []

                for i in range(rows):
                    cells.append(st.columns(3))

                generated_reels = 0
                for index, cut in enumerate(reel_intervals):

                    reel_name = (
                        f"{st.session_state['unique_file_name']}_reel_{index + 1}.mp4"
                    )
                    reel_path = os.path.join(REEL_DIR, reel_name)

                    # Create reel based on the timestamps of intervals
                    cut_video(
                        input_video_path=st.session_state["uploaded_file_path"],
                        output_video_path=reel_path,
                        start_time=cut[0],
                        end_time=cut[1],
                        target_width=res_width,
                        target_height=res_height,
                    )

                    with cells[(index // 3)][index % 3]:
                        # Display generated reel
                        st.video(reel_path)

                        download_button(
                            label="Download",
                            file_path=reel_path,
                            filename=reel_name,
                        )

                    generated_reels = generated_reels + 1

                # Button to generate reels again
                st.button(label="Generate Again", use_container_width=True, icon="✨")

                conn = create_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO clips (user_id, file_name, no_of_clips, duration)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id, file_name)
                    DO UPDATE SET no_of_clips = EXCLUDED.no_of_clips;
                """,
                    (
                        st.session_state["user_id"],
                        st.session_state["unique_file_name"],
                        generated_reels,
                        st.session_state["video_duration"],
                    ),
                )

                conn.commit()
                cursor.close()
                conn.close()

    except Exception as e:
        st.error(f"Error: {e}")


# reel_generation_page()
