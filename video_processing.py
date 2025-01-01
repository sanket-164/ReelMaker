import os
import time
import whisper
import streamlit as st
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip
from openai import OpenAI
import torch

from utils.constants import REEL_DIR


# Function to convert video to audio
def video_to_audio(video_file, output_audio_file):
    try:
        progress_text = "Extracting audio..."
        my_bar = st.progress(10, text=progress_text)

        # Load the video file
        video = VideoFileClip(video_file)

        st.session_state["video_duration"] = video.duration

        my_bar.progress(40, text=progress_text)

        # Extract the audio from the video
        audio = video.audio

        my_bar.progress(80, text=progress_text)

        # Write the audio to the output file
        audio.write_audiofile(output_audio_file)

        my_bar.progress(100, text=progress_text)

        my_bar.empty()
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Function to convert audio to text using Whisper
def transcribe_audio(audio_file, output_text_file):
    progress_text = "Transcribing audio..."
    my_bar = st.progress(10, text=progress_text)

    # Check if a GPU is available
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load the model and move it to the GPU
    model = whisper.load_model("base").to(device)

    my_bar.progress(50, text=progress_text)

    # Transcribe the audio file
    print(f"Transcribing {audio_file}...")

    result = model.transcribe(audio_file)

    my_bar.progress(80, text=progress_text)

    extractedText = ""

    for segment in result["segments"]:
        extractedText += f"[{round(segment['start'], 2)} - {round(segment['end'], 2)}] {segment['text']}\n"

    time.sleep(2)
    my_bar.progress(90, text=progress_text)

    save_transcription_to_file(extractedText, output_text_file)

    my_bar.progress(100, text=progress_text)

    time.sleep(1)
    my_bar.empty()

    return extractedText


# Function to save the transcribed text into a file
def save_transcription_to_file(transcribed_text, output_file):
    with open(output_file, "w") as file:
        file.write(transcribed_text)
    print(f"Transcription saved to {output_file}")


# Function to cut video based on start and end time
def cut_video(
    input_video_path,
    output_video_path,
    start_time,
    end_time,
    target_width,
    target_height,
):
    # Load the video file
    with VideoFileClip(input_video_path) as video:

        # Cut the video between start_time and end_time
        progress_text = "Generating reel..."
        my_bar = st.progress(10, text=progress_text)

        video_cut = video.subclip(start_time, end_time)

        my_bar.progress(20, text=progress_text)

        temp_reel_path = os.path.join(REEL_DIR, "temp_reel.mp4")

        # Write the result to the output video file
        video_cut.write_videofile(temp_reel_path, codec="libx264")

        my_bar.progress(40, text=progress_text)

        ###### Changing the resolution of the video ######

        # Get the height and width of original video
        original_width, original_height = video.size

        # Calculate the new height to fit within the target width
        new_height = int((target_width / original_width) * original_height)

        # Resize the video to the new height and width
        clip = VideoFileClip(
            temp_reel_path, target_resolution=(new_height, target_width)
        )

        my_bar.progress(60, text=progress_text)

        # Create a black background with target dimensions
        background = ColorClip(size=(target_width, target_height), color=(0, 0, 0))
        background = background.set_duration(clip.duration)

        # Center the resized clip on the black background (top and bottom padding)
        video = CompositeVideoClip(
            [background, clip.set_position(("center", "center"))]
        )

        my_bar.progress(70, text=progress_text)

        # Write the result to a file
        video.write_videofile(output_video_path, codec="libx264", fps=clip.fps)

        my_bar.progress(100, text=progress_text)
        my_bar.empty()


def analyze_text(audio_file_path):
    progress_text = "Analyzing Video..."
    my_bar = st.progress(10, text=progress_text)

    client = OpenAI()

    # print(client.models.list())

    # Read the entire contents of the file

    file_contents = ""

    if st.session_state["transcribed_text"] is None:
        with open(audio_file_path, "r") as file:
            file_contents = file.read()
    else:
        file_contents = st.session_state["transcribed_text"]

    my_bar.progress(30, text=progress_text)

    analyzeSpeechPrompt = (
        file_contents
        + "\nYou are tasked with identifying the type of video based on its transcript. Analyze the speech content and determine if it fits a category such as educational, tutorial, motivational, news report, cooking, documentary, interview, product review, entertainment, comedy or another genre. Provide a brief classification of the video type and the rationale for your choice based on the content and tone of the speech. Write the explanation in one paragraph."
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": analyzeSpeechPrompt,
            },
        ],
        temperature=0.25,
    )

    my_bar.progress(60, text=progress_text)

    analysisPrompt = (
        file_contents
        + "\n"
        + completion.choices[0].message.content
        + " You are tasked with identifying key moments in a speech that should be highlighted in 25 to 35 seconds of intervals for short video creation. Analyze the speech content, and based on its most engaging parts, provide only the timestamps as intervals in the format [start_time - end_time]. Each interval should last 25 to 35 seconds, contain no speech text, and maximize viewer engagement. Do not include explanations or additional information; list only the intervals."
    )

    print(analysisPrompt)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": analysisPrompt}],
    )

    response = completion.choices[0].message.content

    print(response)

    my_bar.progress(90, text=progress_text)

    lines = response.strip().split("\n")

    # Parse the intervals and convert them to a list of lists
    intervals = []
    for line in lines:
        # Remove the square brackets and split by the dash
        start, end = line.strip().strip("[]").split(" - ")
        intervals.append([float(start), float(end)])

    my_bar.progress(100, text=progress_text)

    time.sleep(1)
    my_bar.empty()

    return intervals
