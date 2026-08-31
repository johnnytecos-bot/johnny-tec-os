import requests
import config

BASE_URL = "https://api.vapi.ai"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {config.VAPI_API_KEY}",
        "Content-Type": "application/json"
    }


def trigger_outbound_call(phone_number: str, reason: str) -> dict:
    """Trigger an outbound voice call via Vapi."""
    payload = {
        "phoneNumberId": config.VAPI_PHONE_NUMBER_ID,
        "customer": {"number": phone_number},
        "assistant": {
            "firstMessage": f"Hi, this is Johnny TEC OS calling. {reason}"
        }
    }
    response = requests.post(f"{BASE_URL}/call", headers=_headers(), json=payload)
    response.raise_for_status()
    return response.json()


def parse_incoming_call_event(webhook_body: dict) -> dict | None:
    """Extract the useful bits from a Vapi call webhook event."""
    try:
        message = webhook_body.get("message", {})
        event_type = message.get("type")

        if event_type != "end-of-call-report":
            return None

        return {
            "call_id": message.get("call", {}).get("id"),
            "caller_number": message.get("call", {}).get("customer", {}).get("number"),
            "summary": message.get("summary", ""),
            "transcript": message.get("transcript", "")
        }
    except (KeyError, AttributeError):
        return None
      
