from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_login import LoginManager

from source.admin import init_admin, admin_cli_bp
from source.models import db, User
from source.transactions import transactions_bp
from source.users import users_bp
from source.settings import SettingsConfig


app = Flask(__name__, template_folder='source/templates')
app.config.from_object(SettingsConfig)

db.init_app(app)
with app.app_context():
    db.create_all()
init_admin(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'standard_test_case': "Transactions API"}
    )

app.register_blueprint(transactions_bp)
app.register_blueprint(users_bp)
app.register_blueprint(admin_cli_bp)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(debug=True)
