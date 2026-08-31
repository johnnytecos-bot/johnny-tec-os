from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-90b-vision-preview"


def is_available() -> bool:
    """Quick check that Groq is configured."""
    return bool(config.GROQ_API_KEY)


def reply_to_text(system_instruction: str, user_payload: str) -> str:
    """Generate a fast text reply using Groq."""
    completion = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_payload}
        ],
        temperature=0.4,
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content


def read_image(system_instruction: str, image_url: str, question: str) -> str:
    """Read and describe/answer about an image using Groq's vision model."""
    completion = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "system", "content": system_instruction},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        temperature=0.4
    )
    return completion.choices[0].message.content
  
