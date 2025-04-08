from pydub import AudioSegment
import json
import base64

#get the audio and put it in the write format

audio = AudioSegment.from_file("./Runpod/WhatsApp Audio 2025-04-08 at 12.49.09 PM.mp4")

audio.export("./Runpod/output_audio.wav", format="wav")

# Load a real WAV file from disk
with open("./Runpod/output_audio.wav", "rb") as audio_file:
    audio_bytes = audio_file.read()

# Encode it as base64
encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")


# Your JSON object (can be a dictionary or a list)
event = {
    "input":{
        "audio_data": encoded_audio
    }

}

# Write JSON object to a file
with open('/home/eric-kaz/Desktop/Semester4.2/Project /Sem2 /fast_api/Runpod/test_input.json', 'w') as json_file:
    json.dump(event, json_file, indent=4)