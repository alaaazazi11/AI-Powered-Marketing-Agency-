from pydantic import BaseModel,Field
from typing import Optional

class ColorDetail(BaseModel):
    """Encapsulates a colour's descriptive name and its technical Hex code."""
    descriptive_name: str = Field(
        description="A highly specific, evocative, and creative name for the colour (e.g., 'Deep Oxblood Red')."
    )
    hex_code: str = Field(
        description="The precise six-digit hexadecimal colour code, including the leading '#' (e.g., '#660000')."
    )

class Point(BaseModel):
    x : float = Field(
        description= "Horizontal position of the point normalized between (0-1), where 0 represents the left most point and 1 represent the right most point"
    )
    y : float = Field(
        description= "Vertical position of the point normalized between (0-1), where 0 represents the highest point and 1 represent the lowest point"
    )

class BoundingBox(BaseModel):
    min_point : Point = Field(
        description= "A point representing (x_min,y_min) used in creating a bounding box for a text element in a photo"
    )
    max_point : Point = Field(
        description= "A point representing (x_max,y_max) used in creating a bounding box for a text element in a photo"
    )

class TextAsset_CW(BaseModel):
    text_id : int = Field(
        description= "A unique identifier for the element"
    )
    text_type: str = Field(
        description="The function of this text in the image"
    )
    text_content: str = Field(
        description="The exact copy/text string content."
    )
    justification : str = Field(
        description= "Reasoning for the text used and its role in the image"
    )

class TextAsset_CT(BaseModel):
    text_id : int = Field(
        description= "A unique identifier for the element"
    )
    color_roles : str = Field(
        description= "The role of the used colors in the text"
    )
    fill_color: ColorDetail = Field(
        description= "The ColorDetail of the color used in filling the text"
    )
    outline_color: Optional[ColorDetail] = Field(
        default=None,
        description= "The ColorDetail used in outlinig the text"
    )
    text_gradient : Optional[str] = Field(
        default=None,
        description = "A short representation of how the gradient is supposed to look"
    )
    background_color:ColorDetail = Field(
        description="The background color of the text"
    )
    bg_opacity:float = Field(
        ge= 0.0,
        le=100.0,
        description= "The opacity of the background"
    )
    justification : str = Field(
        description= "The explanation of your chosen parameters"
    )

class TextAsset_LD(BaseModel):
    text_id : int = Field(
        description= "A unique identifier for the element"
    )

    bounding_box : BoundingBox = Field(
        description= "An axis-aligned bounding box, consisting of min_point and max_point normalized between 0-1, 0 is left most in x and highest in y and vice versa"
    )
    element_size : int = Field(
        ge = 16,
        le = 72,
        description= "The size of the text element in the image in pixels as described in css"
    )
    justification : str = Field(
        description= "Reasoning for the placement and size of this textual element"
    )

class TextAsset_FE(BaseModel):
    text_id : int = Field(
        description= "A unique identifier for the element"
    )
    font_name: str = Field(
        description="The specific font name for this text."
    )
    font_weight: str = Field(
        description="The font weight (e.g., 'Bold', 'Regular')."
    )
    justification : str = Field(
        description= "Reasoning for using this font and its weight and its role in the image created"
    ) 

class TextAsset_Final(BaseModel):
    text_id : int = Field(
        description= "A unique identifier for the element"
    )
    text_type: str = Field(
        description="The function of this text in the image"
    )
    text_content: str = Field(
        description="The exact copy/text string content."
    )
    color_roles : str = Field(
        description= "The role of the used colors in the text"
    )
    fill_color: ColorDetail = Field(
        description= "The ColorDetail of the color used in filling the text"
    )
    outline_color: Optional[ColorDetail] = Field(
        default= None,
        description= "The ColorDetail used in outlinig the text"
    )
    text_gradient : Optional[str] = Field(
        default=None,
        description = "A short representation of how the gradient is supposed to look"
    )
    
    bounding_box : BoundingBox = Field(
        description= "An axis-aligned bounding box, consisting of min_point and max_point normalized between 0-1, 0 is left most in x and lowest in y and vice versa"
    )
    element_size : int = Field(
        ge = 16,
        le = 72,
        description= "The size of the text element in the image in pixels as described in css"
    )
    font_name: str = Field(
        description="The specific font name for this text."
    )
    font_weight: str = Field(
        description="The font weight (e.g., 'Bold', 'Regular')."
    )
    layout_justification : str = Field(
        description= "Reasoning for the placement and size of this textual element"
    )
    cw_justification : str = Field(
        description= "Reasoning for the text used and its role in the image"
    )
    font_justification : str = Field(
        description= "Reasoning for using this font and its weight and its role in the image created"
    )
    ct_justification : str = Field(
        description= "Reasoning for using the colors and the role in the created image"
    )
    background_color:ColorDetail = Field(
        description="The background color of the text"
    )
    bg_opacity:float = Field(
        ge= 0.0,
        le=100.0,
        description= "The opacity of the background"
    )
    