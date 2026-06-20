"""
Seed de datos iniciales para Papita Veterinaria.
Ejecutar: python seed.py
"""
from database import SessionLocal, engine, Base
import models
from datetime import date, datetime

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Limpiar tablas en orden correcto
db.query(models.Calificacion).delete()
db.query(models.Historial).delete()
db.query(models.Turno).delete()
db.query(models.Mascota).delete()
db.query(models.Usuario).delete()
db.commit()

# ── USUARIOS ──────────────────────────────────────────────────────────────────
usuarios = [
    models.Usuario(id=1, nombre="María González",    email="maria@mail.com",  password="123", telefono="1134567890", rol="CLIENTE",        activo=True, direccion="Av. Corrientes 1234"),
    models.Usuario(id=2, nombre="Dr. Carlos Pérez",  email="carlos@vet.com",  password="123", telefono="1145678901", rol="VETERINARIO",     activo=True, matricula="MV-4521", especialidad="Clínica General"),
    models.Usuario(id=3, nombre="Dr. Ana Rodríguez", email="ana@vet.com",     password="123", telefono="1156789012", rol="VETERINARIO",     activo=True, matricula="MV-3892", especialidad="Cirugía"),
    models.Usuario(id=4, nombre="Laura Sánchez",     email="laura@mail.com",  password="123", telefono="1167890123", rol="ADMINISTRATIVO",  activo=True),
    models.Usuario(id=5, nombre="Juan Medina",       email="juan@mail.com",   password="123", telefono="1178901234", rol="CLIENTE",         activo=True, direccion="Belgrano 567"),
]
db.add_all(usuarios)
db.commit()

# ── MASCOTAS ──────────────────────────────────────────────────────────────────
mascotas = [
    models.Mascota(id=1, cliente_id=1, nombre="Firulais", especie="Perro", raza="Labrador",  fecha_nacimiento=date(2019, 3, 15),  peso=28.5, sexo="Macho"),
    models.Mascota(id=2, cliente_id=1, nombre="Misha",    especie="Gato",  raza="Persa",     fecha_nacimiento=date(2021, 7, 22),  peso=4.2,  sexo="Hembra"),
    models.Mascota(id=3, cliente_id=5, nombre="Rocky",    especie="Perro", raza="Bulldog",   fecha_nacimiento=date(2020, 11, 8),  peso=22.0, sexo="Macho"),
]
db.add_all(mascotas)
db.commit()

# ── TURNOS ────────────────────────────────────────────────────────────────────
turnos = [
    models.Turno(id=1, cliente_id=1, mascota_id=1, vet_id=2, fecha=date(2026, 6, 3),  hora="10:00", estado="CONFIRMADO", fecha_creacion=date(2026, 5, 20)),
    models.Turno(id=2, cliente_id=1, mascota_id=2, vet_id=3, fecha=date(2026, 6, 10), hora="14:30", estado="PENDIENTE",  fecha_creacion=date(2026, 5, 25)),
    models.Turno(id=3, cliente_id=5, mascota_id=3, vet_id=2, fecha=date(2026, 6, 5),  hora="09:00", estado="CONFIRMADO", fecha_creacion=date(2026, 5, 22)),
    models.Turno(id=4, cliente_id=1, mascota_id=1, vet_id=2, fecha=date(2026, 5, 15), hora="11:00", estado="COMPLETADO", fecha_creacion=date(2026, 5, 1)),
]
db.add_all(turnos)
db.commit()

# ── HISTORIAL ─────────────────────────────────────────────────────────────────
historial = [
    models.Historial(id=1, turno_id=4, mascota_id=1, vet_id=2,
        motivo_consulta="Control anual y vacunación",
        diagnostico="Estado general bueno. Vacuna antirrábica aplicada.",
        tratamiento="Vacuna antirrábica anual",
        observaciones="Próxima revisión en 6 meses",
        fecha_registro=datetime(2026, 5, 15, 11, 45)),
    models.Historial(id=2, turno_id=None, mascota_id=1, vet_id=2,
        motivo_consulta="Vómitos frecuentes",
        diagnostico="Gastritis aguda leve",
        tratamiento="Omeprazol 20mg por 7 días",
        observaciones="Dieta blanda 3 días",
        fecha_registro=datetime(2026, 3, 10, 10, 30)),
]
db.add_all(historial)
db.commit()

# ── CALIFICACIONES ────────────────────────────────────────────────────────────
calificaciones = [
    models.Calificacion(id=1, turno_id=4, vet_id=2, cliente_id=1,
        puntuacion=5,
        comentario="Muy buena atención, claro y amable con Firulais.",
        fecha=date(2026, 5, 15)),
]
db.add_all(calificaciones)
db.commit()
db.close()

print("✅ Seed completado: usuarios, mascotas, turnos, historial y calificaciones cargados.")
