from pydantic import BaseModel,Field
from typing import Sequence,Optional,List,Literal,Dict
from Literals import ASPECT_RATIO, RESOLUTION, AGENTS
from datetime import datetime, timezone
from Formats.TextAssets import TextAsset_CW,TextAsset_LD,TextAsset_CT,TextAsset_FE,TextAsset_Final

# Class defining the Color
class ColorDetail(BaseModel):
    """Encapsulates a colour's descriptive name and its technical Hex code."""
    descriptive_name: str = Field(
        description="A highly specific, evocative, and creative name for the colour (e.g., 'Deep Oxblood Red')."
    )
    hex_code: str = Field(
        description="The precise six-digit hexadecimal colour code, including the leading '#' (e.g., '#660000')."
    )

# Class defining the output from the Manager
class ManagerOutput(BaseModel):
    # --- Project Definition ---
    project_goal: str = Field(
        description="The high-level, concrete marketing objective (e.g., 'Generate awareness for new product X among young entrepreneurs')."
    )
    detailed_brief:str = Field(
        description= "The detailed plan of how to achieve the project goal"
    )
    target_audience: str = Field(
        description="A detailed description of the audience persona, including their key motivations and platforms."
    )
    platform :List[str] = Field(
        description= "A list of Social Media sites suggested to create our campaign on"
    )
    time_stamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Class defining the output from the Creative Writer
class CreativeWriterOutput(BaseModel):
    """
    Finalized output for the Creative Writer Agent, providing multiple creative options 
    and essential context for visual, compliance, and localization needs.
    """

    # 1. Core Messaging Layer
    headline_options: List[str] = Field(
        ..., description="10 Primary headline variations for the ad"
    )
    subheadlines: List[str] = Field(
        ..., description="10 Supporting line that reinforces the headline"
    )
    short_paragraphs: List[str] = Field(
        ..., description="5 Main body copies (2–3 sentences)"
    )
    product_benefit_statements: List[str] = Field(
        ..., description= "10 Clear functional and emotional product benefit"
    )
    value_propositions: List[str] = Field(
        ..., description="10 reasons why this product is better than alternatives"
    )
    calls_to_action: List[str] = Field(
        ..., description=" 5 Action-oriented instructions"
    )
    # 2. Emotional & Brand Voice Layer
    tone_of_voice: str = Field(
        ..., description="Overall communication tone"
    )
    emotional_hooks: List[str] = Field(
        ..., description="5 Emotionally compelling hook sentences"
    )
    target_emotions: List[str] = Field(
        ..., description="5 Primary emotions the ad should evoke"
    )
    emotion_icons: List[str] = Field(
        ..., description="Emotion icons (emojis) for the post"
    )
    language: str = Field(
        ..., description="Language of the copy"
    )
    # 3. Creative Direction Layer
    visual_style_mood: str = Field(
        ..., description="Overall visual mood and atmosphere"
    )
    mood_keywords: List[str] = Field(
        ..., description="10 Single-word visual mood descriptors"
    )
    subject_description_snippet: str = Field(
        ..., description="Extremely detailed description of what should appear visually"
    )
    narrative_prompt_snippet: str = Field(
        ..., description="Narrative flow (problem → solution → outcome)"
    )
    video_scene_descriptions: List[str] = Field(
        ..., description="2–3 high-level video scene descriptions"
    )
    visual_do_dont: Dict[str, List[str]] = Field(
        ..., description="Visual guidelines with 'do' and 'dont' lists"
    )
    # 4. Typography & Layout Guidance
    typography_style_recommendation: str = Field(
        ..., description="High-level typography guidance"
    )
    # 5. Platform & Distribution Layer
    hashtags: List[str] = Field(
        ..., description="Platform-optimized 10 hashtags"
    )
    caption_variants: Dict[str, str] = Field(
        ..., description="Caption variations (short, long, platform-specific)"
    )
    # 6. Marketing Strategy Layer
    campaign_objective: List[str] = Field(
        ..., description="5 Marketing objectives (awareness, consideration, conversion)"
    )
    funnel_stage: str = Field(
        ..., description="Customer funnel stage (TOF, MOF, BOF)"
    )
    objection_handling_line: List[str] = Field(
        ..., description="3 Lines addressing user hesitation"
    )
    key_message_hierarchy: List[str] = Field(
        ..., description="Priority order of key messages"
    )
    ab_testing_suggestions: str = Field(
        ..., description="Suggested A/B testing angles"
    )
    # 7. Compliance & Safety Layer
    legal_or_disclaimer_text: Optional[str] = Field(
        None, description="Legal disclaimer if required"
    )
    compliance_risk_level: Optional[str] = Field(
        None, description="Compliance sensitivity level"
    )
    # 8. Internal Quality Signals
    brand_voice_alignment_score: Optional[float] = Field(
        None, description="Brand voice alignment score (0–10)"
    )
    localization_notes: Optional[str] = Field(
        None, description="Cultural or regional adaptation notes"
    )
    text_assets:Optional[Sequence[TextAsset_CW]] = Field(
        description="A list of text elements that would be used in Image Generation"
    )
    decision_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

