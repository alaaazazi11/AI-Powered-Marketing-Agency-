from Formats.MarketingAgency import MarketingAgencyState
from dotenv import load_dotenv
import os
from utils import read_system_message,call_llm,get_input_message,parse_messages


load_dotenv()

class FontExpertAgent:
    def __init__(self,
                 temperature:float = 0.0):
        self.system_message = read_system_message("font_expert")
        self.llm = call_llm("font_expert",temperature,os.getenv("GOOGLE_API_KEY"))
    
    def run(self,State:MarketingAgencyState) -> MarketingAgencyState :
        print("===== Running Font Expert ======\n")
        input_message = get_input_message("font_expert",State)
        messages = parse_messages(self.system_message,input_message)
        llm_output = self.llm.invoke(messages)
        updated_state = State.model_copy(
            update= {
                "messages" : [llm_output],
                "font_expert_output" : [llm_output]
            })
        print("=====Finished Running Font Expert ======\n")
        return updated_state 