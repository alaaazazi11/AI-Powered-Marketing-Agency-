# #API Part:

# from fastapi import FastAPI, HTTPException
# from typing import Dict
# # Import Agents
# from Formats.Input_Formats import HumanInput
# from Formats.MarketingAgency import MarketingAgencyState
# from Agents.Manager import ManagerAgent
# from Agents.CreativeWriter import CreativeWriterAgent
# from Agents.LayoutDesigner import LayoutDesignerAgent
# from Agents.FontExpert import FontExpertAgent
# from Agents.ColorTheorist import ColorTheoristAgent
# from Agents.T2IPromptDesigner import T2IPromptAgent
# from utils import accumalate_text_assets
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="E3lank Marketing Agency")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],  
# )
# @app.post("/create_ad")
# async def create_ad(user_input: HumanInput):
#     state = MarketingAgencyState(human_input=user_input)
    
#     # 2.The Pipeline
#     try:
#         # Sequential Workflow
#         state = ManagerAgent().run(state)
#         state = CreativeWriterAgent().run(state)
#         state = LayoutDesignerAgent().run(state)
#         state = ColorTheoristAgent().run(state)
#         state = FontExpertAgent().run(state)
        
#         # 3. Utils
#         state = accumalate_text_assets(state)
        
#         # Final Prompt
#         state = T2IPromptAgent().run(state)
        

#         # 5. Link Prompt with the Image Agent
#         final_prompt = state.t2i_prompt_designer_output[-1].text_based_only_prompt
#         image_url = state.t2i_prompt_designer_output[-1].generated_image_url 

#         return {
#             "status": "Success",
#             "image_url": state.t2i_prompt_designer_output[-1].generated_image_url,
#             "design_details": state.finalized_text_assets

#         }
#     # 500 -> mean that the error doesnt happen from the sending data but from the server
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from Formats.Input_Formats import HumanInput
from Formats.MarketingAgency import MarketingAgencyState
from graph import myGraph

app = FastAPI(title="E3lank Marketing Agency")
cwd = os.getcwd()
print(os.path.join(cwd,'generated_content'))
OUTPUT_DIR = os.path.join(cwd,'generated_content')
app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")
app_graph = myGraph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.post("/create_ad")
async def create_ad(user_input: HumanInput):
    state = MarketingAgencyState(human_input=user_input)
    try:
        
        final_state = app_graph.run(state)
        result = final_state["result_output"][-1]
        headline = result.headline
        body = result.body
        hashtags = result.hashtags
        image = result.image
        

        return {"headline": headline or "Your AI Generated Headline",
            "body": body or "Your ad content is ready. Edit it as you like!",
            "hashtags": hashtags if hashtags else ["Innovation", "Marketing"],
            "imageUrl": image
        }
        

    except Exception as e:
        print(f"Error in Pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))