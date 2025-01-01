import streamlit as st

from utils.css import apply_css
from utils.session import start_session
from utils.database import create_tables
from utils.constants import TOP_NAV_HEADERS, SIDE_NAV_HEADERS

from ui.auth.login import user_login_page
from ui.auth.register import user_registration_page
from ui.auth.forgot_password import forgot_password_page

from ui.home import home_page

from ui.navbar.top_nav import top_navbar
from ui.navbar.side_nav import side_navbar

from ui.user.profile import profile_page

from ui.reel.upload_video import upload_video_page
from ui.reel.generate_reels import reel_generation_page
from ui.reel.saved_reels import saved_reels_page


st.set_page_config(
    page_title="ReelGinx",
    page_icon="data:image/png;base64,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",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)


# Main
def main():
    if "logged_in" not in st.session_state:
        start_session()

    # print(st.session_state["current_page"])

    if st.session_state["show_balloons"]:
        st.balloons()
        st.session_state["show_balloons"] = False

    if st.session_state["logged_in"]:
        st.markdown(
            """
            <style>
                header {
                    height : 0px;
                    width : 0px;
                    margin : 0px;
                    padding : 0px;
                }
                .stMainBlockContainer{
                    padding-top : 0rem;
                    padding-left : 1rem;
                    padding-right : 1rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        top_navbar()

        with st.columns([0.1, 0.8, 0.1])[1]:
            if st.session_state["current_page"] == TOP_NAV_HEADERS[0]:
                with st.container():
                    home_page()
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[1]:
                with st.container():
                    upload_video_page()
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[2]:
                with st.container():
                    reel_generation_page()
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[3]:
                with st.container():
                    saved_reels_page()
            elif st.session_state["current_page"] == TOP_NAV_HEADERS[4]:
                with st.container():
                    profile_page()

    else:
        side_navbar()

        with st.columns([0.2, 0.6, 0.2])[1]:
            if st.session_state["current_page"] == SIDE_NAV_HEADERS[0]:
                user_login_page()
            elif st.session_state["current_page"] == SIDE_NAV_HEADERS[1]:
                user_registration_page()
            elif st.session_state["current_page"] == SIDE_NAV_HEADERS[2]:
                forgot_password_page()


if __name__ == "__main__":
    # Create table if not exists
    create_tables()
    apply_css()
    main()
