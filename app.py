import streamlit as st
import sys 
import os
import time 
import requests
from zipfile import ZipFile 

st.markdown('# 📝 **Audio Transcriber App**')
bar = st.progress(0)

# Get user audio
def get_audio():


    

    bar.progress(10)

def transcribe_audio():
    filename = 'AUDIO-2022-06-13-16-42-20.m4a'
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    bar.progress(20)
    #print('1. Audio file has been retrieved')            
    
    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))

    audio_url = response.json()['upload_url']
    bar.progress(30)

    #print('2. Audio file has been uploaded to AssemblyAI')

    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": audio_url
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }
    bar.progress(40)
    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    #print('3. Transcribing uploaded file.')

    transcript_id = transcript_input_response.json()["id"]
    bar.progress(50)
    # 6. Retrieve transcription results
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }

    transcript_output_response = requests.get(endpoint, headers=headers)

    #print('4. Retrieve transcription results')
    bar.progress(60)
    # Check if transcription is complete
    from time import sleep

    while transcript_output_response.json()['status'] != 'completed':
        sleep(5)
        st.warning('Transcription is processing ...')
        transcript_output_response = requests.get(endpoint, headers=headers)

    st.header('Output')
    st.success(transcript_output_response.json()["text"])


    # 8. Save transcribed text to file
    bar.progress(100)
    # Save as TXT file
    audio_txt = open('audio.txt', 'w')
    audio_txt.write(transcript_output_response.json()["text"])
    audio_txt.close()

    zip_file = ZipFile('transcription.zip', 'w')
    zip_file.write('test.txt')
    zip_file.close()

#####


# The App
# 1. Read API from text file
api_key = st.secrets['api_key']

#st.info('1. API is read ...')
st.warning('Awaiting audio to be submitted.')


# Sidebar
st.sidebar.header('Input audio')


with st.sidebar.form(key='my_form'):
	URL = st.text_input('Upload audio file')
	submit_button = st.form_submit_button(label='Go')

# Run custom functions if URL is entered
if submit_button:
    get_audio()
    transcribe_audio()

    with open("transcription.zip", "rb") as zip_download:
        btn = st.download_button(
            label="Download ZIP",
            data=zip_download,
            file_name="transcription.zip",
            mime="application/zip"
        )
