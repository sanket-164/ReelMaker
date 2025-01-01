import re
import os
import random
import smtplib
import hashlib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utils.database import create_connection
from utils.validations import email_regex, password_regex


# Function to check if the email exists in the database
def email_exists_in_db(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is None


# Function to send an email
def send_email(to_email, subject, otp):
    # Define the HTML body with inline CSS for styling
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #000000;">
            <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                    <td style="padding: 20px 0; text-align: center;">
                        <img src="https://i.pinimg.com/originals/e4/e5/9c/e4e59c5f8f24911505a7436b61142714.jpg" alt="App Logo" width="100" style="display: block; margin: 0 auto;"/>
                        <h2 style="color: white; margin: 0;">ReelMaker</h2>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 40px; background-color: #ffffff;">
                        <p style="color: #000000;">
                            You have requested to change your password. Please use the OTP below to proceed with the password reset process:
                        </p>
                        <div style="text-align: center; margin: 20px 0;">
                            <span style="display: inline-block; font-size: 24px; color: #1E90FF; font-weight: bold; padding: 10px 20px; border: 1px solid #1E90FF; border-radius: 5px;">
                                {otp}
                            </span>
                        </div>
                        <p style="color: #000000;">
                            This OTP is valid for only a limited time. If you did not request this, please ignore this email.
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center; padding: 10px; background-color: #000000; color: #777;">
                        <p>Thank you for using <strong>ReelMaker</strong>!</p>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """


    # Set up the MIME
    msg = MIMEMultipart("alternative")
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_body, "html"))

    # Connect to the SMTP server
    with smtplib.SMTP("64.233.184.108", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        server.sendmail(os.getenv("EMAIL_USER"), to_email, msg.as_string())
        server.quit()

    st.session_state["otp_sent"] = True


def forgot_password_page():
    # Streamlit UI
    st.title(":material/person_alert: Forgot Password")

    with st.form("Forgot Password"):

        # Input for email
        st.session_state["email"] = st.text_input(
            "Email", disabled=st.session_state["otp_sent"]
        )

        if st.session_state["otp_verified"]:
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")

            with st.columns([0.3, 0.4, 0.3])[1]:
                if st.form_submit_button(
                    label="Update Password", type="primary", use_container_width=True
                ):
                    if re.match(password_regex, new_pass) is None:
                        st.error("Provide strong password")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match")
                    else:
                        hashed_password = hashlib.sha256(new_pass.encode()).hexdigest()

                        conn = create_connection()
                        cursor = conn.cursor()

                        cursor.execute(
                            """
                                    UPDATE users
                                    SET password = %s WHERE email = %s
                                """,
                            (
                                hashed_password,
                                st.session_state["email"],
                            ),
                        )

                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.session_state["otp_sent"] = False
                        st.session_state["otp_verified"] = False
                        st.session_state["email"] = None
                        st.session_state["show_balloons"] = True
                        st.rerun()
        else:

            if st.session_state["otp_sent"]:
                given_otp = st.text_input("OTP")

                with st.columns([0.3, 0.4, 0.3])[1]:
                    if st.form_submit_button(
                        label="Verify OTP", type="primary", use_container_width=True
                    ):
                        if given_otp == st.session_state["user_otp"]:
                            st.session_state["otp_verified"] = True
                            st.rerun()
                        else:
                            st.error("Invalid OTP")

            else:

                with st.columns([0.3, 0.4, 0.3])[1]:
                    if st.form_submit_button(
                        "Send OTP", type="primary", use_container_width=True
                    ):
                        if re.match(email_regex, st.session_state["email"]) is None:
                            st.error("Please enter a valid email.")
                        elif email_exists_in_db(st.session_state["email"]):
                            st.error("Email does not exist")
                        else:
                            st.session_state["user_otp"] = str(
                                random.randint(100000, 999999)
                            )

                            if not st.session_state["otp_sent"]:
                                with st.spinner("Sending..."):
                                    
                                    # Send email if validation and existence checks pass
                                    send_email(
                                        st.session_state["email"],
                                        "Password Change",
                                        st.session_state["user_otp"],
                                    )

                                    st.success("OTP sent successfully!")
                                    st.rerun()
