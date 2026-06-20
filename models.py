from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    telefono = Column(String, default="")
    rol = Column(String, nullable=False)          # CLIENTE | VETERINARIO | ADMINISTRATIVO
    activo = Column(Boolean, default=True)
    direccion = Column(String, default="")
    matricula = Column(String, default="")        # solo VETERINARIO
    especialidad = Column(String, default="")     # solo VETERINARIO

    mascotas = relationship("Mascota", back_populates="cliente", foreign_keys="Mascota.cliente_id")
    turnos_como_cliente = relationship("Turno", back_populates="cliente", foreign_keys="Turno.cliente_id")
    turnos_como_vet = relationship("Turno", back_populates="veterinario", foreign_keys="Turno.vet_id")
    historiales = relationship("Historial", back_populates="veterinario", foreign_keys="Historial.vet_id")
    calificaciones_dadas = relationship("Calificacion", back_populates="cliente", foreign_keys="Calificacion.cliente_id")
    calificaciones_recibidas = relationship("Calificacion", back_populates="veterinario", foreign_keys="Calificacion.vet_id")


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raza = Column(String, default="")
    fecha_nacimiento = Column(Date, nullable=True)
    peso = Column(Float, default=0.0)
    sexo = Column(String, default="")

    cliente = relationship("Usuario", back_populates="mascotas", foreign_keys=[cliente_id])
    turnos = relationship("Turno", back_populates="mascota")
    historial = relationship("Historial", back_populates="mascota")


class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    vet_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(String, nullable=False)
    estado = Column(String, default="PENDIENTE")   # PENDIENTE | CONFIRMADO | COMPLETADO | CANCELADO
    fecha_creacion = Column(Date, default=func.current_date())

    cliente = relationship("Usuario", back_populates="turnos_como_cliente", foreign_keys=[cliente_id])
    veterinario = relationship("Usuario", back_populates="turnos_como_vet", foreign_keys=[vet_id])
    mascota = relationship("Mascota", back_populates="turnos")
    historial = relationship("Historial", back_populates="turno", uselist=False)
    calificacion = relationship("Calificacion", back_populates="turno", uselist=False)


class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, index=True)
    turno_id = Column(Integer, ForeignKey("turnos.id"), nullable=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    vet_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    motivo_consulta = Column(Text, nullable=False)
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text, default="")
    observaciones = Column(Text, default="")
    fecha_registro = Column(DateTime, default=func.now())

    turno = relationship("Turno", back_populates="historial")
    mascota = relationship("Mascota", back_populates="historial")
    veterinario = relationship("Usuario", back_populates="historiales", foreign_keys=[vet_id])


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    turno_id = Column(Integer, ForeignKey("turnos.id"), nullable=False)
    vet_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    puntuacion = Column(Integer, nullable=False)
    comentario = Column(Text, default="")
    fecha = Column(Date, default=func.current_date())

    turno = relationship("Turno", back_populates="calificacion")
    veterinario = relationship("Usuario", back_populates="calificaciones_recibidas", foreign_keys=[vet_id])
    cliente = relationship("Usuario", back_populates="calificaciones_dadas", foreign_keys=[cliente_id])
