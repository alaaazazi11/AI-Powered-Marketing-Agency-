import os
from Formats.TextAssets import TextAsset_Final
from Formats.Input_Formats import HumanInput
from Formats.MarketingAgency import MarketingAgencyState
from langchain_google_genai import ChatGoogleGenerativeAI
from Formats.Output_Formats import ManagerOutput,CreativeWriterOutput,ColorTheoristOutput,FontExpertOutput,LayoutDesignerOutput,T2IPromptDesignerOutput,ImageGeneratorOutput,FeedbackOutput,ResultOutput
from Formats.Input_Formats import HumanInput
from typing import Literal, List,Optional
from Literals import ASPECT_RATIO
from langchain_core.messages import HumanMessage,SystemMessage
from PIL import Image
import json
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

def initialize_shared_state(user_request:str,
                            input_type:str = "Basic",
                            brand_name:Optional[str]= "",
                            product_name:Optional[str]= "",
                            brand_logo:Optional[str]= "",
                            product_reference_images:Optional[List[str]] = [""],
                            human_model_images:Optional[List[str]] = [""],
                            artistic_style:Optional[str]= "",
                            aspect_ratio:ASPECT_RATIO = "1:1",
                            target_audience:Optional[str]= "",
                            location:Optional[str]= "",
                            language:Optional[str]= "",
                            negative_constraints:Optional[str]= "",
                            call_to_action:Optional[str]= "",
                            additional_information:Optional[str] = ""
                            ) -> MarketingAgencyState :
    if input_type not in ["basic","advanced"]:
        pass
    else :
        human_input = HumanInput(main_prompt=user_request,info_type= input_type)
        initial_state = MarketingAgencyState(human_input=human_input)
        human_input == HumanInput(main_prompt= user_request,
                                  info_type=input_type,
                                  brand_name= brand_name,
                                  product_name= product_name,
                                  brand_logo=brand_logo,
                                  product_reference_images=product_reference_images,
                                  human_model_images= human_model_images,
                                  artistic_style= artistic_style,
                                  aspect_ratio=aspect_ratio,
                                  target_audience=target_audience,
                                  location=location,
                                  language=language,
                                  negative_constraints=negative_constraints,
                                  call_to_action=call_to_action,
                                  additional_information=additional_information)
    
    return initial_state

def read_system_message(agent_name:str):
    """
    Docstring for read_system_message
    A utility function that reads the system message according to the agent name
    :param agent_name: The name of the agent [manager,creative_writer,layout_designer,color_theorist,font_expert,t2i_prompt_designer,human_feedback_analyzer]
    :type agent_name: str
    """
    main_folder = ""
    system_messages = {
        "manager" : "manager.txt",
        "creative_writer" : "creative_writer.txt",
        "layout_designer" : "layout_designer.txt",
        "color_theorist" : "color_theorist.txt",
        "font_expert" : "font_expert.txt",
        "t2i_prompt_designer" : "t2i_prompt_designer.txt",
        "human_feedback_analyzer" : "human_feedback_analyzer.txt",
        "image_generator_system" : "imagegenerator.txt",
        "feedback"  : "feedback.txt",
        "result" : "result.txt"
    }
    message = None
    try:
        main_folder = "system_messages"
    except:
        return None
    message_name = system_messages[agent_name]
    file_path = os.path.join(main_folder,message_name)
    try :
        with open(file_path,"r",encoding="utf-8") as f:
            message = f.read()
            return message
    except:
        return None

