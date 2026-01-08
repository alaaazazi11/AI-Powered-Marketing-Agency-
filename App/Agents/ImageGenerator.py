from Formats.MarketingAgency import MarketingAgencyState
from dotenv import load_dotenv
import os
from utils import read_system_message,call_llm,get_input_message,parse_messages
load_dotenv()

class ImageGeneratorAgent:
    def __init__(self,temperature:float = 0.0):
        self.system_message = read_system_message("image_generator_system")
        self.llm = call_llm("image_generator_system",temperature,os.getenv("GOOGLE_API_KEY"))
        

    def run(self, State: MarketingAgencyState) -> MarketingAgencyState:
        print("===== Running Image Generator ======\n")
        input_message = get_input_message("image_generator_system", State)
        messages = parse_messages(self.system_message, input_message)
        llm_output = self.llm.invoke(messages)

        updated_state = State.model_copy(
            update={
                "messages": [llm_output],
                "image_generation_output": [llm_output]
            }
        )
        with open("prompt_state.json" , "w", encoding="utf-8") as f:
            data = llm_output.model_dump_json(indent=2)
            f.write(data)
        print("===== Finished Running Image Generator ======\n")
        return updated_state