# Class defining the output from the Layout Designer
class LayoutDesignerOutput(BaseModel):
    Ad_Type : Literal ["visual-heavy","text-heavy","product-focused-shot","lifestyle-shot","teaser","balanced","brand-awareness-ad","call-to-action-ad"] = Field(
        description= "The nature and characteristics of the ad"
    )
    SubjectType : Literal["human","object","product","none"] = Field(
        description= "The main subject type "
    )
    image_type: str = Field(
        description="The medium of the image, e.g., 'Photograph', 'Digital Illustration', 'Oil Painting'."
    )
    aspect_ratio: ASPECT_RATIO = Field(
        description="The width-to-height ratio of the generated image."
    )
    image_resolution: RESOLUTION = Field(
        default="1K", 
        description="The resolution quality of the final output."
    )
    shot_type: str = Field(
        description="The photographic framing, e.g., 'Extreme Close-Up', 'Wide Shot', 'Birds-eye view'."
    )
    camera_lens_details: str = Field(
        description="Specific lens characteristics, e.g., '35mm wide-angle', '85mm f/1.8 prime lens'."
    )
    artistic_style: str = Field(
        description="The overall aesthetic direction, e.g., 'Cyberpunk', 'Minimalist', 'Baroque'."
    )
    subject_detailed_description: str = Field(
        description="A comprehensive description of the main person, object, or creature in the scene."
    )
    action_or_expression: str = Field(
        description="What the subject is doing or the emotion they are conveying, e.g., 'Running in fear', 'Smirking'."
    )
    environment_description: str = Field(
        description="The setting or background details, e.g., 'A misty pine forest at dawn'."
    )
    lighting_description: str = Field(
        description="The light source and quality, e.g., 'Golden hour sunlight', 'Harsh neon flickering'."
    )
    mood_description: str = Field(
        description="The emotional atmosphere, e.g., 'Melancholic', 'Energetic', 'Suspenseful'."
    )
    focus_and_key_details: str = Field(
        description="Specific elements to highlight or depth-of-field notes, e.g., 'Sharp focus on the eyes, blurred background'."
    )
    color_schema_description: str = Field(
        description="The dominant color palette, e.g., 'Monochromatic blue', 'Vibrant earth tones'."
    )
    composition_style: str = Field(
        description="How the image is framed, e.g., 'Rule of Thirds', 'Golden Spiral', 'Symmetrical'."
    )
    subject_prominence: str = Field(
        description="How much of the frame the subject occupies, e.g., 'Dominant foreground', 'Small silhouette in distance'."
    )
    negative_elements: List[str] = Field(
        description="A list of things to exclude from the image, e.g., ['text', 'extra limbs', 'blurry hands']."
    )
    text_assets : Optional[Sequence[TextAsset_LD]] = Field(
        description="A list of text elements that would be used in Image Generation"
    )
    decision_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

