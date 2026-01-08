# E3lank-NTI-Graduation-Project
A Multi Agent Marketing Agency used to imitate real life marketing team to create social media posts, created as a graduation project for NTI's HireReady 4 Months program - Round 12



# 🎨 E3lank Marketing Agency: Multi-Agent System

**An Autonomous, AI-Powered Creative Agency orchestrated by LangGraph and Gemini.**

This project implements a sophisticated Multi-Agent System (MAS) that simulates a full-service marketing agency workflow. Using **LangGraph** for state management and **Google Gemini** as the cognitive engine, specialized AI agents collaborate to plan, write, design, and generate professional marketing assets from a simple human brief.

## 🚀 Overview

The system operates as a Directed Cyclic Graph (DAG), meaning agents pass work forward, but quality control can send it backward for revision.

* **Autonomous Collaboration:** Seven distinct agents work in sequence to build a cohesive ad campaign.
* **Iterative Refinement:** A "Feedback Agent" acts as a Creative Director. If the output quality score is below **7.0**, the system automatically loops back to the Manager to refine the strategy and assets.
* **Multi-Modal Output:** Generates not just text (headlines/hashtags) but also renders final visual assets via a local generation engine.

## 🏗 Architecture & Workflow

The system is built on **FastAPI** for the interface and **LangGraph** for the logic. The workflow proceeds as follows:

1. **Brief Intake**: The user submits a brand, topic, and channel via the API.
2. **Strategy Phase**:
* **Manager**: Analyzes the request to define the "Persona," "Goal," and "Target Audience".


3. **Creative Phase**:
* **Creative Writer**: Drafts the "Creative Bible" containing headlines and body copy.
* **Layout Designer**: Calculates spatial composition and bounding boxes for elements.
* **Color Theorist**: Applies color psychology to select a palette (Hex codes) matching the emotion.
* **Font Expert**: Selects typography that bridges the brand identity with the layout constraints.


4. **Synthesis Phase**:
* **T2I Prompt Designer**: Compiles all previous creative decisions into a highly technical Text-to-Image prompt.
* **Image Generator**: Prepares the configuration and metadata.
* **Nano Banana**: Executes the image generation and serves the file locally.


5. **Review Phase**:
* **Feedback Agent**: Critiques the result. If `Score < 7`, the graph loops. If `Score >= 7`, it proceeds to the result creator.



## 🤖 The Agent Team

| Agent | Role | Source File |
| --- | --- | --- |
| **Manager** | **Project Lead:** Deconstructs user input and sets the strategic direction. | `Agents/Manager.py` |
| **Creative Writer** | **Copywriter:** Generates engaging text assets tailored to the audience. | `Agents/CreativeWriter.py` |
| **Layout Designer** | **Visual Architect:** Defines the geometry and placement (bounding boxes) of the ad. | `Agents/LayoutDesigner.py` |
| **Color Theorist** | **Palette Specialist:** Uses color psychology to evoke specific viewer emotions. | `Agents/ColorTheorist.py` |
| **Font Expert** | **Typography Lead:** Selects fonts ensuring readability and brand alignment. | `Agents/FontExpert.py` |
| **T2I Prompt Designer** | **Prompt Engineer:** Translates creative concepts into machine-readable prompts. | `Agents/T2IPromptDesigner.py` |
| **Nano Banana** | **Production:** The execution engine that renders the final image. | `Agents/NanoBanana.py` |
| **Feedback Agent** | **Quality Assurance:** Grades the output and enforces high standards. | `Agents/FeedbackAgent.py` |

## 🛠️ Installation

### Prerequisites

* Python 3.10+
* Google Cloud API Key (with access to Gemini models)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/marketing-agency-mas.git
cd marketing-agency-mas

```

### 2. Setup Environment

Create a `.env` file in the root directory and add your Google API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

## ⚡ Usage

### Start the Server

The project exposes a REST API via FastAPI.

```bash
uvicorn api:app --reload

```

*The server will start at `http://127.0.0.1:8000`.*

### Generate an Advertisement

Send a **POST** request to `/create_ad` with your brief.

**Example Request:**

```json
{
  "brand": "CyberSoda",
  "topic": "Launch of new Neon-Lime flavor",
  "channel": "Instagram Story",
  "target_audience": "Gamers and Tech Enthusiasts"
}

```

**Example Response:**

```json
{
  "headline": "Taste the Glitch",
  "body": "Fuel your late-night raids with the new Neon-Lime spark. Zero lag, maximum flavor.",
  "hashtags": ["#CyberSoda", "#GamerFuel", "#NeonLime"],
  "image": "http://127.0.0.1:8000/static/image.png"
}

```

## 📂 Project Structure

```text
├── Agents/                 # Logic for individual agents
│   ├── Manager.py
│   ├── CreativeWriter.py
│   ├── LayoutDesigner.py
│   ├── ColorTheorist.py
│   ├── FontExpert.py
│   ├── T2IPromptDesigner.py
│   ├── ImageGenerator.py
│   ├── NanoBanana.py
│   └── FeedbackAgent.py
├── Formats/                # Pydantic Schemas & State
│   ├── Input_Formats.py
│   ├── Output_Formats.py
│   └── MarketingAgency.py  # Main State definition
├── api.py                  # FastAPI entry point
├── graph.py                # LangGraph workflow definition
├── utils.py                # LLM & Utility tools
├── requirements.txt
└── .env

```

## 📜 License

[MIT License]