def load_nano_banana( 
    api_key: str,
    # --- Image Physical Configs ---
    aspect_ratio: str = "1:1",          # "16:9", "9:16", "4:3", "3:2", "21:9"
    image_size: str = "1K",             # "1K", "2K", "4K" (Free tier usually 1K)
    mime_type: str = "image/png",       # "image/png", "image/jpeg", "image/webp"
    # --- Model Behavioral Configs ---
    enhance_prompt: bool = False,        # AI expansion of your prompt for quality
    person_generation: str = "allow_all",
    negative_prompt:str = "" # "allow_adult", "dont_allow"
):
    """
    Generates a high-fidelity image using Gemini 2.5 Flash Image (Nano Banana).

    This function wraps the Google Generative AI multimodal API. It processes 
    physical image constraints, behavioral randomness, and safety protocols 
    to return a ready-to-use PIL Image object.

    Args:
        api_key (str): Your Google AI Studio or Vertex AI API key.
        aspect_ratio (str): The width-to-height ratio. 
            Options: "1:1", "16:9", "9:16", "3:2", "2:3", "4:3", "3:4", "21:9", "5:4", "4:5".
        image_size (str): Target resolution. 
            Options: "1K" (Standard), "2K" (HD), "4K" (Ultra-HD/Pro only).
        mime_type (str): The image encoding format. 
            Options: "image/png", "image/jpeg", "image/webp".
        enhance_prompt (bool): If True, AI expands your prompt for better aesthetics.
        person_generation (str): Safety filter for drawing humans. 
            Options: "allow_adult", "dont_allow".

    Returns:
        PIL.Image.Image: The generated image object, or None if the request fails.
    """
    
    # 1. Initialize the model with physical image_configs
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-pro-image",
        google_api_key=api_key,
        image_config={
            "aspect_ratio": aspect_ratio,
            "image_size": image_size,
            "output_mime_type": mime_type,
            "person_generation": person_generation,
            "enhance_prompt": enhance_prompt,
            "negative_prompt":negative_prompt
        }
    )
    return llm

def run_nano_banana(state:MarketingAgencyState):
    

    # 1. Initialize the Client
    # It automatically looks for the GOOGLE_API_KEY environment variable
    folder_name = r"generated_content"
    image_name = "image.png"
    saved_file_path = os.path.join(folder_name,image_name)
    client = genai.Client(api_key="AIzaSyDLhbmTgK8sonQ1VO8ZnqUTxV-iv_tgukI")
    prompt = state.t2i_prompt_designer_output[-1].model_dump_json(indent=2)
    aspect = state.human_input.aspect_ratio
    
    print (f"Prompt : {prompt}")
    response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=
    types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio= aspect,
            image_size= "1K"
        )
    ))

# 4. Extract and save the image
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            # The SDK provides a helper to convert inline data directly to an image
            img = Image.open(BytesIO(part.inline_data.data))
            img.show()
            img.save(saved_file_path)
            

def call_llm(agent_name:str,temperature:float,api_key:str):
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        temperature = temperature,
        api_key = api_key
    )
    if agent_name == "manager":
        llm = llm.with_structured_output(ManagerOutput)
    elif agent_name == "creative_writer":
        llm = llm.with_structured_output(CreativeWriterOutput)
    elif agent_name == "color_theorist":
        llm = llm.with_structured_output(ColorTheoristOutput)
    elif agent_name == "layout_designer":
        llm = llm.with_structured_output(LayoutDesignerOutput)
    elif agent_name == "font_expert":
        llm = llm.with_structured_output(FontExpertOutput)
    elif agent_name == "t2i_prompt_designer":
        llm = llm.with_structured_output(T2IPromptDesignerOutput)
    elif agent_name == "human_feedback_analyzer":
        llm = llm.with_structured_output()
    elif agent_name == "image_generator_system":
        llm = llm.with_structured_output(ImageGeneratorOutput)
    elif agent_name == "feedback":
        llm = llm.with_structured_output(FeedbackOutput)
    elif agent_name == "result" :
        llm = llm.with_structured_output(ResultOutput)
        
    
    return llm

def parse_messages(system_message,input_message):
    messages = [
        SystemMessage(system_message),
        HumanMessage(input_message)
    ]
    return messages

