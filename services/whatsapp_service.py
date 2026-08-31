import requests
import config

BASE_URL = f"https://graph.facebook.com/v20.0/{config.WHATSAPP_PHONE_NUMBER_ID}/messages"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {config.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }


def send_text_message(to_number: str, message: str) -> dict:
    """Send a plain text reply to a WhatsApp number."""
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(BASE_URL, headers=_headers(), json=payload)
    response.raise_for_status()
    return response.json()


def get_media_url(media_id: str) -> str:
    """Given a media ID from an incoming message, get the downloadable URL."""
    url = f"https://graph.facebook.com/v20.0/{media_id}"
    response = requests.get(url, headers=_headers())
    response.raise_for_status()
    return response.json().get("url")


def download_media(media_url: str) -> bytes:
    """Download the actual media file (image/document/video) bytes."""
    response = requests.get(media_url, headers=_headers())
    response.raise_for_status()
    return response.content


def parse_incoming_message(webhook_body: dict) -> dict | None:
    """Extract the useful bits from a WhatsApp webhook payload."""
    try:
        entry = webhook_body["entry"][0]
        change = entry["changes"][0]["value"]

        if "messages" not in change:
            return None

        message = change["messages"][0]
        contact_name = change["contacts"][0]["profile"]["name"]
        from_number = message["from"]
        msg_type = message["type"]

        parsed = {
            "contact_name": contact_name,
            "from_number": from_number,
            "type": msg_type
        }

        if msg_type == "text":
            parsed["content"] = message["text"]["body"]
        elif msg_type in ("image", "document", "video"):
            parsed["media_id"] = message[msg_type]["id"]
            parsed["caption"] = message[msg_type].get("caption", "")

        return parsed
    except (KeyError, IndexError):
        return None
