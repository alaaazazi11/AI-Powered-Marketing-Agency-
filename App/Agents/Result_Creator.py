from Formats.MarketingAgency import MarketingAgencyState
from Formats.Output_Formats import FinalResultOutput
from dotenv import load_dotenv
import os
from utils import read_system_message,call_llm,get_input_message,parse_messages


load_dotenv()

class ResultAgent:
    def __init__(self,
                 temperature:float = 0.0):
        self.system_message = read_system_message("result")
        self.llm = call_llm("result",temperature,os.getenv("GOOGLE_API_KEY"))
    
    def run(self,State:MarketingAgencyState) -> MarketingAgencyState :
        print("===== Running Result Creator ======\n")
        input_message = get_input_message("result",State)
        messages = parse_messages(self.system_message,input_message)
        llm_output = self.llm.invoke(messages)
        result = FinalResultOutput(
            headline=llm_output.headline,
            body = llm_output.body,
            hashtags= llm_output.hashtags,
            image= rf"http://127.0.0.1:8000/static/image.png"
        )
        updated_state = State.model_copy(
            update= {
                "messages" : [llm_output],
                "result_output" : [result]
            })
        print("===== Finished Running Result Creator ======\n")
        return updated_state 


    
    