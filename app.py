import os
import streamlit as st
from pytube import YouTube
from pytube.cli import on_progress
from youtubesearchpython import VideosSearch
from moviepy.editor import AudioFileClip

def sanitize_filename(filename):
    bad_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in bad_chars:
        filename = filename.replace(char, '')
    return filename

def download_and_convert(url, video_quality, audio_format, convert, directory):
    yt = YouTube(url, on_progress_callback=on_progress)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    if video is None:
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    output_path = video.download(filename=sanitize_filename(video.title), output_path=directory)
    media_type = 'video/mp4'
    
    if convert:
        audio_output_path = f"{output_path.rsplit('.', 1)[0]}.{audio_format}"
        audioclip = AudioFileClip(output_path)
        audioclip.write_audiofile(audio_output_path)
        output_path = audio_output_path
        media_type = f'audio/{audio_format}'

    return output_path, media_type

def search_and_download(search_query, video_quality, audio_format, convert, directory):
    videos_search = VideosSearch(search_query, limit=10).result()["result"]
    video_title = videos_search[0]['title']
    video_url = videos_search[0]['link']
    return download_and_convert(video_url, video_quality, audio_format, convert, directory)

st.title("YouTube Downloader & Converter")

query = st.text_input("Enter URL or Search Query")

video_quality = st.selectbox("Choose Video Quality", ["720p", "360p"])

audio_format = st.selectbox("Choose Audio Format", ["mp3", "wav"])

convert = st.checkbox("Convert to audio?")

directory = st.text_input("Enter Directory Path")

if st.button("Download") and directory:
    # If directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    if "youtube.com" in query or "youtu.be" in query:
        output_path, media_type = download_and_convert(query, video_quality, audio_format, convert, directory)
    else:
        output_path, media_type = search_and_download(query, video_quality, audio_format, convert, directory)

    if not convert:
        st.video(output_path)
    else:
        st.audio(output_path, format=media_type)









