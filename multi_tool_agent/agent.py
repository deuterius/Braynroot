
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import os
import asyncio
#from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
import logging
import warnings
from parser import extract_json_and_text
from json_validator import process_graph_string

# Ignore all warnings
warnings.filterwarnings("ignore")

MODEL_GEMINI_2_0_FLASH = "gemini-2.5-flash-preview-04-17"
MODEL_CLAUDE_SONNET_LATEST = "claude-3-7-sonnet-20250219"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCMT787FU6HQ35ORnBee88L-V2PPjS-XGM"
logging.basicConfig(level=logging.INFO)
MAX_ITERATIONS = 3

prompt = """
    # Mental Mapping Agent Instructions

You are a SPECIALIZED MENTAL MAPPING ASSISTANT designed to analyze and improve conceptual graphs representing educational content.

## Core Capabilities
- Understand relationships between concepts in academic texts
- Compare graph versions for logical improvements
- Provide targeted feedback on graph modifications
- Suggest minimal, high-value additions when users are stuck

## Graph Structure
Graphs are provided in JSON format with this structure:
- `nodes`: Individual concepts (each with an "id" field)
- `links`: Relationships between concepts (with "source", "target", and "label" fields)

## Your Primary Task
You MUST compare two versions of a graph (G0 and G1) representing the same educational text, then provide SPECIFIC FEEDBACK on whether G1 shows improvement.

## Input Format
1. REFERENCE TEXT (between `### START TEXT ###` and `### END TEXT ###` markers)
   - This is your GROUND TRUTH for evaluating graph accuracy
   - All feedback MUST be based on this text only

2. GRAPH G0 (between `### START GRAPH G0 ###` and `### END GRAPH G0 ###` markers)
   - The PREVIOUS version of the conceptual map

3. GRAPH G1 (between `### START GRAPH G1 ###` and `### END GRAPH G1 ###` markers)
   - The CURRENT version of the conceptual map

4. OPTIONAL supplementary instructions

## Response Requirements
- FOCUS EXCLUSIVELY on changes between G0 and G1
- Evaluate if new elements ACCURATELY represent concepts from the text
- Assess if relationship labels (verbs) CORRECTLY capture connections
- Check if modifications maintain LOGICAL CONSISTENCY
- Be DIRECT and CONCISE in your feedback
- NEVER rewrite the entire graph - recommend only minimal necessary changes
- PRESERVE the user's conceptual approach and workflow

## Important Guidelines
- DO NOT go beyond the scope of the reference text
- USE SPECIFIC examples from the text to justify feedback
- MAINTAIN the user's agency in the learning process
- PRIORITIZE clarity over comprehensiveness
    """

graph_agent = Agent(
    name="conceptual_map_assistant",
    model=MODEL_GEMINI_2_0_FLASH,
    description=(
        "A specialized study assistant that transforms educational texts into structured conceptual maps, identifying key concepts and their relationships to enhance learning and retention."
    ),
    instruction=prompt,
    tools=[],
)


import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

session_service = InMemorySessionService()

APP_NAME = "GDG"
USER_ID = "Test_User"
SESSION_ID = "session_4269420_nice"

session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

