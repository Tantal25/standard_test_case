from flask import Blueprint, request


webhook_bp = Blueprint('webhooks', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"======  Received webhook: {data}  ======")
    return '', 200
