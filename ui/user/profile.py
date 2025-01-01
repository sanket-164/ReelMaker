import streamlit as st
import base64

from ui.user.change_profile import change_profile_page
from ui.auth.logout import logout_page


# Helper function to convert image bytes to a base64 string
def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


# Profile page to display user information
def profile_page():
    try:
        btn_label = ""

        if st.session_state["change_profile"]:
            btn_label = ":material/visibility: View Profile"
        else:
            btn_label = ":material/edit: Edit"

        if st.session_state["change_profile"]:
            change_profile_page()

        else:
            # Convert profile picture to base64 if it exists
            profile_picture_base64 = ""
            if (
                "profile_picture" in st.session_state
                and st.session_state["profile_picture"]
            ):
                # Convert memoryview to bytes, then to base64
                profile_picture_base64 = image_to_base64(
                    st.session_state["profile_picture"]
                )

            # Set custom CSS and HTML layout for the profile page
            st.html(
                f"""
                <div class="profile-container">
                    <div class="profile-header">
                        {f'<img src="data:image/png;base64,{profile_picture_base64}" width="150" />' if profile_picture_base64 else ""}
                        <h2 style="margin: 0;">{st.session_state.get("name", "User")}</h2>
                    </div>
                    <div class="profile-details">
                        <p class="detail-label">📧 {st.session_state.get("email", "N/A")} </p>
                        <p class="detail-label">📱 {st.session_state.get("phone_no", "N/A")} </p>
                        <p class="detail-label">🎂 {st.session_state.get("dob", "N/A")} </p>
                        <p class="detail-label">💼 {st.session_state.get("profession", "N/A")} </p>
                        <p class="detail-label">👩‍💼/👨‍💼 {st.session_state.get("gender", "N/A")} </p>
                    </div>
                </div>
                """
            )

        with st.columns([0.3, 0.4, 0.3])[1]:
            if st.button(label=btn_label, type="primary", use_container_width=True):
                st.session_state["change_profile"] = not st.session_state[
                    "change_profile"
                ]
                st.rerun()

        if not st.session_state["change_profile"]:
            logout_page()

    except Exception as e:
        st.error(f"Error: {e}")


# profile_page()