def input_message_manager(state:MarketingAgencyState):
    the_input = state.human_input
    input_type = the_input.info_type
    message = ""
    if input_type == "basic" :
        message = f"User Prompt : {the_input.main_prompt}"
    elif input_type == "advanced" :
        message = f"""
        User Prompt : {the_input.main_prompt}\n
        Brand Name : {the_input.brand_name}\n
        Product Name : {the_input.product_name}\n
        Requested Artistic Style : {the_input.artistic_style}\n
        Requested Target Audience : {the_input.target_audience}\n
        Location : {the_input.location}\n
        Language : {the_input.language}\n
        Negative Constraints : {the_input.negative_constraints}\n
        Call To Action : {the_input.call_to_action}\n
        Additional Information : {the_input.additional_information}\n
        """
    return message

def input_message_creative_writer(state: MarketingAgencyState) -> str:
    """Extracts and formats data for the Creative Writer's prompt."""
    human = state.human_input
    manager = state.manager_output[-1]  # This is your ManagerOutput object

    goal = manager.project_goal
    brief = manager.detailed_brief
    target_audience = manager.target_audience
    platforms = ", ".join(manager.platform)

    brand_name = f"""{human.brand_name if human.brand_name else "Not Provided"}"""
    product = f"""{human.product_name if human.product_name else "Not Provided"}"""
    artistic_style = f"""{human.artistic_style if human.artistic_style else "Not Provided"}"""
    language = f"""{human.language if human.language else "Not Provided"}"""
    negative_constraints = f"""{" ".join(human.negative_constraints) if human.negative_constraints else "Not Provided"} """
    context = f"""
    ### Main User Prompt (From User)
    **User Request**: {human.main_prompt}
    ### STRATEGIC MANDATE (From Manager)
    - **Goal**: {goal}
    - **Brief**: {brief}
    - **Target Audience**: {target_audience}
    - **Platforms**: {platforms}
    ### RAW USER ASSETS & PREFERENCES
    - **Brand**: {brand_name}
    - **Product**: {product}
    - **Style Reference**: {artistic_style}
    - **Language**: {language}
    - **Negative Constraints**: {negative_constraints}
    
    ### VISUAL CONTEXT
    - **Logo Provided**: {'Yes' if human.brand_logo else 'No'}
    - **Ref Images Provided**: {"Yes" if human.product_reference_images else "No"}
    """
    return context

def input_message_layout_designer(state: MarketingAgencyState) -> str:
    text_assets = state.creative_writer_output[-1].text_assets
    text_as_str = ""
    if len(text_assets) == 0 or None :
        text_as_str = "Not provided"
    else :
        for text_asset in text_assets :
            text = f"""========== Text No :{text_asset.text_id} ==========
            Text Content : {text_asset.text_content}
Text Type : {text_asset.text_type}
CW Justification : {text_asset.justification}
==========
""" 
            text_as_str += text

    text_as_str += "\n"
    human = state.human_input
    manager = state.manager_output[-1]  # This is your ManagerOutput object
    creative = state.creative_writer_output[-1]

    goal = manager.project_goal
    brief = manager.detailed_brief
    target_audience = manager.target_audience
    platforms = ", ".join(manager.platform)

    brand_name = f"""{human.brand_name if human.brand_name else "Not Provided"}"""
    product = f"""{human.product_name if human.product_name else "Not Provided"}"""
    artistic_style = f"""{human.artistic_style if human.artistic_style else "Not Provided"}"""
    language = f"""{human.language if human.language else "Not Provided"}"""
    negative_constraints = f"""{" ".join(human.negative_constraints) if human.negative_constraints else "Not Provided"} """
    creative_as_text = creative.model_dump_json(indent=2)
    context = f"""
    ### Main User Prompt (From User)
    **User Request**: {human.main_prompt}
    ### STRATEGIC MANDATE (From Manager)
    - **Goal**: {goal}
    - **Brief**: {brief}
    - **Target Audience**: {target_audience}
    - **Platforms**: {platforms}
    ### RAW USER ASSETS & PREFERENCES
    - **Brand**: {brand_name}
    - **Product**: {product}
    - **Style Reference**: {artistic_style}
    - **Language**: {language}
    - **Negative Constraints**: {negative_constraints}
    
    ### VISUAL CONTEXT
    - **Logo Provided**: {'Yes' if human.brand_logo else 'No'}
    - **Ref Images Provided**: {"Yes" if human.product_reference_images else "No"}
    ### CREATIVE MANDATE (From Creative Writer)
    {creative_as_text}
    """
    text_as_str += context
    return text_as_str    

