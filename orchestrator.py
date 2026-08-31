import json
from services import whatsapp_service, supabase_service, vapi_service
from prompts.master_prompt import MASTER_PROMPT
import ai_router


def _build_user_payload(contact_name: str, message_content: str) -> str:
    """Bundle contact profile, memory, and history into one payload for the AI."""
    memory = supabase_service.get_contact_memory(contact_name)
    history = supabase_service.get_conversation_history(contact_name)

    payload = {
        "contact_profile": {"contact_name": contact_name},
        "known_memory": memory,
        "conversation_history": history,
        "new_incoming_event": {"type": "text", "content": message_content}
    }
    return json.dumps(payload)


def _apply_decision(contact_name: str, from_number: str, decision_raw: str) -> None:
    """Parse the AI's decision and act on it: save memory, reply, trigger call."""
    decision = json.loads(decision_raw)

    if decision.get("memory_updates"):
        supabase_service.save_memory(contact_name, decision["memory_updates"])

    if decision.get("trigger_call"):
        vapi_service.trigger_outbound_call(from_number, decision.get("call_reason", ""))

    reply = decision.get("reply_message")
    if reply:
        whatsapp_service.send_text_message(from_number, reply)
        supabase_service.save_message(contact_name, "assistant", reply)


def handle_whatsapp_message(webhook_body: dict) -> None:
    """Main entry point: process one incoming WhatsApp message end-to-end."""
    parsed = whatsapp_service.parse_incoming_message(webhook_body)
    if not parsed:
        return

    contact_name = parsed["contact_name"]
    from_number = parsed["from_number"]
    msg_type = parsed["type"]

    supabase_service.save_message(contact_name, "user", parsed.get("content", f"[{msg_type}]"))

    if msg_type == "text":
        user_payload = _build_user_payload(contact_name, parsed["content"])
        decision_raw = ai_router.route_text(MASTER_PROMPT, user_payload)

    elif msg_type == "image":
        media_url = whatsapp_service.get_media_url(parsed["media_id"])
        question = parsed.get("caption") or "Describe this image and respond appropriately."
        decision_raw = ai_router.route_image(MASTER_PROMPT, media_url, question)

    elif msg_type in ("document", "video"):
        media_url = whatsapp_service.get_media_url(parsed["media_id"])
        question = parsed.get("caption") or f"Read this {msg_type} and respond appropriately."
        if msg_type == "document":
            decision_raw = ai_router.route_document(MASTER_PROMPT, media_url, question)
        else:
            decision_raw = ai_router.route_video(MASTER_PROMPT, media_url, question)

    else:
        return

    _apply_decision(contact_name, from_number, decision_raw)


def handle_call_event(webhook_body: dict) -> None:
    """Main entry point: process a Vapi call event (e.g. after a call ends)."""
    parsed = vapi_service.parse_incoming_call_event(webhook_body)
    if not parsed:
        return

    contact_name = parsed["caller_number"]
    summary = parsed.get("summary", "")

    if summary:
        supabase_service.save_memory(contact_name, f"Call summary: {summary}")
      
