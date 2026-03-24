from flask import Flask, render_template, url_for, request, redirect
from modelo.dao import db, Refugio, Mascota, Usuario, Ciudad, SolicitudAdopcion

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789./@localhost:3308/adoptamex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/imagen_mascota/<int:id>')
def imagen_mascota(id):
    pet = Mascota()
    return pet.consultaImagen(id)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('index.html')

@app.route('/acercade')
def acercaDe():
    return render_template('acercade.html')

@app.route('/usuarios')
def usuarios():
    user_obj = Usuario()
    users = user_obj.consultaGeneral()
    return render_template('usuarios.html', adoptantes=users)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nuevo = Usuario()
        nuevo.nombre = request.form['nombre']
        nuevo.correo = request.form['email']
        nuevo.contraseña = request.form['contrasena']
        nuevo.telefono = request.form['tel']
        nuevo.rol = 'adoptante'
        nuevo.agregar()
        return redirect(url_for('usuarios'))
    return render_template('registro.html')

@app.route('/editarUsuarios/<int:id>', methods=['GET', 'POST'])
def editarUsuarios(id):
    user = Usuario().consultaIndividual(id)
    if not user:
        return "Usuario no encontrado", 404

    if request.method == 'POST':
        user.nombre = request.form['nombre']
        user.correo = request.form['email']
        user.contraseña = request.form['contrasena']
        user.telefono = request.form['tel']
        user.editar()
        return redirect(url_for('usuarios'))

    return render_template('editarUsuarios.html', usuario=user)

@app.route('/eliminarUsuarios/<int:id>', methods=['GET', 'POST'])
def eliminarUsuarios(id):
    user = Usuario().consultaIndividual(id)
    if not user:
        return "Usuario no encontrado", 404

    if request.method == 'POST':
        Usuario().eliminar(id)
        return redirect(url_for('usuarios'))

    return render_template('eliminarUsuarios.html', usuario=user)

@app.route('/login', methods=('GET','POST'))
def login():
    msg = ""
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        usuario = Usuario().consultaPorCorreo(correo)
        if usuario and usuario.contraseña == contrasena:
            return redirect(url_for('menu'))
        msg = 'Datos incorrectos'
    
    return render_template('login.html', msg=msg)

@app.route('/mascotas')
def mascotas():
    pet_obj = Mascota()
    pets = pet_obj.consultaGeneral()
    return render_template('mascotas.html', pets=pets)

@app.route('/registrarMascota', methods=['GET', 'POST'])
def registrarMascota():
    refugios = Refugio().consultaGeneral()
    if request.method == 'POST':
        nueva = Mascota()
        
        nueva.nombre = request.form['nombre']
        nueva.especie = request.form['especie'].lower()
        nueva.raza = request.form['raza']
        nueva.edad = int(request.form['edad']) if request.form['edad'] else 0
        nueva.sexo = request.form['sexo'][0].upper() 
        nueva.estado = request.form['estado'].lower()
        nueva.foto= request.files['foto'].stream.read()
        nueva.id_refugio = request.values['refugio']
        nueva.agregar()
        return redirect(url_for('mascotas'))
    return render_template('registrarMascota.html', refugios=refugios)

@app.route('/editarMascota/<int:id>', methods=['GET', 'POST'])
def editarMascota(id):
    pet = Mascota().consultaIndividual(id)
    refugios = Refugio().consultaGeneral()
    if not pet:
        return "Mascota no encontrada", 404

    if request.method == 'POST':
        pet.nombre = request.form['nombre']
        pet.especie = request.form['especie']
        pet.raza = request.form['raza']
        pet.edad = int(request.form['edad']) if request.form['edad'] else 0
        pet.sexo = request.form['sexo'][0].upper()
        pet.estado = request.form['estado']
        if 'foto' in request.files:
            file = request.files['foto']
            if file.filename !='':
                pet.foto=request.files['foto'].stream.read()
        pet.id_refugio=request.values['refugio']
        pet.editar()
        return redirect(url_for('mascotas'))

    return render_template('editarMascota.html', pet=pet, refugios=refugios)

@app.route('/eliminarMascota/<int:id>', methods=['GET', 'POST'])
def eliminarMascota(id):
    pet = Mascota().consultaIndividual(id)
    if not pet:
        return "Mascota no encontrada", 404

    if request.method == 'POST':
        Mascota().eliminar(id)
        return redirect(url_for('mascotas'))

    return render_template('eliminarMascota.html', pet=pet)

@app.route('/mascotaDetalles/<int:id>')
def mascotaDetalles(id):
    pet = Mascota().consultaIndividual(id)
    if not pet:
        return "Mascota no encontrada", 404
    ruta_imagen = pet.foto
    return render_template('mascotaDetalles.html', pet=pet, ruta_imagen=ruta_imagen)

@app.route('/refugios')
def refugios():
    refugio_obj = Refugio()
    refugiosL = refugio_obj.consultaGeneral()
    return render_template('refugios.html', refugiosL=refugiosL)

@app.route('/registrarRefugio', methods=['GET', 'POST'])
def registrarRefugio():
    ciudades = Ciudad().consultaGeneral()
    usuarios = Usuario().consultaGeneral()
    
    if request.method == 'POST':
        nuevo = Refugio()
        nuevo.nombre_refugio = request.form['nombre']
        nuevo.direccion = request.form['ubicacion']
        nuevo.id_ciudad = request.form['ciudad']
        nuevo.id_admin = request.form['admin']
        nuevo.agregar()
        return redirect(url_for('refugios'))
    return render_template('registrarRefugio.html', ciudades=ciudades, usuarios=usuarios)