def input_message_color_theorist(state: MarketingAgencyState) -> str:
    human = state.human_input
    manager = state.manager_output[-1]  # This is your ManagerOutput object
    layout = state.layout_designer_output[-1]
    creative = state.creative_writer_output[-1]
    creative_as_text = creative.model_dump_json(indent=2)
    layout_as_text = layout.model_dump_json(indent = 2)


    goal = manager.project_goal
    brief = manager.detailed_brief
    target_audience = manager.target_audience
    platforms = ", ".join(manager.platform)

    brand_name = f"""{human.brand_name if human.brand_name else "Not Provided"}"""
    product = f"""{human.product_name if human.product_name else "Not Provided"}"""
    artistic_style = f"""{human.artistic_style if human.artistic_style else "Not Provided"}"""
    language = f"""{human.language if human.language else "Not Provided"}"""
    negative_constraints = f"""{" ".join(human.negative_constraints) if human.negative_constraints else "Not Provided"} """
    text = f"""
### Main User Prompt (From User)
    **User Request**: {human.main_prompt}
    ### STRATEGIC MANDATE (From Manager)
    - **Goal**: {goal}
    - **Brief**: {brief}
    - **Target Audience**: {target_audience}
    - **Platforms**: {platforms}
    ### RAW USER ASSETS & PREFERENCES
    - **Brand**: {brand_name}
    - **Product**: {product}
    - **Style Reference**: {artistic_style}
    - **Language**: {language}
    - **Negative Constraints**: {negative_constraints}
    ### VISUAL CONTEXT
    - **Logo Provided**: {'Yes' if human.brand_logo else 'No'}
    - **Ref Images Provided**: {"Yes" if human.product_reference_images else "No"}
    ### CREATIVE MANDATE (From Creative Writer)
    {creative_as_text}
    ### LAYOUT MANDATE (From Layout Designer)
    {layout_as_text}
"""
    text_assets = creative.text_assets
    text_as_str = ""
    if len(text_assets) == 0 or None :
        text_as_str = "Not provided"
    else :
        for text_asset in text_assets :
            text_as_str += f"""========== Text No :{text_asset.text_id} ==========
            Text Content : {text_asset.text_content}
Text Type : {text_asset.text_type}
CW Justification : {text_asset.justification}
"""
    text_assets = layout.text_assets
    if len(text_assets) == 0 or None :
        text_as_str = "Not provided"
    else :
        for text_asset in text_assets :
            text_as_str += f"""
            Element Size : {text_asset.element_size}
Bounding Box : {text_asset.bounding_box}
Justification : {text_asset.justification}
==========================
"""
    
    text += text_as_str
    return text

