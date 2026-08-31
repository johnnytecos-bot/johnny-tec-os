import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def is_available() -> bool:
    """Quick check that Gemini is configured."""
    return bool(config.GEMINI_API_KEY)


def reply_to_text(system_instruction: str, user_payload: str) -> str:
    """Generate a text reply using Gemini (used when Groq is down)."""
    response = model.generate_content(
        [system_instruction, user_payload],
        generation_config={"temperature": 0.4}
    )
    return response.text


def read_document(system_instruction: str, file_path: str, question: str) -> str:
    """Read and answer questions about a document (pdf, docx, etc.)."""
    uploaded_file = genai.upload_file(file_path)
    response = model.generate_content(
        [system_instruction, uploaded_file, question],
        generation_config={"temperature": 0.4}
    )
    return response.text


def read_video(system_instruction: str, file_path: str, question: str) -> str:
    """Read and answer questions about a video."""
    uploaded_file = genai.upload_file(file_path)
    response = model.generate_content(
        [system_instruction, uploaded_file, question],
        generation_config={"temperature": 0.4}
    )
    return response.text


def read_image(system_instruction: str, file_path: str, question: str) -> str:
    """Read and answer questions about an image."""
    uploaded_file = genai.upload_file(file_path)
    response = model.generate_content(
        [system_instruction, uploaded_file, question],
        generation_config={"temperature": 0.4}
    )
    return response.text
