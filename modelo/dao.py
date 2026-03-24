from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Refugio(db.Model):
    __tablename__ = 'Refugios'

    id_refugio = Column(Integer, primary_key=True, autoincrement=True)
    nombre_refugio = Column(String(100), nullable=False)
    direccion = Column(String(255))
    id_ciudad = Column(Integer, ForeignKey('Ciudades.id_ciudad'), nullable=False)
    id_admin = Column(Integer, ForeignKey('Usuarios.id_usuario'), nullable=False)

    ciudad = relationship('Ciudad', back_populates='refugios', lazy=True)
    admin = relationship('Usuario', back_populates='refugios', lazy=True)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Refugio.query.get(id)

    def consultaGeneral(self):
        return Refugio.query.all()

    def eliminar(self, id):
        refugio = self.consultaIndividual(id)
        if refugio:
            db.session.delete(refugio)
            db.session.commit()
            
    def __str__(self):
        return self.nombre_refugio

class Mascota(db.Model):
    __tablename__ = 'Mascotas'

    id_mascota = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(10), nullable=False)
    raza = Column(String(100))
    edad = Column(Integer)
    sexo = Column(String(1))
    estado = Column(String(20), nullable=False)
    foto = Column(LargeBinary)
    id_refugio = Column(Integer, ForeignKey('Refugios.id_refugio'), nullable=False)

    refugio = relationship('Refugio', backref='mascotas', lazy=True)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Mascota.query.get(id)

    def consultaGeneral(self):
        return Mascota.query.all()

    def consultaPorRefugio(self, id_refugio):
        return Mascota.query.filter_by(id_refugio=id_refugio).all()
    
    def consultaImagen(self, id):
        return self.consultaIndividual(id).foto

    def eliminar(self, id):
        pet = self.consultaIndividual(id)
        if pet:
            db.session.delete(pet)
            db.session.commit()

class Ciudad(db.Model):
    __tablename__ = 'Ciudades'
    
    id_ciudad = Column(Integer, primary_key=True, autoincrement=True)
    nombre_ciudad = Column(String(100), nullable=False)
    
    refugios = relationship('Refugio', back_populates='ciudad', lazy=True)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Ciudad.query.get(id)

    def consultaGeneral(self):
        return Ciudad.query.all()

    def eliminar(self, id):
        ciudad = self.consultaIndividual(id)
        if ciudad:
            db.session.delete(ciudad)
            db.session.commit()
            
    def __str__(self):
        return self.nombre_ciudad

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    contraseña = Column(String(255), nullable=False)
    telefono = Column(String(20))
    rol = Column(String(20), nullable=False)
    
    refugios = relationship('Refugio', back_populates='admin', lazy=True)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Usuario.query.get(id)

    def consultaGeneral(self):
        return Usuario.query.all()

    def consultaPorCorreo(self, correo):
        return Usuario.query.filter_by(correo=correo).first()

    def eliminar(self, id):
        usuario = self.consultaIndividual(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            
    def __str__(self):
        return self.nombre

class SolicitudAdopcion(db.Model):
    __tablename__ = 'Solicitudes_Adopcion'

    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_mascota = Column(Integer, ForeignKey('Mascotas.id_mascota'), nullable=False)
    fecha_solicitud = Column(DateTime, default=db.func.now())
    estado = Column(String(20), nullable=False)
    observaciones = Column(String(255))

    usuario = relationship('Usuario', backref='solicitudes_adopcion', lazy=True)
    mascota = relationship('Mascota', backref='solicitudes_adopcion', lazy=True)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return SolicitudAdopcion.query.get(id)

    def consultaGeneral(self):
        return SolicitudAdopcion.query.all()

    def consultaPorUsuario(self, id_usuario):
        return SolicitudAdopcion.query.filter_by(id_usuario=id_usuario).all()

    def consultaPorMascota(self, id_mascota):
        return SolicitudAdopcion.query.filter_by(id_mascota=id_mascota).all()

    def consultaPorRefugio(self, id_refugio):
        return SolicitudAdopcion.query.join(Mascota).filter(Mascota.id_refugio == id_refugio).all()

    def eliminar(self, id):
        solicitud = self.consultaIndividual(id)
        if solicitud:
            db.session.delete(solicitud)
            db.session.commit()
            
    def __str__(self):
        return f"Solicitud {self.id_solicitud} - {self.mascota.nombre} por {self.usuario.nombre}"