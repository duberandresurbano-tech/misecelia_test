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

        # Crear el nuevo administrador
        hash_pass = generate_password_hash(password)
        nuevo_admin = Usuario(
            nombre=nombre,
            usuario_acceso=usuario_acceso,
            hash_contrasena=hash_pass,
            estado=True
        )

        db.session.add(nuevo_admin)
        db.session.commit()
        
        flash('¡Administrador registrado con éxito! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/registro.html')