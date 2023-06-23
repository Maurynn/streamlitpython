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

def baixar_e_converter(url, formato_audio, converter):
    yt = YouTube(url, on_progress_callback=on_progress)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    output_path = video.download(filename=sanitize_filename(video.title))
    tipo_midia = 'video/mp4'
    
    if converter:
        audio_output_path = f"{output_path.rsplit('.', 1)[0]}.{formato_audio}"
        AudioFileClip(output_path).write_audiofile(audio_output_path)
        output_path = audio_output_path
        tipo_midia = f'audio/{formato_audio}'

    return output_path, tipo_midia

st.title("YouTube Downloader & Conversor")

url = st.text_input("Coloque aqui a URL do vídeo")

formato_audio = st.selectbox("Escolha o formato do áudio", ["mp3", "wav"])

converter = st.checkbox("Converter para áudio?")

if st.button("Baixar"):
    output_path, tipo_midia = baixar_e_converter(url, formato_audio, converter)
    if converter:
        st.audio(output_path, format=tipo_midia)
    else:
        st.video(output_path, format=tipo_midia)













