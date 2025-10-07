from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import httpx
import os
from datetime import datetime, date

from app.db.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.comprobante import Comprobante
from app.schemas.comprobante import ComprobanteInDB, VencimientoResponse
from app.core.config import settings

router = APIRouter()

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ComprobanteInDB, status_code=status.HTTP_201_CREATED)
async def upload_comprobante(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Subir comprobante y procesarlo con OCR"""
    # Guardar archivo
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Llamar al servicio OCR
    ocr_text = ""
    try:
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                files = {"file": (file.filename, f, file.content_type)}
                response = await client.post(f"{settings.OCR_SERVICE_URL}/ocr", files=files)
                
                if response.status_code == 200:
                    ocr_result = response.json()
                    ocr_text = ocr_result.get("text", "")
    except Exception as e:
        print(f"Error al llamar OCR service: {e}")
    
    # Crear registro en DB
    comprobante = Comprobante(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        ocr_text=ocr_text
    )
    
    db.add(comprobante)
    db.commit()
    db.refresh(comprobante)
    
    return comprobante

@router.get("/", response_model=List[ComprobanteInDB])
def list_comprobantes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar comprobantes del usuario"""
    comprobantes = db.query(Comprobante).filter(
        Comprobante.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return comprobantes

@router.get("/vencimientos", response_model=List[VencimientoResponse])
def get_vencimientos(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Dashboard de vencimientos próximos"""
    today = date.today()
    
    comprobantes = db.query(Comprobante).filter(
        Comprobante.user_id == current_user.id,
        Comprobante.fecha_vencimiento.isnot(None),
        Comprobante.fecha_vencimiento >= today
    ).order_by(Comprobante.fecha_vencimiento).all()
    
    result = []
    for comp in comprobantes:
        dias_restantes = (comp.fecha_vencimiento.date() - today).days
        result.append(VencimientoResponse(
            id=comp.id,
            filename=comp.filename,
            fecha_vencimiento=comp.fecha_vencimiento,
            dias_restantes=dias_restantes,
            monto_total=comp.monto_total,
            cuit=comp.cuit
        ))
    
    return result

@router.get("/{comprobante_id}", response_model=ComprobanteInDB)
def get_comprobante(
    comprobante_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener comprobante por ID"""
    comprobante = db.query(Comprobante).filter(
        Comprobante.id == comprobante_id,
        Comprobante.user_id == current_user.id
    ).first()
    
    if not comprobante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comprobante no encontrado"
        )
    
    return comprobante