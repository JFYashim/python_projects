import streamlit as st
import yt_dlp
import os

st.title("YouTube Video Downloader")

url = st.text_input("Enter YouTube Video URL:")

if st.button("Download Video"):
    if url:
        st.info("Processing video...")
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            with open(filename, "rb") as file:
                st.download_button(
                    label="Click here to save video",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4"
                )
            st.success("Download ready!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please paste a valid YouTube URL.")
