from flask import Flask
from flask_login import LoginManager

from source.admin.admin_views import init_admin
from source.models import User, db
from source.routes import main_routes_bp
from source.settings import SettingsConfig

app = Flask(__name__, template_folder='source/templates')
app.config.from_object(SettingsConfig)

with app.app_context():
    db.init_app(app)
    db.create_all()
    init_admin(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(main_routes_bp)


if __name__ == '__main__':
    app.run(debug=True)
