import streamlit as st
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import AudioFileClip
import os

def sanitize_filename(filename):
    bad_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in bad_chars:
        filename = filename.replace(char, '')
    return filename

def download_and_convert(url, audio_format, convert, download_dir):
    yt = YouTube(url, on_progress_callback=on_progress)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    output_path = video.download(filename=sanitize_filename(video.title), output_path=download_dir)
    media_type = 'video/mp4'
    
    if convert:
        audio_output_path = f"{output_path.rsplit('.', 1)[0]}.{audio_format}"
        AudioFileClip(output_path).write_audiofile(audio_output_path)
        output_path = audio_output_path
        media_type = f'audio/{audio_format}'

    return output_path, media_type

st.title("YouTube Downloader & Converter")

query = st.text_input("Input here")

audio_format = st.selectbox("Choose Audio Format", ["mp3", "wav"])

convert = st.checkbox("Convert to audio?")

# diretório padrão que pode ser alterado pelo usuário
download_dir = st.text_input("Enter download directory", value='C:\\Users\\mauro\\Downloads')

if st.button("Download"):
    if os.path.exists(download_dir):
        output_path, media_type = download_and_convert(query, audio_format, convert, download_dir)
        if convert:
            st.audio(output_path, format=media_type)
        else:
            st.video(output_path, format=media_type)
    else:
        st.write(f"The directory {download_dir} does not exist.")











