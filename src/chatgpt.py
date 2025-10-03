import os
import glob
import base64
from openai import OpenAI

def encode_image_to_data_url(image_path):
    """Read image and return a base64 data URL string"""
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"

def send_to_chatgpt(temp_dir):
    """
    Sends the last two images in temp_dir to ChatGPT and returns a text result.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment")

    client = OpenAI(api_key=api_key)

    images = sorted(glob.glob(os.path.join(temp_dir, "*.jpg")), key=os.path.getmtime)
    if len(images) < 2:
        return "Need at least 2 photos"

    last_two = images[-2:]
    print(f"[DEBUG] Sending last two images: {last_two}")

    content_parts = [
        {"type": "text", "text": "Analyze these images. If multiple choice, give the answer letter. If short answer, give the short answer. If blurry, return 'blurry'."}
    ]
    for img in last_two:
        data_url = encode_image_to_data_url(img)
        content_parts.append({"type": "image_url", "image_url": {"url": data_url}})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # vision + fast
        messages=[
            {"role": "system", "content": "You are a vision model analyzing English and Math questions. You may receive two photos: one with a prompt, one with answer choices. Return only the answer letter if multiple choice, or a short answer if not. If blurry, return 'blurry'."},
            {"role": "user", "content": content_parts}
        ],
        max_tokens=100
    )

    # Extract result safely
    msg_content = response.choices[0].message.content
    if isinstance(msg_content, list):
        # Sometimes it's split into content parts
        result = "".join([c.get("text", "") for c in msg_content])
    else:
        result = msg_content

    print(f"[DEBUG] ChatGPT result: {result}")
    return result.strip()