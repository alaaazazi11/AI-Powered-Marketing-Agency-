from Formats.MarketingAgency import MarketingAgencyState
from dotenv import load_dotenv
import os
from utils import read_system_message,call_llm,get_input_message,parse_messages


load_dotenv()

class T2IPromptAgent:
    def __init__(self,
                 temperature:float = 0.0):
        self.system_message = read_system_message("t2i_prompt_designer")
        self.llm = call_llm("t2i_prompt_designer",temperature,os.getenv("GOOGLE_API_KEY"))
    
    def run(self,State:MarketingAgencyState) -> MarketingAgencyState :
        print("===== Running T2I Prompt Designer ======\n")
        input_message = get_input_message("t2i_prompt_designer",State)
        messages = parse_messages(self.system_message,input_message)
        llm_output = self.llm.invoke(messages)
        updated_state = State.model_copy(
            update= {
                "messages" : [llm_output],
                "t2i_prompt_designer_output" : [llm_output]
            })
        print("===== Finished Running T2I Prompt Designer ======\n")
        
        return updated_state 


    
    