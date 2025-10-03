import openai, glob, os

def send_to_chatgpt(folder):
    """Send all images in folder to ChatGPT and return result."""
    images = sorted(glob.glob(os.path.join(folder, "*.jpg")))
    if not images:
        return "No photos"

    image_inputs = [{"type": "image_url", "image_url": {"url": "file://" + f}} for f in images]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a vision model. Return a single word or number."},
            {"role": "user", "content": image_inputs}
        ]
    )
    return response.choices[0].message["content"].strip()
