from app import create_app, db
from app.models import Role

app = create_app()

with app.app_context():
    db.create_all()
    if Role.query.count() == 0:
        user_role = Role(name='user')
        admin_role = Role(name='admin')
        db.session.add(user_role)
        db.session.add(admin_role)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