def input_message_font_expert(state:MarketingAgencyState) -> str:
    human = state.human_input
    manager = state.manager_output[-1]
    creative = state.creative_writer_output[-1]
    layout = state.layout_designer_output[-1]

    goal = manager.project_goal
    brief = manager.detailed_brief
    target_audience = manager.target_audience
    platforms = ", ".join(manager.platform)

    brand_name = f"""{human.brand_name if human.brand_name else "Not Provided"}"""
    product = f"""{human.product_name if human.product_name else "Not Provided"}"""
    artistic_style = f"""{human.artistic_style if human.artistic_style else "Not Provided"}"""
    language = f"""{human.language if human.language else "Not Provided"}"""
    negative_constraints = f"""{" ".join(human.negative_constraints) if human.negative_constraints else "Not Provided"} """
    text_as_str = ""
    text_assets = creative.text_assets
    if len(text_assets) == 0 or None :
        text_as_str = "Not provided"
    else :
        for text_asset in text_assets :
            text_as_str += f"""========== Text No :{text_asset.text_id} ==========
            Text Content : {text_asset.text_content}
Text Type : {text_asset.text_type}
CW Justification : {text_asset.justification}
"""
    text_assets = layout.text_assets
    if len(text_assets) == 0 or None :
        text_as_str = "Not provided"
    else :
        for text_asset in text_assets :
            text_as_str += f"""
            Element Size : {text_asset.element_size}
Bounding Box : {text_asset.bounding_box}
Justification : {text_asset.justification}
==========================
"""
    
    context = f"""
    ### Main User Prompt (From User)
    **User Request**: {human.main_prompt}
    ### STRATEGIC MANDATE (From Manager)
    - **Goal**: {goal}
    - **Brief**: {brief}
    - **Target Audience**: {target_audience}
    - **Platforms**: {platforms}
    ### RAW USER ASSETS & PREFERENCES
    - **Brand**: {brand_name}
    - **Product**: {product}
    - **Style Reference**: {artistic_style}
    - **Language**: {language}
    - **Negative Constraints**: {negative_constraints}
    ### VISUAL CONTEXT
    - **Logo Provided**: {'Yes' if human.brand_logo else 'No'}
    - **Ref Images Provided**: {"Yes" if human.product_reference_images else "No"}
    ### Creative Writer Recommendations
    - **Typograpghy style**: {creative.typography_style_recommendation}
    - **Tone of Voice** : {creative.tone_of_voice}
    - **Visual Style Mood** :{creative.visual_style_mood}
    ## Text assets : \n{text_as_str}

    """

    return context

def input_message_t2i(state:MarketingAgencyState) -> str :
    final_text = ""
    human = state.human_input
    manager = state.manager_output[-1]
    creative = state.creative_writer_output[-1]
    layout = state.layout_designer_output[-1]
    color = state.color_theorist_output[-1]
    text_assets = state.finalized_text_assets
    goal = manager.project_goal
    brief = manager.detailed_brief
    target_audience = manager.target_audience
    platforms = ", ".join(manager.platform)

    brand_name = f"""{human.brand_name if human.brand_name else "Not Provided"}"""
    product = f"""{human.product_name if human.product_name else "Not Provided"}"""
    artistic_style = f"""{human.artistic_style if human.artistic_style else "Not Provided"}"""
    language = f"""{human.language if human.language else "Not Provided"}"""
    negative_constraints = f"""{" ".join(human.negative_constraints) if human.negative_constraints else "Not Provided"} """

    context = f"""
    ### Main User Prompt (From User)
    **User Request**: {human.main_prompt}
    ### STRATEGIC MANDATE (From Manager)
    - **Goal**: {goal}
    - **Brief**: {brief}
    - **Target Audience**: {target_audience}
    - **Platforms**: {platforms}
    ### RAW USER ASSETS & PREFERENCES
    - **Brand**: {brand_name}
    - **Product**: {product}
    - **Style Reference**: {artistic_style}
    - **Language**: {language}
    - **Negative Constraints**: {negative_constraints}
    ### VISUAL CONTEXT
    - **Logo Provided**: {'Yes' if human.brand_logo else 'No'}
    - **Ref Images Provided**: {"Yes" if human.product_reference_images else "No"}
    ### Creative Writer Recommendations
    - **Typograpghy style**: {creative.typography_style_recommendation}
    - **Tone of Voice** : {creative.tone_of_voice}
    - **Visual Style Mood** :{creative.visual_style_mood}
    ### Color Theorist Recommendation
    {color.model_dump_json(indent=2)}
    ### Layout Designer Recommendation
    {layout.model_dump_json(indent=2)}
    """

    text_assets_as_str = ""
    if text_assets != None :
        if len(text_assets) != 0 :
            for text_asset in text_assets:
                text_assets_as_str += f"===== Text No : {text_asset.text_id} =====\n"
                text_assets_as_str += f"Text Content : {text_asset.text_content}\n"
                text_assets_as_str += f"Text Type : {text_asset.text_type}\n"
                text_assets_as_str += f"Color Role : {text_asset.color_roles}\n"
                text_assets_as_str += f"Fill Color : {text_asset.fill_color}\n" 
                text_assets_as_str += f"Outline Color : {text_asset.outline_color}\n"
                text_assets_as_str += f"Text Gradient : {text_asset.text_gradient}\n"
                text_assets_as_str += f"Text Bounding box : {text_asset.bounding_box}\n"
                text_assets_as_str += f"Text Font : {text_asset.font_name}\n"
                text_assets_as_str += f"Text Font Weight : {text_asset.font_weight}\n"
                text_assets_as_str += f"Text Size : {text_asset.element_size}\n"
                text_assets_as_str += "=========="
    
    final_text = context + text_assets_as_str
    return final_text
    
