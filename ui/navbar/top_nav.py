import streamlit as st
from streamlit_option_menu import option_menu

from utils.constants import TOP_NAV_HEADERS, TOP_NAV_ICONS


def top_navbar():
    st.session_state["current_page"] = option_menu(
        menu_title="Video to Reels",
        options=TOP_NAV_HEADERS,
        icons=TOP_NAV_ICONS,
        default_index=TOP_NAV_HEADERS.index(st.session_state["current_page"]),
        orientation="horizontal",
        menu_icon="file-play",
        key="navbar",
    )
