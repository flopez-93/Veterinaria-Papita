from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date

import models, schemas

HORARIOS = ["09:00","09:30","10:00","10:30","11:00","11:30",
            "14:00","14:30","15:00","15:30","16:00","16:30"]

# ── USUARIOS ──────────────────────────────────────────────────────────────────

def get_usuario(db: Session, uid: int):
    return db.query(models.Usuario).filter(models.Usuario.id == uid).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db: Session, rol: Optional[str] = None):
    q = db.query(models.Usuario).filter(models.Usuario.activo == True)
    if rol:
        q = q.filter(models.Usuario.rol == rol)
    return q.all()

def create_usuario(db: Session, data: schemas.UsuarioCreate):
    u = models.Usuario(**data.model_dump())
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


# ── MASCOTAS ──────────────────────────────────────────────────────────────────

def get_mascota(db: Session, mid: int):
    return db.query(models.Mascota).filter(models.Mascota.id == mid).first()

def get_mascotas(db: Session, cliente_id: Optional[int] = None):
    q = db.query(models.Mascota)
    if cliente_id:
        q = q.filter(models.Mascota.cliente_id == cliente_id)
    return q.all()

def create_mascota(db: Session, data: schemas.MascotaCreate):
    m = models.Mascota(**data.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def update_mascota(db: Session, mid: int, data: schemas.MascotaUpdate):
    m = get_mascota(db, mid)
    if not m:
        return None
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return m

def delete_mascota(db: Session, mid: int):
    m = get_mascota(db, mid)
    if not m:
        return False
    db.delete(m)
    db.commit()
    return True


# ── TURNOS ────────────────────────────────────────────────────────────────────

def get_turno(db: Session, tid: int):
    return db.query(models.Turno).filter(models.Turno.id == tid).first()

def get_turnos(db: Session, cliente_id=None, vet_id=None,
               estado=None, desde=None, hasta=None):
    q = db.query(models.Turno)
    if cliente_id:
        q = q.filter(models.Turno.cliente_id == cliente_id)
    if vet_id:
        q = q.filter(models.Turno.vet_id == vet_id)
    if estado:
        q = q.filter(models.Turno.estado == estado)
    if desde:
        q = q.filter(models.Turno.fecha >= desde)
    if hasta:
        q = q.filter(models.Turno.fecha <= hasta)
    return q.order_by(models.Turno.fecha, models.Turno.hora).all()

def create_turno(db: Session, data: schemas.TurnoCreate):
    t = models.Turno(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def cambiar_estado_turno(db: Session, tid: int, nuevo_estado: str):
    t = get_turno(db, tid)
    if not t:
        return None
    t.estado = nuevo_estado
    db.commit()
    db.refresh(t)
    return t

def delete_turno(db: Session, tid: int):
    t = get_turno(db, tid)
    if not t:
        return False
    db.delete(t)
    db.commit()
    return True

def get_slots_disponibles(db: Session, vet_id: int, fecha: date):
    ocupados = db.query(models.Turno.hora).filter(
        models.Turno.vet_id == vet_id,
        models.Turno.fecha == fecha,
        models.Turno.estado.in_(["PENDIENTE", "CONFIRMADO"])
    ).all()
    ocupados_set = {h[0] for h in ocupados}
    return [{"hora": h, "disponible": h not in ocupados_set} for h in HORARIOS]


# ── HISTORIAL ─────────────────────────────────────────────────────────────────

def get_historial_entry(db: Session, hid: int):
    return db.query(models.Historial).filter(models.Historial.id == hid).first()

def get_historial(db: Session, mascota_id=None, vet_id=None):
    q = db.query(models.Historial)
    if mascota_id:
        q = q.filter(models.Historial.mascota_id == mascota_id)
    if vet_id:
        q = q.filter(models.Historial.vet_id == vet_id)
    return q.order_by(models.Historial.fecha_registro.desc()).all()

def create_historial(db: Session, data: schemas.HistorialCreate):
    h = models.Historial(**data.model_dump())
    db.add(h)
    if data.turno_id:
        t = get_turno(db, data.turno_id)
        if t:
            t.estado = "COMPLETADO"
    db.commit()
    db.refresh(h)
    return h


# ── CALIFICACIONES ────────────────────────────────────────────────────────────

def get_calificacion_por_turno(db: Session, turno_id: int):
    return db.query(models.Calificacion).filter(
        models.Calificacion.turno_id == turno_id).first()

def get_calificaciones(db: Session, vet_id=None):
    q = db.query(models.Calificacion)
    if vet_id:
        q = q.filter(models.Calificacion.vet_id == vet_id)
    return q.order_by(models.Calificacion.fecha.desc()).all()

def create_calificacion(db: Session, data: schemas.CalificacionCreate):
    c = models.Calificacion(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


# ── STATS ─────────────────────────────────────────────────────────────────────

def get_dashboard_stats(db: Session):
    total_turnos = db.query(func.count(models.Turno.id)).scalar()
    turnos_hoy = db.query(func.count(models.Turno.id)).filter(
        models.Turno.fecha == date.today()).scalar()
    total_mascotas = db.query(func.count(models.Mascota.id)).scalar()
    total_clientes = db.query(func.count(models.Usuario.id)).filter(
        models.Usuario.rol == "CLIENTE").scalar()
    pendientes = db.query(func.count(models.Turno.id)).filter(
        models.Turno.estado == "PENDIENTE").scalar()
    promedio_cal = db.query(func.avg(models.Calificacion.puntuacion)).scalar()

    return {
        "total_turnos": total_turnos,
        "turnos_hoy": turnos_hoy,
        "total_mascotas": total_mascotas,
        "total_clientes": total_clientes,
        "turnos_pendientes": pendientes,
        "promedio_calificacion": round(promedio_cal, 2) if promedio_cal else None,
    }
