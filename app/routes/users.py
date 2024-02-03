from flask import Blueprint, render_template, request

from app.models import User
from app.validation.roles import admin_required

users = Blueprint('users', __name__)


@users.route('/users')
@admin_required
def users_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('users.html', users=users.items, pagination=users)
