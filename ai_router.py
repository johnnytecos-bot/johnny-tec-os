from services import groq_service, gemini_service


def route_text(system_instruction: str, user_payload: str) -> str:
    """Text messages: Groq first (faster), Gemini as fallback."""
    if groq_service.is_available():
        return groq_service.reply_to_text(system_instruction, user_payload)
    if gemini_service.is_available():
        return gemini_service.reply_to_text(system_instruction, user_payload)
    raise RuntimeError("No AI provider available for text replies")


def route_image(system_instruction: str, file_ref: str, question: str) -> str:
    """Images: Groq first (can read images), Gemini as fallback."""
    if groq_service.is_available():
        return groq_service.read_image(system_instruction, file_ref, question)
    if gemini_service.is_available():
        return gemini_service.read_image(system_instruction, file_ref, question)
    raise RuntimeError("No AI provider available for image reading")


def route_document(system_instruction: str, file_path: str, question: str) -> str:
    """Documents: Gemini only capability - Groq can't read documents."""
    if gemini_service.is_available():
        return gemini_service.read_document(system_instruction, file_path, question)
    raise RuntimeError("Gemini is required to read documents but is not available")


def route_video(system_instruction: str, file_path: str, question: str) -> str:
    """Video: Gemini only capability - Groq can't read video."""
    if gemini_service.is_available():
        return gemini_service.read_video(system_instruction, file_path, question)
    raise RuntimeError("Gemini is required to read video but is not available")
