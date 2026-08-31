from flask import Blueprint, jsonify
from datetime import datetime, timezone
import config
from services import supabase_service

status_bp = Blueprint("status", __name__)


@status_bp.route("/api/status", methods=["GET"])
def get_status():
    """Live health check of every connected service + basic usage stats."""

    services = {
        "backend": True,
        "supabase": bool(config.SUPABASE_URL and config.SUPABASE_KEY),
        "groq": bool(config.GROQ_API_KEY),
        "gemini": bool(config.GEMINI_API_KEY),
        "whatsapp": bool(
            config.WHATSAPP_TOKEN
            and config.WHATSAPP_PHONE_NUMBER_ID
            and config.WHATSAPP_VERIFY_TOKEN
        ),
        "vapi": bool(config.VAPI_API_KEY and config.VAPI_PHONE_NUMBER_ID),
    }

    messages_today = 0
    users_today = 0
    total_messages = 0

    if services["supabase"]:
        try:
            today_start = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00")

            today_rows = supabase_service.supabase.table("chat_history") \
                .select("contact_name", count="exact") \
                .gte("created_at", today_start) \
                .execute()

            messages_today = today_rows.count or 0
            users_today = len({row["contact_name"] for row in today_rows.data})

            all_rows = supabase_service.supabase.table("chat_history") \
                .select("id", count="exact") \
                .execute()
            total_messages = all_rows.count or 0
        except Exception:
            services["supabase"] = False

    return jsonify({
        "services": services,
        "stats": {
            "messages_today": messages_today,
            "users_today": users_today,
            "total_messages": total_messages
        }
    }), 200


@status_bp.route("/api/contacts", methods=["GET"])
def get_contacts():
    """List every contact who has messaged, with their most recent message."""
    try:
        rows = supabase_service.supabase.table("chat_history") \
            .select("contact_name, role, content, created_at") \
            .order("created_at", desc=True) \
            .execute()
    except Exception:
        return jsonify({"contacts": []}), 200

    seen = {}
    for row in rows.data:
        name = row["contact_name"]
        if name not in seen:
            seen[name] = {
                "contact_name": name,
                "last_message": row["content"],
                "last_role": row["role"],
                "last_timestamp": row["created_at"]
            }

    return jsonify({"contacts": list(seen.values())}), 200


@status_bp.route("/api/contacts/<contact_name>/messages", methods=["GET"])
def get_contact_messages(contact_name):
    """Full chat history for one contact, oldest first."""
    try:
        rows = supabase_service.supabase.table("chat_history") \
            .select("role, content, created_at") \
            .eq("contact_name", contact_name) \
            .order("created_at", desc=False) \
            .execute()
        return jsonify({"messages": rows.data}), 200
    except Exception:
        return jsonify({"messages": []}), 200
        
