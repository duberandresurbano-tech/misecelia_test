from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = Usuario.query.filter_by(usuario_acceso=username).first()

        if user and user.estado and user.verificar_password(password):
            session.clear()  # evita reutilizar una sesión anterior
            session['usuario_id'] = user.id_usuario
            session['usuario_acceso'] = user.usuario_acceso
            session['nombre_usuario'] = user.nombre

            # --- AGREGAMOS LOS ROLES DEL USUARIO A LA SESIÓN ---
            session['roles'] = [rol.nombre for rol in user.roles]

            flash('¡Bienvenido a Miscelia!', 'success')
            return redirect(url_for('main.dashboard'))

        flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        usuario_acceso = request.form.get('usuario_acceso', '').strip()
        password = request.form.get('password', '')

        if not nombre or not usuario_acceso or not password:
            flash('Por favor completa todos los campos.', 'danger')
            return render_template('auth/registro.html')

        # Validar si el usuario ya existe
        existente = Usuario.query.filter_by(usuario_acceso=usuario_acceso).first()
        if existente:
            flash('¡El usuario de acceso ya está registrado!', 'danger')
            return render_template('auth/registro.html')

        # Crear el nuevo usuario (administrador inicial) sin depender de campos de texto obsoletos
        nuevo_admin = Usuario(
            nombre=nombre,
            usuario_acceso=usuario_acceso,
            estado=True
        )
        
        # Aplicar el cifrado Argon2 usando el método del modelo
        nuevo_admin.establecer_password(password)

        # --- ASIGNACIÓN RELACIONAL DEL ROL ---
        # Buscamos el rol 'Administrador' en la tabla roles que sembramos previamente
        from app.models.usuario import Rol # Asegúrate de importar Rol si no está arriba
        rol_admin = Rol.query.filter_by(nombre='Administrador').first()
        
        if rol_admin:
            # Esto inserta automáticamente la relación en la tabla puente 'usuario_rol'
            nuevo_admin.roles.append(rol_admin)
        else:
            flash('Error crítico: El rol de Administrador no está inicializado en la BD.', 'danger')
            return render_template('auth/registro.html')

        db.session.add(nuevo_admin)
        db.session.commit()
        
        flash('¡Administrador registrado con éxito! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/registro.html')