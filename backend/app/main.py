import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables, get_session
from sqlmodel import Session, select
import shutil, requests

app = FastAPI(title="Asistente PyME")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoint simple para subir comprobante (MVP)
@app.post("/comprobantes/upload")
async def upload_comprobante(file: UploadFile = File(...), db: Session = Depends(get_session)):
    upload_dir = "/data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Llamar al microservicio OCR
    try:
        with open(file_path, "rb") as f:
            resp = requests.post("http://ocr:5000/ocr", files={"file": f}, timeout=20)
        text = resp.json().get("text", "")
    except Exception as e:
        text = ""
    # Guardar registro en DB - (aquí crearías la instancia y commit)
    return {"filename": file.filename, "ocr_text": text}
