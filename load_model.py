from transformers import WhisperProcessor, WhisperForConditionalGeneration

MODEL_ID = "Lingua-Connect/whisper-small-sw-bible"

print(f"Downloading model and processor from: {MODEL_ID}")

try:
    processor = WhisperProcessor.from_pretrained(MODEL_ID)
    model = WhisperForConditionalGeneration.from_pretrained(MODEL_ID)
    print("Model and processor downloaded successfully.")
except Exception as e:
    print("Failed to download model.")
    print(e)
    raise e