import streamlit as st

from utils.session import end_session


@st.dialog("Are you sure you want to logout?")
def logout():

    with st.columns([0.4, 0.3, 0.4])[1]:
        if st.button(
            label=":material/logout: Yes", type="primary", use_container_width=True
        ):
            end_session()
            st.rerun()


def logout_page():
    try:
        with st.columns([0.3, 0.4, 0.3])[1]:
            if st.button(
                label=":material/lock: Logout",
                use_container_width=True,
            ):
                logout()

    except Exception as e:
        st.error(f"Error: {e}")


# logout_page()
