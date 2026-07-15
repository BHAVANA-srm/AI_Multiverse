import streamlit as st
import requests
import random
from urllib.parse import quote
import time

st.set_page_config(page_title="AI Image Generator", page_icon="🖼️")

st.title("🖼️ MY AI IMAGE GENERATOR")

st.sidebar.header("⚙️ SETTINGS")

art_style = st.sidebar.selectbox(
    "Select Desired Art Style",
    ["Photorealistic", "Anime", "Vintage Victorian", "Sketch", "3D Render"]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=768
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=768
)

# Magic Enhance
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

user_prompt = st.text_input("Describe the image you want to generate")

# Surprise prompts
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon reading books in a modern library",
    "A floating island with glowing waterfalls",
    "A futuristic underwater city"
]


def generate_image(prompt):
    full_prompt = f"{prompt}, {art_style}"

    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    # Encode prompt
    encoded_prompt = quote(full_prompt)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&seed={int(time.time())}"
    )

    with st.spinner("🎨 Rendering image..."):
        response = requests.get(url)

    if response.status_code == 200:

        # Check if response is an image
        if response.headers.get("Content-Type", "").startswith("image"):

            st.success("✅ Image Generated Successfully!")

            st.image(
                response.content,
                caption=full_prompt,
                use_container_width=True
            )

            st.download_button(
                label="📥 Download Image",
                data=response.content,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )

        else:
            st.error("The API returned something other than an image.")
            st.text(response.text)

    else:
        st.error(f"API Error: {response.status_code}")


# Generate button
if st.button("🎨 Generate Image"):
    if user_prompt.strip():
        generate_image(user_prompt)
    else:
        st.warning("Please enter a prompt.")


# Surprise Me button
if st.button("🎲 Surprise Me!"):
    random_prompt = random.choice(surprise_prompts)
    st.info(f"🎲 Prompt: {random_prompt}")
    generate_image(random_prompt)
