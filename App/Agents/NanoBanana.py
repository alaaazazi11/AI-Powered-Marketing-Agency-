from Formats.MarketingAgency import MarketingAgencyState
from dotenv import load_dotenv
import os
from utils import run_nano_banana
from PIL import Image
import io
import base64


load_dotenv()

class NanoBananaAgent:
    def run(self,State:MarketingAgencyState) -> MarketingAgencyState :
        print("===== Running Nano Banana ======\n")
        
        print("Nano Banana System Message")

        run_nano_banana(State)
        image_url = f"http://127.0.0.1:8000/static/image.png" 
        
        updated_state = State.model_copy(
            update= {
                "gen_image_path" : image_url
            })
        print("===== Finished Running Nano Banana ======\n")
        return updated_state 
    