runner = Runner(
    agent=graph_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

logger.info(f"Runner created for agent {runner.agent.name}")

async def _agent_call_async(query: str, runner:Runner, user_id, session_id):
    """Sends a query to the agent and returns the response"""    
    logger.info(f"User query: {query}")
    
    content = types.Content(role="user", parts=[types.Part(text=query)]) # qua ci andra anche il json
    
    final_response_text = "The agent wasn't able to provide a response"
    
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent has escalated: {event.error_message or 'could not find an error message, sowwy :('}"
            break
    
    logger.info(f"Final response: {final_response_text}")
    return final_response_text

async def suggest_addition(text: str, g0: str, g1: str):
    
    user_prompt = """You MUST analyze the existing conceptual graphs and provide MINIMAL, STRATEGIC additions when a user is stuck.

## Input Data
- REFERENCE TEXT: Educational content that serves as the ground truth
- GRAPH G0: Previous version of the conceptual map
- GRAPH G1: Current version of the conceptual map

## Output Requirements
- Provide EXACTLY ONE valid JSON object representing graph G2
- Follow the PRECISE format requirements below
- Add only 1-3 new nodes OR 2-4 new relationships maximum
- Ensure suggestions are DIRECTLY supported by the reference text
- NEVER CITE the graph IDs (G0, G1) in your response, but refer to them as "previous" and "current" versions
- NEVER add labels on already existing edges, NEVER! Only on new edges if you add any.
- AVOID adding ONLY labels, add at least an edge+label, or a node+edge+label. 
- you MAY add more than one node/edge when necessary, but be careful to not add too many.  

## JSON Format Requirements
```json
{
  "directed": false,
  "multigraph": false,
  "graph": {},
  "nodes": [
    {"id": "ConceptName1"},
    {"id": "ConceptName2"}
  ],
  "links": [
    {"label": "relationship verb", "source": "ConceptName1", "target": "ConceptName2"}
  ]
}
```

## Relationship Guidelines
- Use CLEAR, SPECIFIC verbs for relationships such as:
  - "is part of"
  - "contains"
  - "influences"
  - "causes"
  - "requires"
  - "produces"
  - "contrasts with"
  - "complements"

## Critical Instructions
- MAINTAIN all existing nodes and relationships from G1
- ADD only what's necessary to help the user progress
- ENSURE suggestions are FIRMLY grounded in the reference text
- NEVER completely reshape the user's conceptual approach
- VALIDATE your JSON is properly formatted before returning it

## Response Format
- Include a BRIEF explanation (1-2 sentences) of your suggestion
- IMMEDIATELY followed by the complete G2 JSON object\n\n"""

    user_prompt += f"### START TEXT ###\n\n {text} \n\n ### END TEXT ###\n\n### START GRAPH G0 ###\n\n {g0} \n\n ### END GRAPH G0 ###\n\n ### START GRAPH G1 ###\n\n {g1} \n\n ### END GRAPH G1 ###"
    
    for iter in range(MAX_ITERATIONS):
        output = await _agent_call_async(user_prompt,
                                runner=runner,
                                user_id=USER_ID,
                                session_id=SESSION_ID)
        
        json_string, text_explanation = extract_json_and_text(output)
        logger.info(f"Extracted JSON object: {json_string}")
        logger.info(f"Extracted text explanation: {text_explanation}")
        try:
            json_object = process_graph_string(json_string)
        except:
            logger.error(f"Error processing JSON string: {json_string}")
            continue
        
        logger.info(f"Valid JSON found")
        logger.info(f"JSON object: {json_object}")
        return json_object, text_explanation
    
    raise ValueError(f"No valid JSON found after {MAX_ITERATIONS} iterations")
    
    


async def feedback(text: str, g1: str, g0: str):
    # user_prompt = f"DO NOT respond using JSON format, the response should be accurate. DO NOT produce summaries, DO NOT introduce the reponse in a way that does not immediatly provides useful information such as \"I've reviewed the graphs and here's the feedback\". DO NOT mention the names of the graphs G0 and G1. Your responses will be suggestions and NOT actions. Justify your suggestions. \n ### START TEXT ### {text} ### END TEXT ###\n\n### START GRAPH G0 ###\n\n {g0} \n\n ### END GRAPH G0 ###\n\n ### START GRAPH G1 ###\n\n {g1} \n\n ### END GRAPH G1 ###"
    
    user_prompt = f""" You MUST analyze the differences between two conceptual graphs (G0 and G1) and provide TARGETED FEEDBACK based on the reference text.

## Input Data Format
- REFERENCE TEXT: Between markers `### START TEXT ###` and `### END TEXT ###`
- GRAPH G0: Between markers `### START GRAPH G0 ###` and `### END GRAPH G0 ###`
- GRAPH G1: Between markers `### START GRAPH G1 ###` and `### END GRAPH G1 ###`

## Output Requirements
- Provide feedback as NATURAL LANGUAGE TEXT only (NO JSON, NO code blocks)
- Keep your response CONCISE. Even more concise if the differences are minimal.
- Structure feedback in 2-3 paragraphs maximum
- Use DIRECT, CLEAR language appropriate for students
- NEVER CITE the graph IDs (G0, G1) in your response, but refer to them as "previous" and "current" versions
- AVOID unnecessary introductions or summaries
- FOCUS on the differences between the two graphs

## Analysis Steps
1. IDENTIFY specific nodes and relationships added, removed, or modified
2. EVALUATE whether changes accurately reflect concepts in the reference text
3. ASSESS if relationship labels (verbs) logically connect the concepts, if present
4. DETERMINE if graph modifications help clarify understanding

## Feedback Guidelines
- Be CONSTRUCTIVE - highlight both positive changes and areas for improvement
- CITE specific examples from the reference text to support your feedback
- FOCUS on conceptual accuracy rather than graph complexity

## Critical Instructions
- NEVER generate a complete alternative graph - focus solely on feedback
- AVOID overwhelming the user - prioritize 2-3 most important points
- MAINTAIN a supportive tone that encourages learning

### START TEXT ###\n\n {text} \n\n ### END TEXT ###\n\n### START GRAPH G0 ###\n\n {g0} \n\n ### END GRAPH G0 ###\n\n ### START GRAPH G1 ###\n\n {g1} \n\n ### END GRAPH G1 ###
"""
    
    await _agent_call_async(user_prompt,
                            runner=runner,
                            user_id=USER_ID,
                            session_id=SESSION_ID)


