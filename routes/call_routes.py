from flask import Blueprint, request, jsonify
import orchestrator

call_bp = Blueprint("call", __name__)


@call_bp.route("/webhook/call", methods=["POST"])
def receive_call_event():
    """Vapi calls this on call events (start, end, transcript, etc)."""
    body = request.get_json()
    orchestrator.handle_call_event(body)
    return jsonify({"status": "received"}), 200
  
