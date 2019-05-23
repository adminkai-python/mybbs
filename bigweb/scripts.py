from bigweb.extensions import db
from bigweb import create_app
from bigweb.models import Role

app = create_app('development')

with app.app_context():
    db.drop_all()
    db.create_all()
    Role.init_role()