# Class defining the output from the Font Expert
class FontExpertOutput(BaseModel):
    text_assets: Optional[Sequence[TextAsset_FE]] = Field(
        description="The text elements font details"
    )
    decision_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class ColorTheoristOutput(BaseModel):
    """
    Output for the Color Theorist Agent, defining the visual mood, the primary 
    color palette, and assigning color/contrast to every text asset.
    """
    # --- Palette and Mood ---
    colour_scheme_type: str = Field(
        description="Descriptive name of the colour harmony or scheme (e.g., 'Complementary', 'Triadic', 'High-Contrast Complementary')."
    )
    dominant_hue: ColorDetail = Field(
        description="Main color covering the largest area, used for backgrounds or primary environment. This is the base color for contrast decisions."
    )
    accent_hue: Optional[ColorDetail] = Field(
        description="The secondary, high-impact color used for focal points, contrast, or the Call-to-Action background/product highlight."
    )
    supporting_hue: Optional[ColorDetail] = Field(
        description="Third neutral/tertiary color used for mid-tones and balancing the composition."
    )
    visual_mood_and_tone: str = Field(
        description="The specific, nuanced emotional or thematic effect the colours are intended to create (e.g., 'Eerie and Unsettling', 'Futuristic and Sterile')."
    )

    # --- Text Colors ---
    text_assets: Optional[Sequence[TextAsset_CT]] = Field(
        description="The complete list of TextAsset objects received from the Font Expert, now fully populated with the required 'text_color_hex' and 'outline_color_hex' fields, ensuring optimal contrast."
    )

    # --- Lighting & Environment ---
    light_and_shadow_role: str = Field(
        description="A detailed description of the recommended lighting style and how it interacts with the colours. Specify quality (hard/soft), direction, and colour temperature."
    )
    ambient_light_color: Optional[ColorDetail] = Field(
        default=None,
        description="Color of the ambient light affecting the entire scene. Influences overall mood, color blending, and text visibility."
    )
    shadow_intensity: Optional[str] = Field(
        default=None,
        description="Intensity of shadows in the scene (Soft, Medium, Hard). Affects contrast between text and background, and visual depth."
    )
    reflection_highlights: Optional[str] = Field(
        default=None,
        description="Description of reflective highlights or shiny surfaces. Impacts perception of colors, brightness, and material textures."
    )

    # --- Background & Secondary Elements ---
    background_color: Optional[ColorDetail] = Field(
        default=None,
        description="Primary color of the background."
    )
    background_texture_or_pattern: Optional[str] = Field(
        default=None,
        description="Description of background pattern, gradient, or texture. Influences readability of text and visual harmony."
    )
    # --- Prompting for Image Generation ---
    colour_prompt_snippet: str = Field(
        description="A rich, descriptive paragraph for the T2I model summarizing all primary color and lighting relationships."
    )
    contrast_guidelines: Optional[str] = Field(
        default=None,
        description="Specific rules to ensure optimal text-to-background contrast for all text elements, considering colors, brightness, and outline usage."
    )
    mood_instructions: Optional[str] = Field(
        default=None,
        description="Additional instructions guiding the overall mood, tone, and emotional effect of the color palette in the scene."
    )
    decision_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class T2IPromptDesignerOutput(BaseModel):
    """
    Output for the T2I Prompt Designer Agent. It synthesizes all previous creative 
    and technical inputs into final generative prompts and instructions.
    """
    
    # --- 1. Synthesized Prompt Sections ---
    aspect_ratio :ASPECT_RATIO = Field(
        default= "1:1",
        description= "The width-to-height ratio of the generated image taken for layout_output"
    )
    base_visual_concept: str = Field(
        description="The primary descriptive phrase covering the main subject(s) and action, derived from the Creative Writer's narrative and subject concept. Must be highly evocative."
    )  
    composition_synthesis: str = Field(
        description="A synthesis of the aspect ratio, camera angle, compositional style, and scene environment from the Layout Designer (e.g., '9:16 vertical ratio, low-angle shot, subject centered in a minimalist, concrete studio')."
    )
    color_and_lighting_synthesis: str = Field(
        description="A synthesis of the Color Theorist's output: lighting style, shadow behavior, and the dominant/accent colors (e.g., 'Dramatic low-key lighting, strong cool rim light, deep teal shadows and gold highlights, visual mood is unsettling and luxurious')."
    )
    style_and_texture_modifiers: str = Field(
        description="The aesthetic direction: medium, texture, and artistic style (e.g., 'Hyper-detailed cinematic photorealism, heavy film grain texture, Octane render, 8K, highly detailed')."
    )
    # --- 2. Final Generative Outputs (The Deliverable) ---
    text_based_only_prompt:str = Field(
        description="A world class text-to-image prompt for Nano Banana based on all given input structured in the best format for image generation"
    )
    negative_prompt_list: List[str] = Field(
        description="A list of specific undesirable elements to exclude from the generated image (e.g., 'blurry', 'distorted', 'deformed hands', 'watermark', 'low quality', 'text'), created from your best judgement in addition to layout_output negative prompts"
    )
    # finalized_text_assets: Optional[Sequence[TextAsset_Final]] = Field(
    #     default=None,
    #     description="The full list of finalized text assets"
    # )
    # decision_timestamp: Optional[datetime] = Field(
    #     default_factory=lambda: datetime.now(timezone.utc)
    # )

