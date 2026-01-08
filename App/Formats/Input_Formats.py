# Class defining the parsing process of human info
from pydantic import BaseModel,Field
from typing import Literal,Optional,List
from Literals import ASPECT_RATIO

# Class Defining the human input
class HumanInput(BaseModel):
    main_prompt: str = Field(..., description="The core mission of the campaign.")
    info_type : Literal["basic","advanced"] = Field(description="The type of input selected by user")
    # --- Brand & Product ---
    brand_name: Optional[str] = Field(default=None)
    product_name: Optional[str] = Field(default=None)
    brand_logo: Optional[str] = Field(default=None)
    
    # --- Visual Assets (0-3 constraints) ---
    product_reference_images: Optional[List[str]] = Field(
        default_factory=list, 
        max_items=3, 
        description="Up to 3 images of the product."
    )
    human_model_images: Optional[List[str]] = Field(
        default_factory=list, 
        max_items=3, 
        description="Up to 3 images for model/persona reference."
    )

    # --- Style & Format ---
    artistic_style: Optional[str] = Field(None, placeholder="e.g., Minimalist, Cyberpunk, Cinematic")
    aspect_ratio: ASPECT_RATIO = Field(
        default="1:1", 
        description="The target format for visual outputs."
    )

    # --- Marketing Strategy ---
    target_audience: Optional[str] = Field(
        default=None,
        description="The audience targeted by marketing campaign"
    )
    location: Optional[str] = Field(
        default=None,
        description="Geographic target (e.g., London, UK).")
    language: Optional[str] = Field(
        default=None,
        description="Primary campaign language.")

    # --- Suggested Added Fields ---
    negative_constraints: Optional[str] = Field(
        default=None, 
        description="What to AVOID (e.g., 'don't use the color red')."
    )
    call_to_action: Optional[str] = Field(
        default=None, 
        description="The primary button text or goal."
    )
    additional_information: Optional[str] = Field(
        default=None
    )

class Manager_Input(BaseModel):
    human_input:HumanInput = Field(
        description= "The input provided by the human that dictates the marketing campaign"
    )