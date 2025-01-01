import streamlit as st


def apply_css():

    st.markdown(
        """
        <style>
            .stStatusWidget { 
                visibility: hidden; 
            }
            p {
                font-size: 20px;
            }
            .button-link {
                display: block;              /* Make the link behave like a block element */
                width: 100%;                 /* Full width of container */
                text-align: center;          /* Center-align text */
                font-weight: bold;           /* Bold text */
                text-decoration: none;       /* Remove underline from link */
                border-radius: 8px;          /* Rounded corners */
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* Subtle shadow */
                transition: 0.3s;            /* Transition effect */
            }
            .download-button{
                display: block; 
                width: 100%; 
                padding: 15px;
                margin-bottom: 30px;
                background-color: #9C27B0; 
                color: white; 
                border: none;
                border-radius: 5px; 
                cursor: pointer;
                font-size: 16px;
                text-align: center;
                transition: background-color 0.3s;
            }
            .card {
                border: 1px solid #B0B0B0;      /* Border color */
                border-radius: 8px;          /* Rounded corners */
                padding: 20px;                /* Inner padding */
                margin: 10px;                 /* Margin around cards */
                text-align: center;           /* Center text */
                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1); /* Shadow effect */
                transition: transform 0.2s;   /* Animation */
            }
            .card:hover {
                transform: scale(1.02);      /* Scale effect on hover */
            }
            .card h3 {
                margin: 0;                   /* Remove default margin */
            }
            .profile-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #B0B0B0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                max-width: 500px;
                margin: 0 auto;
            }
            .profile-header {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .profile-header img {
                border-radius: 50%;
            }
            .profile-details p {
                margin: 5px 0;
            }
            .detail-label {
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
