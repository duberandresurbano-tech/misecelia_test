from flask import Blueprint, flash, redirect, render_template, request, session, url_for

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
            # (Asumiendo que tu relación en el modelo se llama .roles y cada rol tiene .nombre)
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
