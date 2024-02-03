from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role_name != 'admin':
            flash('You do not have permission to view this page.', 'danger')
            return redirect(
                url_for('main.index'))  # Предполагается, что 'main.index' - это endpoint для главной страницы
        return f(*args, **kwargs)

    return decorated_function
