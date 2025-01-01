import io
import re
import streamlit as st
from PIL import Image

from utils.database import create_connection
from utils.validations import name_regex, email_regex, mobile_regex


def change_profile_page():
    try:

        with st.columns([0.2, 0.6, 0.2])[1]:
            name = st.text_input("Name", value=st.session_state.get("name", ""))
            email = st.text_input("Email", value=st.session_state.get("email", ""))
            phone_no = st.text_input(
                "Phone Number", value=st.session_state.get("phone_no", "")
            )
            dob = st.date_input("Date of Birth", value=st.session_state.get("dob"))
            profession = st.text_input(
                "Profession", value=st.session_state.get("profession", "")
            )
            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=["Male", "Female", "Other"].index(
                    st.session_state.get("gender", "Other")
                ),
            )

            # Update profile picture option
            profile_picture = st.file_uploader(
                "Profile Picture", type=["jpg", "jpeg", "png"]
            )

        with st.columns([0.3, 0.4, 0.3])[1]:
            profile_pic_binary = None
            if profile_picture is not None:
                image = Image.open(profile_picture)
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                profile_pic_binary = buffered.getvalue()

                st.image(image, caption="New Profile Pic", use_column_width=True)
            else:
                profile_pic_binary = st.session_state["profile_picture"]

            # Update session state with form inputs when the "Update Profile" button is clicked
            if st.button(
                label=":material/person_check: Update",
                type="primary",
                use_container_width=True,
            ):
                if re.match(name_regex, name) is None:
                    st.error("Provide valid name")
                elif re.match(email_regex, email) is None:
                    st.error("Provide valid email address")
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

                    if result is None or email == st.session_state["email"]:

                        # Execute the update query
                        cursor.execute(
                            """
                            UPDATE users 
                            SET name = %s, email = %s, phone_no = %s, dob = %s, profession = %s, gender = %s, profile_picture = %s 
                            WHERE id = %s
                        """,
                            (
                                name,
                                email,
                                phone_no,
                                dob.strftime("%Y-%m-%d"),
                                profession,
                                gender,
                                profile_pic_binary,
                                st.session_state["user_id"],
                            ),
                        )

                        # Commit changes and close connection
                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.session_state["name"] = name
                        st.session_state["email"] = email
                        st.session_state["phone_no"] = phone_no
                        st.session_state["dob"] = dob
                        st.session_state["profession"] = profession
                        st.session_state["gender"] = gender
                        if profile_picture is not None:
                            st.session_state["profile_picture"] = profile_pic_binary

                        st.balloons()
                        st.success("Profile updated successfully!")
                    else:
                        st.error("Email already exists")

    except Exception as e:
        st.error(f"Error: {e}")
