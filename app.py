import sys 
import time 
import requests

f = open("api.txt", "r")
api_key = f.read()
filename = 'AUDIO-2022-06-13-16-42-20.m4a'

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

print('1. Audio file has been retrieved')            
 
headers = {'authorization': api_key}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

audio_url = response.json()['upload_url']

print('2. Audio file has been uploaded to AssemblyAI')

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
  "audio_url": audio_url
}

headers = {
    "authorization": api_key,
    "content-type": "application/json"
}

transcript_input_response = requests.post(endpoint, json=json, headers=headers)

print('3. Transcribing uploaded file.')

transcript_id = transcript_input_response.json()["id"]

# 6. Retrieve transcription results
endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
headers = {
    "authorization": api_key,
}

transcript_output_response = requests.get(endpoint, headers=headers)

print('4. Retrieve transcription results')

# Check if transcription is complete
from time import sleep

while transcript_output_response.json()['status'] != 'completed':
  sleep(5)
  print('Transcription is processing ...')
  transcript_output_response = requests.get(endpoint, headers=headers)

print('----------\n')
print('Output:\n')
print(transcript_output_response.json()["text"])


# 8. Save transcribed text to file

# Save as TXT file
yt_txt = open('test.txt', 'w')
yt_txt.write(transcript_output_response.json()["text"])
yt_txt.close()