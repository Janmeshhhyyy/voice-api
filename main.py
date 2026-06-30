from fastapi import FastAPI, Response
from pydantic import BaseModel
from transformers import pipeline
import scipy.io.wavfile as wavfile
import torch
import io
import uvicorn

# 1. Initialize the FastAPI app
app = FastAPI(title="Text-to-Speech Microservice")

# 2. Load the Model into memory ONCE when the server starts
print("Waking up the AI... Loading Meta MMS TTS model...")
synthesizer = pipeline(
    "text-to-speech", 
    model="facebook/mms-tts-eng", 
    device=0 if torch.cuda.is_available() else -1
)
print("Model loaded and ready for traffic!")

# 3. Define what the incoming web request should look like
class TTSRequest(BaseModel):
    text: str

# 4. Create the API Endpoint
@app.post("/generate-audio")
async def generate_audio(request: TTSRequest):
    print(f"Processing text: '{request.text}'")
    
    # Pass the incoming text to the transformer
    speech = synthesizer(request.text)
    
    # Extract audio data safely
    sample_rate = speech["sampling_rate"]
    audio_array = speech["audio"].squeeze()
    
    # Instead of saving to disk, write the .wav file to an in-memory buffer
    buffer = io.BytesIO()
    wavfile.write(buffer, rate=sample_rate, data=audio_array)
    
    # Send the buffer back to the user as an audio file over the internet!
    return Response(content=buffer.getvalue(), media_type="audio/wav")

# 5. Force the server to listen on port 7860
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)