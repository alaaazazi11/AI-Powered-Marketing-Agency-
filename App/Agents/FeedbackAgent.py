from Formats.MarketingAgency import MarketingAgencyState
from dotenv import load_dotenv
import os
from utils import read_system_message,call_llm,get_input_message,parse_messages


load_dotenv()
class  FeedbackAgent: 
    def __init__(self,temperature:float = 0.0):
        self.system_message = read_system_message("feedback")
        self.llm = call_llm("feedback",temperature,os.getenv("GOOGLE_API_KEY"))
    
    def run(self, State: MarketingAgencyState) -> MarketingAgencyState:
        print("===== Running Feedback Agent ======\n")
        input_message = get_input_message("feedback", State)

        messages = parse_messages(
            self.system_message,
            input_message
        )

        feedback = self.llm.invoke(messages)

        updated_state = State.model_copy(
            update={
                "messages":  [feedback],
                "feedback_output": [feedback]
            }
        )
        print("===== Finished Running Feedback Agent ======\n")

        return updated_state