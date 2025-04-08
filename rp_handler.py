from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import tempfile
import os
import base64
import librosa
import runpod


# Load model globally for reuse across invocations
MODEL_ID = "Lingua-Connect/whisper-small-sw-bible"
processor = WhisperProcessor.from_pretrained(MODEL_ID)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_ID)
model.to("cuda" if torch.cuda.is_available() else "cpu")

def handler(event):
    try:
        # Get audio data from the request
        if "input" not in event or "audio_data" not in event["input"]:
            return {"error": "No audio data provided"}
        
        # Decode base64 audio data
        audio_data = base64.b64decode(event["input"]["audio_data"])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            temp.write(audio_data)
            temp_path = temp.name
        
        # Load audio using librosa
        audio_array, sampling_rate = librosa.load(temp_path, sr=16000)
        
        # Clean up temp file early
        os.unlink(temp_path)
        
        # Process with Whisper
        input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
        
        # Move to GPU if available
        if torch.cuda.is_available():
            input_features = input_features.to("cuda")
        
        # Generate tokens
        predicted_ids = model.generate(input_features)
        
        # Decode the tokens
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        return {"success": True, "transcription": transcription}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
    

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})