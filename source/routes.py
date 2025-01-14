from flask import Blueprint

from source.commands import admin_cli_bp
from source.webhook import webhook_bp
from source.swagger.swagger import SWAGGER_URL, swaggerui_blueprint
from source.transactions.transactions_views import transactions_bp
from source.users.users_views import users_bp

main_routes_bp = Blueprint('main_routes', __name__)


main_routes_bp.register_blueprint(transactions_bp)
main_routes_bp.register_blueprint(users_bp)
main_routes_bp.register_blueprint(admin_cli_bp)
main_routes_bp.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
main_routes_bp.register_blueprint(webhook_bp)
