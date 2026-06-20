from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from database import SessionLocal, engine, Base
import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Papita Veterinaria API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── AUTH ──────────────────────────────────────────────────────────────────────

@app.post("/auth/login", response_model=schemas.UsuarioOut)
def login(data: schemas.LoginInput, db: Session = Depends(get_db)):
    user = crud.get_usuario_by_email(db, data.email)
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return user

@app.post("/auth/register", response_model=schemas.UsuarioOut, status_code=201)
def register(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.create_usuario(db, data)

# ── USUARIOS ──────────────────────────────────────────────────────────────────

@app.get("/usuarios", response_model=List[schemas.UsuarioOut])
def list_usuarios(rol: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, rol=rol)

@app.get("/usuarios/{uid}", response_model=schemas.UsuarioOut)
def get_usuario(uid: int, db: Session = Depends(get_db)):
    u = crud.get_usuario(db, uid)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u

# ── MASCOTAS ──────────────────────────────────────────────────────────────────

@app.get("/mascotas", response_model=List[schemas.MascotaOut])
def list_mascotas(cliente_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_mascotas(db, cliente_id=cliente_id)

@app.get("/mascotas/{mid}", response_model=schemas.MascotaOut)
def get_mascota(mid: int, db: Session = Depends(get_db)):
    m = crud.get_mascota(db, mid)
    if not m:
        raise HTTPException(404, "Mascota no encontrada")
    return m

@app.post("/mascotas", response_model=schemas.MascotaOut, status_code=201)
def create_mascota(data: schemas.MascotaCreate, db: Session = Depends(get_db)):
    return crud.create_mascota(db, data)

@app.put("/mascotas/{mid}", response_model=schemas.MascotaOut)
def update_mascota(mid: int, data: schemas.MascotaUpdate, db: Session = Depends(get_db)):
    m = crud.update_mascota(db, mid, data)
    if not m:
        raise HTTPException(404, "Mascota no encontrada")
    return m

@app.delete("/mascotas/{mid}", status_code=204)
def delete_mascota(mid: int, db: Session = Depends(get_db)):
    if not crud.delete_mascota(db, mid):
        raise HTTPException(404, "Mascota no encontrada")

# ── TURNOS ────────────────────────────────────────────────────────────────────

@app.get("/turnos", response_model=List[schemas.TurnoOut])
def list_turnos(
    cliente_id: Optional[int] = None,
    vet_id: Optional[int] = None,
    estado: Optional[str] = None,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return crud.get_turnos(db, cliente_id=cliente_id, vet_id=vet_id,
                           estado=estado, desde=desde, hasta=hasta)

@app.get("/turnos/{tid}", response_model=schemas.TurnoOut)
def get_turno(tid: int, db: Session = Depends(get_db)):
    t = crud.get_turno(db, tid)
    if not t:
        raise HTTPException(404, "Turno no encontrado")
    return t

@app.post("/turnos", response_model=schemas.TurnoOut, status_code=201)
def create_turno(data: schemas.TurnoCreate, db: Session = Depends(get_db)):
    return crud.create_turno(db, data)

@app.patch("/turnos/{tid}/estado", response_model=schemas.TurnoOut)
def cambiar_estado_turno(tid: int, data: schemas.CambioEstado, db: Session = Depends(get_db)):
    t = crud.cambiar_estado_turno(db, tid, data.estado)
    if not t:
        raise HTTPException(404, "Turno no encontrado")
    return t

@app.delete("/turnos/{tid}", status_code=204)
def delete_turno(tid: int, db: Session = Depends(get_db)):
    if not crud.delete_turno(db, tid):
        raise HTTPException(404, "Turno no encontrado")

# ── HISTORIAL ─────────────────────────────────────────────────────────────────

@app.get("/historial", response_model=List[schemas.HistorialOut])
def list_historial(mascota_id: Optional[int] = None, vet_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_historial(db, mascota_id=mascota_id, vet_id=vet_id)

@app.get("/historial/{hid}", response_model=schemas.HistorialOut)
def get_historial_entry(hid: int, db: Session = Depends(get_db)):
    h = crud.get_historial_entry(db, hid)
    if not h:
        raise HTTPException(404, "Registro no encontrado")
    return h

@app.post("/historial", response_model=schemas.HistorialOut, status_code=201)
def create_historial(data: schemas.HistorialCreate, db: Session = Depends(get_db)):
    return crud.create_historial(db, data)

# ── CALIFICACIONES ────────────────────────────────────────────────────────────

@app.get("/calificaciones", response_model=List[schemas.CalificacionOut])
def list_calificaciones(vet_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_calificaciones(db, vet_id=vet_id)

@app.post("/calificaciones", response_model=schemas.CalificacionOut, status_code=201)
def create_calificacion(data: schemas.CalificacionCreate, db: Session = Depends(get_db)):
    if crud.get_calificacion_por_turno(db, data.turno_id):
        raise HTTPException(400, "Este turno ya fue calificado")
    return crud.create_calificacion(db, data)

# ── SLOTS DISPONIBLES ─────────────────────────────────────────────────────────

@app.get("/slots")
def get_slots(vet_id: int, fecha: date, db: Session = Depends(get_db)):
    return crud.get_slots_disponibles(db, vet_id=vet_id, fecha=fecha)

# ── STATS ─────────────────────────────────────────────────────────────────────

@app.get("/stats/dashboard")
def get_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)
