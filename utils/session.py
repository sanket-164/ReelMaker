import streamlit as st


def start_session():
    # Initialize session variables related to user authentication and profile management
    st.session_state["logged_in"] = False
    st.session_state["forgot_password"] = False
    st.session_state["user_otp"] = None
    st.session_state["otp_sent"] = False
    st.session_state["otp_verified"] = False

    # Initialize session variables for UI and media content
    st.session_state["show_balloons"] = False
    st.session_state["unique_file_name"] = None
    st.session_state["uploaded_file_path"] = None
    st.session_state["audio_file_path"] = None
    st.session_state["text_file_path"] = None
    st.session_state["transcribed_text"] = None
    st.session_state["video_duration"] = 0

    # Initialize session variables for user profile information
    st.session_state["user_id"] = None
    st.session_state["name"] = None
    st.session_state["email"] = None
    st.session_state["phone_no"] = None
    st.session_state["dob"] = None
    st.session_state["profession"] = None
    st.session_state["gender"] = None
    st.session_state["profile_picture"] = None

    # Initialize session variables for app navigation and user interactions
    st.session_state["view_videos"] = False
    st.session_state["change_profile"] = False

    # Set the default page the user is on when they start the session
    st.session_state["current_page"] = ":material/passkey: Login"


def end_session():
    del st.session_state["logged_in"]
    del st.session_state["forgot_password"]
    del st.session_state["user_otp"]
    del st.session_state["otp_sent"]
    del st.session_state["otp_verified"]
    del st.session_state["show_balloons"]
    del st.session_state["unique_file_name"]
    del st.session_state["uploaded_file_path"]
    del st.session_state["audio_file_path"]
    del st.session_state["text_file_path"]
    del st.session_state["transcribed_text"]
    del st.session_state["video_duration"]
    del st.session_state["user_id"]
    del st.session_state["name"]
    del st.session_state["email"]
    del st.session_state["phone_no"]
    del st.session_state["dob"]
    del st.session_state["profession"]
    del st.session_state["gender"]
    del st.session_state["profile_picture"]
    del st.session_state["view_videos"]
    del st.session_state["change_profile"]
    del st.session_state["current_page"]
