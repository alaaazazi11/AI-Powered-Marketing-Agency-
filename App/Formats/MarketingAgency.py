from typing import List,Annotated,Optional,Any
from pydantic import BaseModel,Field
from Formats.Input_Formats import HumanInput
from Formats.Output_Formats import ManagerOutput,CreativeWriterOutput,LayoutDesignerOutput,FontExpertOutput,ColorTheoristOutput,T2IPromptDesignerOutput,ImageGeneratorOutput,FinalResultOutput
from Formats.TextAssets import TextAsset_Final
import operator
from PIL import Image
class MarketingAgencyState(BaseModel):
    
    human_input : HumanInput
    messages : Annotated[List[BaseModel],operator.add] = []

    manager_output : Optional[Annotated[List[ManagerOutput],operator.add]] = Field(default_factory=list)
    creative_writer_output : Optional[Annotated[List[CreativeWriterOutput],operator.add]] = Field(default_factory=list)
    layout_designer_output : Optional[Annotated[List[LayoutDesignerOutput],operator.add]] = Field(default_factory=list)
    font_expert_output : Optional[Annotated[List[FontExpertOutput],operator.add]] = Field(default_factory=list)
    color_theorist_output : Optional[Annotated[List[ColorTheoristOutput],operator.add]] = Field(default_factory=list)
    t2i_prompt_designer_output : Optional[Annotated[List[T2IPromptDesignerOutput],operator.add]] = Field(default_factory=list)
    image_generation_output: Optional[Annotated[List[ImageGeneratorOutput],operator.add]] = Field(default_factory=list)
    result_output: Optional[Annotated[List[FinalResultOutput],operator.add]] = Field(default_factory=list)
    feedback_output: Optional[Annotated[List[Any],operator.add]] = Field(
        default_factory=list,
        description="The output from Feedback Agent")
    finalized_text_assets : Optional[List[TextAsset_Final]] = Field(
        default_factory=list,
        description="A list of text that is written on produced image")
    gen_image_path : Optional[str] = Field(
        default=None,
        description="The path of the generated image"
    )

    




