import streamlit as st
from PIL import Image
import io
import re
import hashlib

from utils.database import create_connection
from utils.validations import name_regex, email_regex, password_regex, mobile_regex


# Streamlit form for user registration
def user_registration_page():
    try:
        st.title(":material/person_edit: Registration")

        with st.form("registration_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            phone_no = st.text_input("Phone Number")
            dob = st.date_input("Date of Birth")
            profession = st.text_input("Profession/Role")
            gender = st.radio("Gender", ("Male", "Female", "Other"))

            profile_picture = st.file_uploader(
                "Profile Picture", type=["png", "jpg", "jpeg"]
            )

            profile_pic_binary = None
            if profile_picture is not None:
                image = Image.open(profile_picture)
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                profile_pic_binary = buffered.getvalue()

                with st.columns([0.2, 0.6, 0.2])[1]:
                    st.image(image, caption="Profile Pic", use_column_width=True)

            if st.form_submit_button(
                label=":material/person_add: Register", type="primary", use_container_width=True
            ):
                if not (
                    name
                    and email
                    and password
                    and phone_no
                    and dob
                    and profession
                    and gender
                    and profile_picture
                ):
                    st.error("Please fill all the fields and upload a profile picture.")
                elif re.match(name_regex, name) is None:
                    st.error("Provide valid name")
                elif re.match(email_regex, email) is None:
                    st.error("Provide valid email address")
                elif re.match(password_regex, password) is None:
                    st.error("Provide strong password")
                elif re.match(mobile_regex, phone_no) is None:
                    st.error("Provide valid mobile number")
                else:
                    conn = create_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                            SELECT * FROM users WHERE email = %s
                        """,
                        (email,),
                    )

                    result = cursor.fetchone()

                    if result is None:

                        hashed_password = hashlib.sha256(password.encode()).hexdigest()

                        cursor.execute(
                            """
                                INSERT INTO users (name, email, password, phone_no, dob, profession, gender, profile_picture)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                name,
                                email,
                                hashed_password,
                                phone_no,
                                dob.strftime("%Y-%m-%d"),
                                profession,
                                gender,
                                profile_pic_binary,
                            ),
                        )

                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.balloons()
                        st.success("User registered successfully")
                    else:
                        st.error("Email already exists")
    except Exception as e:
        st.error(f"Error: {e}")


# user_registration_page()
