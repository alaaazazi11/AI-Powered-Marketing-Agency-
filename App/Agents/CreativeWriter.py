from Formats.MarketingAgency import MarketingAgencyState
from dotenv import load_dotenv
import os
from utils import read_system_message,call_llm,get_input_message,parse_messages


load_dotenv()

class CreativeWriterAgent:
    def __init__(self,
                 temperature:float = 0.0):
        self.system_message = read_system_message("creative_writer")
        self.llm = call_llm("creative_writer",temperature,os.getenv("GOOGLE_API_KEY"))
    
    def run(self,State:MarketingAgencyState) -> MarketingAgencyState :
        print("===== Running Creative Writer ======\n")
        input_message = get_input_message("creative_writer",State)
        messages = parse_messages(self.system_message,input_message)
        llm_output = self.llm.invoke(messages)
        with open("creative_writer.json" , "w", encoding="utf-8") as f:
            data = llm_output.model_dump_json(indent = 2)
            f.write(data)
        updated_state = State.model_copy(
            update= {
                "messages" : [llm_output],
                "creative_writer_output" : [llm_output]
            })
        print("===== Finished Running Creative Writer ======\n")
        return updated_state 
