from supabase import create_client, Client
import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def get_contact_memory(contact_name: str) -> list:
    """Fetch all learned facts about a contact."""
    response = (
        supabase.table("contact_memories")
        .select("*")
        .eq("contact_name", contact_name)
        .execute()
    )
    return response.data


def save_memory(contact_name: str, learned_fact: str) -> None:
    """Store a new learned fact about a contact."""
    supabase.table("contact_memories").insert({
        "contact_name": contact_name,
        "learned_fact": learned_fact
    }).execute()


def get_conversation_history(contact_name: str, limit: int = 20) -> list:
    """Fetch recent chat history with a contact."""
    response = (
        supabase.table("chat_history")
        .select("*")
        .eq("contact_name", contact_name)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


def save_message(contact_name: str, role: str, content: str) -> None:
    """Save a message (incoming or outgoing) to chat history."""
    supabase.table("chat_history").insert({
        "contact_name": contact_name,
        "role": role,
        "content": content
    }).execute()
  
