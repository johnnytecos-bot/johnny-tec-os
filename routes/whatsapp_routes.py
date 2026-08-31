from flask import Blueprint, request, jsonify
import config
import orchestrator

whatsapp_bp = Blueprint("whatsapp", __name__)


@whatsapp_bp.route("/webhook/whatsapp", methods=["GET"])
def verify_webhook():
    """Meta calls this once to verify the webhook URL."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == config.WHATSAPP_VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


@whatsapp_bp.route("/webhook/whatsapp", methods=["POST"])
def receive_message():
    """Meta calls this every time a message/event comes in."""
    body = request.get_json()
    orchestrator.handle_whatsapp_message(body)
    return jsonify({"status": "received"}), 200
    
