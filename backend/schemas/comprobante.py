from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComprobanteBase(BaseModel):
    filename: str
    tipo_comprobante: Optional[str] = None
    cuit: Optional[str] = None
    monto_total: Optional[float] = None
    fecha_emision: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None

class ComprobanteCreate(ComprobanteBase):
    file_path: str
    ocr_text: Optional[str] = None

class ComprobanteInDB(ComprobanteBase):
    id: int
    user_id: int
    file_path: str
    ocr_text: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class VencimientoResponse(BaseModel):
    id: int
    filename: str
    fecha_vencimiento: datetime
    dias_restantes: int
    monto_total: Optional[float]
    cuit: Optional[str]