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
    page_title="ReelMaker",
    page_icon="images/ReelMaker_Logo.png",
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
