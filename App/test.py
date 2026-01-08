from utils import run_nano_banana
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
load_dotenv()
# If your key is in the environment variable GEMINI_API_KEY, 
# you don't need to pass it here.
client = genai.Client(api_key="AIzaSyDLhbmTgK8sonQ1VO8ZnqUTxV-iv_tgukI")

prompt = """{
  "aspect_ratio": "4:5",
  "base_visual_concept": "A joyful and affectionate tear-free bathing experience with a happy child and caring mother in a bright, modern bathroom, emphasizing shiny, healthy hair.",
  "composition_synthesis": "4:5 aspect ratio, wide shot captured with a 50mm f/1.8 prime lens creating soft bokeh, utilizing the Rule of Thirds with mother and child occupying the left two-thirds of the frame, leaving negative space on the right for text.",
  "color_and_lighting_synthesis": "High-key lighting with soft, bright natural light casting a gentle, warm glow, minimal soft shadows, and soft, diffused highlights on wet, shiny hair and ethereal bubbles. The dominant color is Soft Sunshine Yellow (#FFFAD6) with playful accents of Sky Blue Whisper (#A7D9EE) and Blush Pink (#FFD1DC), creating a bright, joyful, and refreshing ambiance.",
  "style_and_texture_modifiers": "Realistic photography with a warm and bright aesthetic, high-quality 2K image.",
  "text_based_only_prompt": "The scene captures a heartwarming moment in a modern, pristine bathroom, bathed in abundant, soft natural light streaming from a large window. A happy child, approximately 3-5 years old, is the central focus, positioned prominently in the left two-thirds of the frame. Their face is radiant with pure joy, completely tear-free, and they are laughing heartily, splashing gently in a bathtub filled with clear water and rich, ethereal foam. The child's wet hair glistens, appearing thick, strong, and remarkably shiny, a testament to gentle care. Behind the child, their mother, 
in her late twenties to early thirties, leans in with an affectionate and reassuring smile, her hands gently washing the child's hair, her presence exuding warmth and comfort. The bathroom itself is clean and bright, featuring light-colored tiles, contributing to an overall sense of purity and serenity. Subtle, colorful bath toys are strategically placed, either floating playfully in the water or resting neatly on the tub's edge, enhancing the cheerful, childlike atmosphere without being distracting. The composition leaves significant negative space on the right side of the image. In the top-right quadrant, a primary text element is positioned. Directly below this, in the upper-middle section of the right-hand negative space, a secondary text element describing a key benefit is present. Finally, a call-to-action text element is placed in the bottom-right quadrant, clearly visible and encouraging 
engagement, completing the balanced visual narrative.",
  "negative_prompt_list": [
    "blurry",
    "distorted",
    "deformed hands",
    "watermark",
    "low quality",
    "blurry hands",
    "extra limbs",
    "distracting elements in the background",
    "unnatural water splashes",
    "ugly or sparse bubbles",
    "any text not explicitly provided in text_assets"
  ]
}
"""

response = client.models.generate_images(
    model='gemini-3-pro-image',
    prompt=prompt,
    config=types.ImageConfig(
        # The API explicitly separates these concepts
        aspect_ratio='16:9',
        # Set to False to prevent the model from "helping" by adding text context
        image_size= "1K" 
    )
    
)

response.generated_images[0].image.save("no_text_output.png")      