def input_message_image_generator(state: MarketingAgencyState) -> str:
    t2i = (
        state.t2i_prompt_designer_output[-1]
        if state.t2i_prompt_designer_output
        else None
    )

    if not t2i:
        raise RuntimeError(
            "ImageGeneratorAgent requires T2IPromptDesignerOutput in state"
        )

    negative_prompt = (
        ", ".join(t2i.negative_prompt_list)
        if t2i.negative_prompt_list
        else "None"
    )
    text_assets = state.finalized_text_assets
    text_assets_as_str = ""
    if text_assets != None :
        if len(text_assets) != 0 :
            for text_asset in text_assets:
                text_assets_as_str += f"===== Text No : {text_asset.text_id} =====\n"
                #text_assets_as_str += f"Text Content : {text_asset.text_content}\n"
                #text_assets_as_str += f"Text Type : {text_asset.text_type}\n"
                #text_assets_as_str += f"Color Role : {text_asset.color_roles}\n"
                #text_assets_as_str += f"Fill Color : {text_asset.fill_color}\n" 
                #text_assets_as_str += f"Outline Color : {text_asset.outline_color}\n"
                #text_assets_as_str += f"Text Gradient : {text_asset.text_gradient}\n"
                text_assets_as_str += f"Text Bounding box : {text_asset.bounding_box}\n"
                #text_assets_as_str += f"Text Font : {text_asset.font_name}\n"
                #text_assets_as_str += f"Text Font Weight : {text_asset.font_weight}\n"
                #text_assets_as_str += f"Text Size : {text_asset.element_size}\n"
                text_assets_as_str += "==========\n"

    text = f"""
### IMAGE GENERATION INPUT (T2I AUTHORITATIVE SOURCE)

## ASPECT RATIO
{t2i.aspect_ratio}

## BASE VISUAL CONCEPT
{t2i.base_visual_concept}

## COMPOSITION SYNTHESIS
{t2i.composition_synthesis}

## COLOR & LIGHTING SYNTHESIS
{t2i.color_and_lighting_synthesis}

## STYLE & TEXTURE MODIFIERS
{t2i.style_and_texture_modifiers}

## FINAL TEXT-TO-IMAGE PROMPT
{t2i.text_based_only_prompt}

## NEGATIVE PROMPT
{negative_prompt}
## TEXT ASSETS
{text_assets_as_str}

### EXECUTION RULES
- Use ONLY the information above.
- Do NOT reinterpret or creatively modify any section.
- Apply negative prompts strictly.
- Preserve visual hierarchy, lighting intent, and style fidelity.
- Generate a single high-quality image.
- Return ONLY valid ImageGeneratorOutput JSON.
"""

    return text
                
