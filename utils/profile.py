from flask import redirect, session, url_for, flash
from functools import wraps

def profile_required(profiles):
    def decorator(view):
        @wraps(view)
        def decorated_view(*args, **kwargs):
            usuario = session.get('usuario')
            if usuario and usuario['perfil'] in profiles:
                return view(*args, **kwargs)
            else:
                flash('No tienes permiso para acceder a este recurso', 'danger')
                return redirect(url_for('index'))
        return decorated_view
    return decorator