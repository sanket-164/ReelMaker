import streamlit as st
import hashlib
import re

from utils.database import create_connection
from utils.validations import email_regex, password_regex
from utils.constants import TOP_NAV_HEADERS


# Streamlit form for user login
def user_login_page():
    try:
        st.title(":material/passkey: Login")

        # User input form for email and password
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.form_submit_button(label=":material/login: Login", type="primary", use_container_width=True):
                # Validate email and password format
                if re.match(email_regex, email) is None:
                    st.error("Provide valid email")
                elif re.match(password_regex, password) is None:
                    st.error("Provide strong password")
                else:
                    # Establish database connection
                    conn = create_connection()
                    cursor = conn.cursor()

                    # Hash password for secure comparison
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    # Check credentials against the database
                    cursor.execute(
                        """
                                SELECT * FROM users WHERE email = %s AND password = %s
                            """,
                        (email, hashed_password),
                    )

                    user = cursor.fetchone()  # Retrieve user data
                    cursor.close()
                    conn.close()

                    if user:
                        # Store user details in session state upon successful login
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = user[0]
                        st.session_state["name"] = user[1]
                        st.session_state["email"] = user[2]
                        st.session_state["phone_no"] = user[4]
                        st.session_state["dob"] = user[5]
                        st.session_state["profession"] = user[6]
                        st.session_state["gender"] = user[7]
                        st.session_state["profile_picture"] = user[8]
                        st.session_state["show_balloons"] = True

                        st.session_state["current_page"] = TOP_NAV_HEADERS[0]

                        st.rerun()  # Refresh page to reflect logged-in state
                    else:
                        st.error("Wrong email or password")  # Invalid credentials
    except Exception as e:
        st.error(f"Error: {e}")  # Handle unexpected errors


# user_login_page()  # Execute the login page function
