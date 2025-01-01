import streamlit as st

from utils.constants import SIDE_NAV_HEADERS

def side_navbar():
    sidebar = st.sidebar

    sidebar.markdown(
        """
        <h1>Start Creating Reels</h1>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar radio button for navigation
    st.session_state['current_page'] = st.sidebar.radio(
        "", SIDE_NAV_HEADERS
    )