def input_message_feedback(state: MarketingAgencyState) -> str:
    human = state.human_input
    manager = state.manager_output[-1] if state.manager_output else None
    creative = state.creative_writer_output[-1] if state.creative_writer_output else None
    layout = state.layout_designer_output[-1] if state.layout_designer_output else None
    color = state.color_theorist_output[-1] if state.color_theorist_output else None
    font = state.font_expert_output[-1] if state.font_expert_output else None
    image = state.t2i_prompt_designer_output[-1] if state.t2i_prompt_designer_output else None

    # Serialize agent outputs safely
    creative_text = creative.model_dump_json(indent=2) if creative else "Not Provided"
    layout_text = layout.model_dump_json(indent=2) if layout else "Not Provided"
    color_text = color.model_dump_json(indent=2) if color else "Not Provided"
    font_text = font.model_dump_json(indent=2) if font else "Not Provided"
    image_text = image.model_dump_json(indent=2) if image else "Not Provided"

    # Manager context
    goal = manager.project_goal if manager else "Not Provided"
    brief = manager.detailed_brief if manager else "Not Provided"
    target_audience = manager.target_audience if manager else "Not Provided"
    platforms = ", ".join(manager.platform) if manager and manager.platform else "Not Provided"

    # Human inputs
    brand_name = human.brand_name if human and human.brand_name else "Not Provided"
    product = human.product_name if human and human.product_name else "Not Provided"
    language = human.language if human and human.language else "Not Provided"

    text = f"""
### MAIN USER REQUEST
User Prompt: {human.main_prompt if human else "Not Provided"}

### STRATEGIC CONTEXT (Manager)
Goal: {goal}
Brief: {brief}
Target Audience: {target_audience}
Platforms: {platforms}

### BRAND CONTEXT
Brand Name: {brand_name}
Product: {product}
Language: {language}

### AGENT OUTPUTS TO EVALUATE

--- Creative Writer Output ---
{creative_text}

--- Layout Designer Output ---
{layout_text}
--- Font Expert Output ---
{font_text}

--- Image Prompt Designer Output ---
{image_text}

### EVALUATION INSTRUCTIONS
- Evaluate each agent independently.
- Identify strengths, issues, and severity.
- Detect cross-agent conflicts.
- Provide actionable recommendations.
- Return ONLY valid FeedbackOutput JSON.
"""

    return text

def input_message_result(state: MarketingAgencyState) -> str :
    text = formatted_prompt = f"""
### CAMPAIGN CONTEXT & STRATEGY (Manager)
- **Project Goal:** {state.manager_output[-1].project_goal}
- **Detailed Brief:** {state.manager_output[-1].detailed_brief}
- **Target Audience:** {state.manager_output[-1].target_audience}
- **Suggested Platforms:** {", ".join(state.manager_output[-1].platform)}

---

### HUMAN CONSTRAINTS & BRAND INFO (Human)
- **Brand/Product:** {state.human_input.brand_name} - {state.human_input.product_name}
- **Main Mission:** {state.human_input.main_prompt}
- **Location & Language:** {state.human_input.location} | {state.human_input.language}
- **Artistic Style:** {state.human_input.artistic_style} ({state.human_input.aspect_ratio})
- **Negative Constraints (AVOID):** {state.human_input.negative_constraints or "None"}
- **Primary CTA:** {state.human_input.call_to_action}

---

### CREATIVE ASSETS (Creative Writer)
- **Tone & Emotion:** {state.creative_writer_output[-1].tone_of_voice} (Targeting: {", ".join(state.creative_writer_output[-1].target_emotions)})
- **Funnel Stage:** {state.creative_writer_output[-1].funnel_stage}
- **Headline Options:** {state.creative_writer_output[-1].headline_options}
- **Subheadlines:** {state.creative_writer_output[-1].subheadlines}
- **Body Paragraphs:** {state.creative_writer_output[-1].short_paragraphs}
- **Key Benefits:** {state.creative_writer_output[-1].product_benefit_statements}
- **Objection Handling:** {state.creative_writer_output[-1].objection_handling_line}
- **Suggested Hashtags:** {", ".join(state.creative_writer_output[-1].hashtags)}

---

### FINAL INSTRUCTION
Using the Creative Assets above, synthesize a single, cohesive advertisement that fulfills the Manager's Goal and adheres to the Human Constraints. 

Return your response in the following format:
**Headline:** [Selected/Refined Headline]
**Body:** [Combined Narrative Body Copy]
**Hashtags:** [Final List of 5 Hashtags]
"""
    return text

