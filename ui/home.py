import streamlit as st


def home_page():
    st.title(f"Welcome {st.session_state['name']}")
    st.write(
        """
        This application allows you to upload a long video and generate short video clips (reels) from it. 
        Follow the steps below to get started!
        """
    )

    with st.columns([0.1, 0.8, 0.1])[1]:
        # Create cards
        card(
            '1.  <i class="bi bi-1-circle"></i> Upload Video',
            "Click on the 'Upload Video' section to upload the video you want to process.",
        )
        card(
            "2. Generate Reel",
            "After uploading video, go to the 'Generate Reel' section to create short clips.",
        )
        card(
            "3. Download Clips", "Once the reels are generated, you can download them."
        )

    st.markdown(
        """# Guidelines for Uploading Videos

To ensure you get the best experience and results, please follow these simple guidelines when uploading your video:

1. **Video Duration**  
   - Your video should be between **5 to 20 minutes** long.  
   - Videos shorter than 5 minutes may not generate enough highlights.  
   - Videos longer than 20 minutes might reduce processing quality and efficiency.  

2. **Language**  
   - The application works best with **English-language videos**.  
   - Non-English content may lead to inaccurate processing or summaries.  

3. **Supported Video Formats**  
   - Ensure your video is in one of the commonly supported formats, such as **MP4, MPEG4**.  

4. **Content Quality**  
   - For optimal results, ensure your video has:  
     - **Clear audio** without significant background noise.  
     - **High-quality visuals** with minimal distortion or blurring.  

5. **Output**  
   - The platform will generate **short, engaging reels** based on key moments detected in your video.  

6. **Processing Time**  
   - Depending on the length and quality of your video, processing might take a few minutes. Please be patient.  

7. **Restrictions**  
   - Please avoid uploading videos with:  
     - **Explicit or inappropriate content**.  
     - **Copyrighted material** unless you have permission.  

8. **Post-Processing Options**  
   - Once your reels are generated, you can **download them or share them** directly to supported platforms.  

By following these guidelines, you’ll ensure smooth operation and high-quality results from the application.  
**Happy creating!** 🎥✨
"""
    )


# Function to create a card
def card(title, description):
    st.markdown(
        f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
