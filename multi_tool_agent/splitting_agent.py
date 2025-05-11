import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import os
import asyncio
# from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
import logging
import warnings
from parser import extract_json_and_text
from json_validator import process_graph_string

# Ignore all warnings
warnings.filterwarnings("ignore")

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDkMq3SUqW56rZ5EyrutxP-VbN8tJlinOs"
logging.basicConfig(level=logging.INFO)

prompt=""" 
This agent specializes in transforming raw, unstructured text—typically generated from PDF conversions—into clean, structured educational content. Its main responsibilities are:
- Removing non-informative or noisy elements (e.g., page numbers, footnotes, image placeholders, formatting artifacts).
- Preserving the original content as much as possible, avoiding summarization or rephrasing.
- Segmenting the cleaned text into coherent, pedagogically useful learning units.
Each learning unit should group semantically related ideas or concepts, even if they span multiple paragraphs. The agent should avoid creating sections that are too short or overly fragmented. 
It is encouraged to aggregate content when appropriate, as long as the resulting section remains coherent and thematically consistent. As a general guideline, each learning unit should be approximately 500 words in length.
The final output consists of clearly separated sections, each representing a self-contained topic or theme that a student could learn independently.
"""

split_agent = Agent(
    name="document_cleaner_and_splitter",
    model=MODEL_GEMINI_2_0_FLASH,
    description=(
        "An agent specialized in cleaning a text document from uninformative data and splitting it according to the semantics"
    ),
    instruction=prompt,
    tools=[],
)

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
    agent=split_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

logger.info(f"Runner created for agent {runner.agent.name}")


async def _agent_call_async(query: str, runner:Runner, user_id, session_id):
    """Sends a query to the agent and returns the response"""    
    logger.info(f"User query: {query}")
    
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
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


async def split_text(input_text: str):
    user_prompt = f""" You are a text-processing and instructional-design agent. 
    Your task is to transform raw textual input—converted from a complex file such as a PDF—into clean, structured educational content. 
    The input text may include irrelevant or noisy elements (e.g., page numbers, footers, headers, figure/image placeholders, garbled characters). You MUST:
    - Thoroughly CLEAN the input, removing all non-informative or noisy elements.
    - SEGMENT the clean text into N meaningful SECTIONS based on semantic and structural coherence.
    - Treat each SECTION as a LEARNING UNIT: group related concepts or ideas that a student could learn as a standalone topic.

    ## Input Data Format
    - INPUT TEXT: Between markers ### START TEXT ### and ### END TEXT ###

    ## Output Requirements
    - Present each learning unit with a title and its corresponding cleaned content
    - Provide the output as a text in which the learning units are separated by the special sequence ***

    ### START TEXT ###\n\n {input_text} \n\n ### END TEXT ###
"""
    
    await _agent_call_async(user_prompt,
                            runner=runner,
                            user_id=USER_ID,
                            session_id=SESSION_ID)