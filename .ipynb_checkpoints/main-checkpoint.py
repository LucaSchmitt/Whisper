from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import whisper
import os

app = FastAPI()

model = whisper.load_model("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un fichier audio")

    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        result = model.transcribe(file_location, language="fr")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la transcription: {str(e)}")
    finally:
        os.remove(file_location)

    return PlainTextResponse(content=result["text"])