class ImageGeneratorOutput(BaseModel):
    image_prompt: str = Field(
        description="the prompt that will be used to create the image using nano banana pro"
    )
    aspect_ratio:ASPECT_RATIO = Field(
        description= "The aspect ratio of the photo"
    )
    image_size:RESOLUTION = Field(
        description= "The Resolution of the photo"
    )
    temperature:float = Field(
        default= 1.0,
        description= "The level of creativity to be used between 0.0 and 2.0 , Lower (0.1) is more literal and consistent. Higher (1.5+) is more artistic and unpredictable ",
        ge=0.0,
        le= 2.0
    ) 
    negative_prompts:str = Field(
        description= "The negative prompts that the model should avoid in generating the photo"
    )
    system_message:str = Field(
        description= "The system message for Nano Banana Pro to generate the content"
    )
    

    decision_timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )



class AgencyOutputFormat(BaseModel):
    pass



class Issue(BaseModel):
    issue: str = Field(
        description="A clear description of the identified problem or weakness."
    )
    severity: str = Field(
        description="The importance level of the issue. Expected values: 'minor', 'medium', or 'critical'."
    )
    suggestion: str = Field(
        description="An actionable recommendation to fix or reduce the impact of the issue."
    )


class AgentFeedback(BaseModel):
    score: float = Field(
        ge=0,
        le=10,
        description="Numerical evaluation of the agent's performance on a scale from 0 to 10."
    )
    strengths: List[str] = Field(
        description="List of key strengths or positive aspects observed in the agent's output."
    )
    issues: List[Issue] = Field(
        description="List of problems or weaknesses identified in the agent's output."
    )


class CrossAgentConflict(BaseModel):
    agents: List[AGENTS] = Field(
        description="Names or identifiers of agents involved in a disagreement or inconsistency."
    )
    issue: str = Field(
        description="Description of the conflict or contradiction between multiple agents."
    )
    severity: Literal["Minor","Medium","Critical"] = Field(
        description="Impact level of the conflict, such as 'minor', 'medium', or 'critical'."
    )


class Recommendation(BaseModel):
    agent: AGENTS = Field(
        description="The name or identifier of the agent receiving the recommendation."
    )
    suggestion: str = Field(
        description="Concrete advice or improvement suggestion for the specified agent."
    )


class FeedbackOutput(BaseModel):
    per_agent: Dict[AGENTS, AgentFeedback] = Field(
        description="Dictionary mapping each agent name to its corresponding feedback details."
    )
    cross_agent_conflicts: List[CrossAgentConflict] = Field(
        description="List of conflicts or inconsistencies detected between different agents."
    )
    overall_score: float = Field(
        ge=0,
        le=10,
        description="Overall system performance score aggregated from all agent evaluations."
    )
    recommendations: List[Recommendation] = Field(
        description="Final actionable recommendations derived from the evaluation process."
    )

class ResultOutput(BaseModel):
    headline : str = Field(
        description= "The headline of the post"
    )
    body : str = Field(
        description= "The body of the post"
    )
    hashtags : List[str] = Field(
        description= "The hashtags used for the post"
    )
    
class FinalResultOutput(BaseModel):
        headline : str
        body : str
        hashtags : List[str]
        image : str
        






