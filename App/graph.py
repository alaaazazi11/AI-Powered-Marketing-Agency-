from Agents.ColorTheorist import ColorTheoristAgent
from Agents.CreativeWriter import CreativeWriterAgent
from Agents.FontExpert import FontExpertAgent
from Agents.LayoutDesigner import LayoutDesignerAgent
from Agents.Manager import ManagerAgent
from Agents.T2IPromptDesigner import T2IPromptAgent
from Agents.ImageGenerator import ImageGeneratorAgent
from Agents.NanoBanana import NanoBananaAgent
from Agents.FeedbackAgent import FeedbackAgent
from Agents.Result_Creator import ResultAgent
from Formats.MarketingAgency import MarketingAgencyState
from utils import initialize_shared_state,accumalate_text_assets,is_approved

from langgraph.graph import StateGraph,START,END

class myGraph:
    def __init__(self):
        # Creating Agents
        print("========== Initializing Graph ==========")
        self.manager = ManagerAgent(temperature= 1)
        self.creativewriter = CreativeWriterAgent(temperature= 1)
        self.layoutdesigner = LayoutDesignerAgent(temperature= 1)
        self.colortheorist = ColorTheoristAgent(temperature=1)
        self.fontexpert = FontExpertAgent(temperature = 1)
        self.t2ipromptdesigner = T2IPromptAgent(temperature = 1)
        #self.image_generator = ImageGeneratorAgent(temperature= 1)
        self.nano_banana = NanoBananaAgent()
        self.feedback_agent = FeedbackAgent(temperature=1)
        self.result_agent = ResultAgent(temperature= 1)
        
        self.builder = StateGraph(MarketingAgencyState)
        
        self.builder.add_node("manager",self.manager.run)
        self.builder.add_node("creative_writer",self.creativewriter.run)
        self.builder.add_node("layout_designer",self.layoutdesigner.run)
        self.builder.add_node("color_theorist",self.colortheorist.run)
        self.builder.add_node("font_expert",self.fontexpert.run)
        self.builder.add_node("combine_textassets",accumalate_text_assets)
        self.builder.add_node("prompt_designer",self.t2ipromptdesigner.run)
        #self.builder.add_node("image_generator",self.image_generator.run)
        self.builder.add_node("feedback",self.feedback_agent.run)
        self.builder.add_node("is_approved",is_approved)
        self.builder.add_node("nano_banana",self.nano_banana.run)
        self.builder.add_node('result',self.result_agent.run)


        self.builder.add_edge(START,"manager")
        self.builder.add_edge("manager","creative_writer")
        self.builder.add_edge("creative_writer","layout_designer")
        self.builder.add_edge("layout_designer","color_theorist")
        self.builder.add_edge("color_theorist","font_expert")
        self.builder.add_edge("font_expert","combine_textassets")
        self.builder.add_edge("combine_textassets","prompt_designer")
        self.builder.add_edge("prompt_designer","feedback")
        #self.builder.add_edge("image_generator","feedback")
        self.builder.add_conditional_edges("feedback",
                                           is_approved,
                                           {"manager" : "manager" ,
                                            "nano_banana" : "nano_banana" 
                                            })
        self.builder.add_edge('nano_banana','result')
        self.builder.add_edge('result',END)
        
        self.graph = self.builder.compile()
        print("========== Finished Initializing Graph ==========")

    def run(self,state):
        return self.graph.invoke(state)






