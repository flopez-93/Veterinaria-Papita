from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


# ── AUTH ──────────────────────────────────────────────────────────────────────

class LoginInput(BaseModel):
    email: str
    password: str


# ── USUARIO ───────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    telefono: Optional[str] = ""
    rol: str = "CLIENTE"
    direccion: Optional[str] = ""
    matricula: Optional[str] = ""
    especialidad: Optional[str] = ""

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str
    rol: str
    activo: bool
    direccion: str
    matricula: str
    especialidad: str

    class Config:
        from_attributes = True


# ── MASCOTA ───────────────────────────────────────────────────────────────────

class MascotaCreate(BaseModel):
    cliente_id: int
    nombre: str
    especie: str
    raza: Optional[str] = ""
    fecha_nacimiento: Optional[date] = None
    peso: Optional[float] = 0.0
    sexo: Optional[str] = ""

class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso: Optional[float] = None
    sexo: Optional[str] = None

class MascotaOut(BaseModel):
    id: int
    cliente_id: int
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: Optional[date]
    peso: float
    sexo: str

    class Config:
        from_attributes = True


# ── TURNO ─────────────────────────────────────────────────────────────────────

class TurnoCreate(BaseModel):
    cliente_id: int
    mascota_id: int
    vet_id: int
    fecha: date
    hora: str

class CambioEstado(BaseModel):
    estado: str   # PENDIENTE | CONFIRMADO | COMPLETADO | CANCELADO

class TurnoOut(BaseModel):
    id: int
    cliente_id: int
    mascota_id: int
    vet_id: int
    fecha: date
    hora: str
    estado: str
    fecha_creacion: Optional[date]

    class Config:
        from_attributes = True


# ── HISTORIAL ─────────────────────────────────────────────────────────────────

class HistorialCreate(BaseModel):
    turno_id: Optional[int] = None
    mascota_id: int
    vet_id: int
    motivo_consulta: str
    diagnostico: str
    tratamiento: Optional[str] = ""
    observaciones: Optional[str] = ""

class HistorialOut(BaseModel):
    id: int
    turno_id: Optional[int]
    mascota_id: int
    vet_id: int
    motivo_consulta: str
    diagnostico: str
    tratamiento: str
    observaciones: str
    fecha_registro: Optional[datetime]

    class Config:
        from_attributes = True


# ── CALIFICACION ──────────────────────────────────────────────────────────────

class CalificacionCreate(BaseModel):
    turno_id: int
    vet_id: int
    cliente_id: int
    puntuacion: int
    comentario: Optional[str] = ""

class CalificacionOut(BaseModel):
    id: int
    turno_id: int
    vet_id: int
    cliente_id: int
    puntuacion: int
    comentario: str
    fecha: Optional[date]

    class Config:
        from_attributes = True