@app.route('/editarRefugio/<int:id>', methods=['GET', 'POST'])
def editarRefugio(id):
    refugio_obj = Refugio().consultaIndividual(id)
    ciudades = Ciudad().consultaGeneral()
    usuarios = Usuario().consultaGeneral()
    
    if not refugio_obj:
        return "Refugio no encontrado", 404
        
    if request.method == 'POST':
        refugio_obj.nombre_refugio = request.form['nombre']
        refugio_obj.direccion = request.form['ubicacion']
        refugio_obj.id_ciudad = request.form['ciudad']
        refugio_obj.id_admin = request.form['admin']
        refugio_obj.editar()
        return redirect(url_for('refugios'))
        
    return render_template('editarRefugio.html', refugio=refugio_obj, ciudades=ciudades, usuarios=usuarios)

@app.route('/eliminarRefugio/<int:id>', methods=['GET', 'POST'])
def eliminarRefugio(id):
    refugio_obj = Refugio().consultaIndividual(id)
    if not refugio_obj:
        return "Refugio no encontrado", 404
    if request.method == 'POST':
        Refugio().eliminar(id)
        return redirect(url_for('refugios'))
    return render_template('eliminarRefugio.html', refugio=refugio_obj)

@app.route('/refugioDetalles/<int:id>')
def refugioDetalles(id):
    refugio_obj = Refugio().consultaIndividual(id)
    if not refugio_obj:
        return "Refugio no encontrado", 404
    mascotas_del_refugio = Mascota().consultaPorRefugio(id)
    return render_template('refugioDetalles.html', refugio=refugio_obj, mascotas=mascotas_del_refugio)

@app.route('/ciudades')
def ciudades():
    ciudad_obj = Ciudad()
    ciudadesL = ciudad_obj.consultaGeneral()
    return render_template('ciudades.html', ciudades=ciudadesL)

@app.route('/registrarCiudad', methods=['GET', 'POST'])
def registrarCiudad():
    if request.method == 'POST':
        nueva = Ciudad()
        nueva.nombre_ciudad = request.form['nombre']
        nueva.agregar()
        return redirect(url_for('ciudades'))
    return render_template('registrarCiudad.html')

@app.route('/editarCiudad/<int:id>', methods=['GET', 'POST'])
def editarCiudad(id):
    ciudad = Ciudad().consultaIndividual(id)
    if not ciudad:
        return "Ciudad no encontrada", 404

    if request.method == 'POST':
        ciudad.nombre_ciudad = request.form['nombre']
        ciudad.editar()
        return redirect(url_for('ciudades'))

    return render_template('editarCiudad.html', ciudad=ciudad)

@app.route('/eliminarCiudad/<int:id>', methods=['GET', 'POST'])
def eliminarCiudad(id):
    ciudad = Ciudad().consultaIndividual(id)
    if not ciudad:
        return "Ciudad no encontrada", 404

    if request.method == 'POST':
        Ciudad().eliminar(id)
        return redirect(url_for('ciudades'))

    return render_template('eliminarCiudad.html', ciudad=ciudad)

@app.route('/solicitud_adopcion/<int:mascota_id>', methods=['GET', 'POST'])
def solicitud_adopcion(mascota_id):
    usuario_id = 1
    
    mascota = Mascota().consultaIndividual(mascota_id)
    if not mascota:
        return "Mascota no encontrada", 404

    if request.method == 'POST':
        nueva_solicitud = SolicitudAdopcion()
        nueva_solicitud.id_usuario = usuario_id
        nueva_solicitud.id_mascota = mascota_id
        nueva_solicitud.estado = 'pendiente'
        nueva_solicitud.observaciones = request.form.get('observaciones', '')
        nueva_solicitud.agregar()
        return redirect(url_for('mis_solicitudes'))

    return render_template('solicitud_adopcion.html', mascota=mascota)

@app.route('/mis_solicitudes')
def mis_solicitudes():
    usuario_id = 1
    solicitud_obj = SolicitudAdopcion()
    mis_solicitudes = solicitud_obj.consultaPorUsuario(usuario_id)
    return render_template('mis_solicitudes.html', solicitudes=mis_solicitudes)

@app.route('/panel_solicitudes')
def panel_solicitudes():
    solicitud_obj = SolicitudAdopcion()
    todas_solicitudes = solicitud_obj.consultaGeneral()
    return render_template('panel_solicitudes.html', solicitudes=todas_solicitudes)

@app.route('/editarSolicitud/<int:id>', methods=['GET', 'POST'])
def editarSolicitud(id):
    solicitud = SolicitudAdopcion().consultaIndividual(id)
    if not solicitud:
        return "Solicitud no encontrada", 404

    if request.method == 'POST':
        solicitud.estado = request.form['estado']
        solicitud.observaciones = request.form.get('observaciones', '')
        solicitud.editar()
        
        if solicitud.estado == 'aceptada':
            mascota = Mascota().consultaIndividual(solicitud.id_mascota)
            mascota.estado = 'en proceso'
            mascota.editar()
            
        return redirect(url_for('panel_solicitudes'))

    return render_template('editarSolicitud.html', solicitud=solicitud)

@app.route('/eliminarSolicitud/<int:id>', methods=['GET', 'POST'])
def eliminarSolicitud(id):
    solicitud = SolicitudAdopcion().consultaIndividual(id)
    if not solicitud:
        return "Solicitud no encontrada", 404

    if request.method == 'POST':
        SolicitudAdopcion().eliminar(id)
        return redirect(url_for('panel_solicitudes'))

    return render_template('eliminarSolicitud.html', solicitud=solicitud)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)