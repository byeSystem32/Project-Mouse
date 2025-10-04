import os, glob, base64
from openai import OpenAI

def encode_image_to_data_url(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"

def send_to_chatgpt(temp_dir):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    images = sorted(glob.glob(os.path.join(temp_dir, "*.jpg")), key=os.path.getmtime)
    if len(images) < 2:
        return "Need at least 2 photos"

    last_two = images[-2:]
    print(f"[DEBUG] Sending last two images: {last_two}")

    content_parts = [
        {"type": "text", "text": "Analyze these two images. If multiple choice, return ONLY the answer letter. If short answer, return the short answer. If either image is blurry, unclear, or poor quality, return 'blurry' (do not guess)."}
    ]
    for img in last_two:
        content_parts.append({"type": "image_url", "image_url": {"url": encode_image_to_data_url(img)}})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a vision model analyzing English/Math questions from photos. Strict rule: if bad quality, return 'blurry'."},
            {"role": "user", "content": content_parts}
        ],
        max_tokens=20
    )

    msg_content = response.choices[0].message.content
    if isinstance(msg_content, list):
        result = "".join([c.get("text", "") for c in msg_content])
    else:
        result = msg_content

    print(f"[DEBUG] ChatGPT result: {result}")
    return result.strip()