import cv2
from openai import OpenAI
import requests
import whisper
import pyaudio
import wave
import threading
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import pyaudio
import wave
import whisper
from D_ID import Clips
import requests
import json
 

# # Audio capture settings
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "recordedFile.wav"

# # Initialize PyAudio
# audio = pyaudio.PyAudio()

# # Create a stream
# stream = audio.open(format=FORMAT, channels=CHANNELS,
#                     rate=RATE, input=True,
#                     frames_per_buffer=CHUNK)

# # Container for frames
# record_frames = []

# # Flag to control recording
# recording = True

# # Function to capture audio
# def capture_audio():
#     global recording
#     while recording:
#         data = stream.read(CHUNK, exception_on_overflow=False)
#         record_frames.append(data)

# # Start audio capture in a separate thread
# audio_thread = threading.Thread(target=capture_audio)
# audio_thread.start()
# print("Recording... Press 'q' and Enter to stop.")
# while True:
#     user_input = input()
#     if user_input.lower() == 'q':
#         recording = False
#         break
# # Ensure audio thread stops
# audio_thread.join()

# # Stop and close everything
# stream.stop_stream()
# stream.close()
# audio.terminate()

# # Save audio
# with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(audio.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(record_frames))

# print("Recording finished and saved to", WAVE_OUTPUT_FILENAME)

# Transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

transcript = transcribe_audio('PATH TO RECORDED AUDIO FILE.wav')
print(transcript)


def get_gpt_response(transcript):
    
    client = OpenAI( api_key="YOUR-API-KEY")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": transcript,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

gpt_response = get_gpt_response(transcript)
print(gpt_response)


def generate_video_with_did(transcript):
    
    api_key = "YOUR-API-KEY"
    
 
    url = "https://api.d-id.com/clips"

    # Change between presenter and source_url "presenter_id": "amy-Aq6OmGZnMt"
    payload = {
        "source_url":'YOUR-PATH-TO-IMG',
        "script": {
            "type": "text",
            "input":transcript,
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false"
        },
        "config": { "result_format": "mp4" },
        "presenter_id": "amy-Aq6OmGZnMt"
        
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic Y0c5MVpHVnNjSEpoZEdsck9UZEFaMjFoYVd3dVkyOXQ6cS1aRF9hcG1BdXYwRXgxUFhLbUNv"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def get_clips(id):
    import requests

    url = "https://api.d-id.com/clips/"+id

    headers = {
        "accept": "application/json",
        "authorization": "Basic Y0c5MVpHVnNjSEpoZEdsck9UZEFaMjFoYVd3dVkyOXQ6cS1aRF9hcG1BdXYwRXgxUFhLbUNv"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

generate_video_with_did(gpt_response)

get_clips('clp_j0yd_J8D_VrEtmPbBuQMT') # you will get the clips id while generating video