def get_input_message(agent_name : str,input_data):
    message = ""
    if agent_name == "manager":
        message = input_message_manager(input_data)
    elif agent_name == "creative_writer":
        message = input_message_creative_writer(input_data)
    elif agent_name == "color_theorist":
        message = input_message_color_theorist(input_data)
    elif agent_name == "layout_designer":
        message = input_message_layout_designer(input_data)
    elif agent_name == "font_expert":
        message = input_message_font_expert(input_data)
    elif agent_name == "t2i_prompt_designer":
        message = input_message_t2i(input_data)
    elif agent_name == "human_feedback_analyzer":
        message = ""
    elif agent_name == "feedback":
        message = input_message_feedback(input_data)
    elif agent_name == "image_generator_system":
        message = input_message_image_generator(input_data)
    elif agent_name == "result":
        message = input_message_result(input_data)
    
    return message

def accumalate_text_assets(state:MarketingAgencyState):
    cw_text = state.creative_writer_output[-1].text_assets
    ct_text = state.color_theorist_output[-1].text_assets
    ld_text = state.layout_designer_output[-1].text_assets
    fe_text = state.font_expert_output[-1].text_assets

    text_assets = None

    if (len(cw_text) == len(ct_text)) and (len(ct_text) == len(ld_text)) and (len(ld_text) == len(fe_text)) and (len(ct_text) != 0) :
        text_assets = []
        for i in range(len(ct_text)) :
            id = cw_text[i].text_id
            content = cw_text[i].text_content
            text_type = cw_text[i].text_type
            cw_justification = cw_text[i].justification
            color_role = ct_text[i].color_roles
            fill = ct_text[i].fill_color
            outline = ct_text[i].outline_color
            grad = ct_text[i].text_gradient
            justification = ct_text[i].justification
            bound = ld_text[i].bounding_box
            sze = ld_text[i].element_size
            font = fe_text[i].font_name
            weight = fe_text[i].font_weight
            ld_justification = ld_text[i].justification
            fe = fe_text[i].justification
            bg_color = ct_text[i].background_color 
            opacity = ct_text[i].bg_opacity


            text_asset = TextAsset_Final(text_id=id,
                                         text_type=text_type,
                                         text_content=content,
                                         color_roles=color_role,
                                         fill_color=fill,
                                         outline_color=outline,
                                         text_gradient=grad,
                                         bounding_box=bound,
                                         element_size=sze,
                                         font_name=font,
                                         font_weight=weight,
                                         layout_justification=ld_justification,
                                         cw_justification=cw_justification,
                                         font_justification=fe,
                                         ct_justification = justification,
                                         background_color=bg_color ,
                                         bg_opacity= opacity
                                         )
            text_assets.append(text_asset)        

    updated_state = state.model_copy(update={
        "finalized_text_assets" : text_assets
    })
    with open(r"generated_content\assets.json" , "w", encoding="utf-8") as f:
            my_list = []
            for i in range(len(updated_state.finalized_text_assets)) :
                my_list.append(updated_state.finalized_text_assets[i].model_dump(mode='json'))
            data = json.dumps(my_list)
            f.write(data)
    return updated_state

def is_approved(state:MarketingAgencyState) -> Literal['nano_banana','manager']:
    score = state.feedback_output[-1].overall_score
    if score >= 7.0:
        return "nano_banana"
    else:
        return "manager"