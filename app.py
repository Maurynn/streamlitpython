import streamlit as st
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import AudioFileClip

def sanitize_filename(filename):
    bad_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in bad_chars:
        filename = filename.replace(char, '')
    return filename

def download_and_convert(url, video_quality, audio_format, convert):
    yt = YouTube(url, on_progress_callback=on_progress)
    if video_quality == "1080p":
        video = yt.streams.get_highest_resolution()
    else:
        video = yt.streams.filter(progressive=True, resolution=video_quality).first()
    
    output_path = video.download(filename=sanitize_filename(video.title))
    media_type = 'video/mp4'
    
    if convert:
        audio_output_path = f"{output_path.rsplit('.', 1)[0]}.{audio_format}"
        AudioFileClip(output_path).write_audiofile(audio_output_path)
        output_path = audio_output_path
        media_type = f'audio/{audio_format}'

    return output_path, media_type

st.title("Baixar e Converter Vídeos do YouTube")

query = st.text_input("Insira aqui a URL do vídeo do YouTube")

video_quality = st.selectbox("Escolha a qualidade do vídeo", ["1080p", "720p", "480p", "360p", "240p"])

audio_format = st.selectbox("Escolha o formato do áudio", ["mp3", "wav"])

convert = st.checkbox("Converter para áudio?")

if st.button("Baixar"):
    output_path, media_type = download_and_convert(query, video_quality, audio_format, convert)
    if convert:
        st.audio(output_path, format=media_type)
    else:
        st.video(output_path, format=media_type)












