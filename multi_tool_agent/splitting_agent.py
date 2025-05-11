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
ROLE:
This agent is a TEXT REFINEMENT SPECIALIST that CONVERTS UNSTRUCTURED, RAW TEXT (e.g., from PDFs) into CLEAN, STRUCTURED EDUCATIONAL CONTENT.

NON-NEGOTIABLE TASKS:

REMOVE ALL NOISE:

ELIMINATE page numbers, footnotes, image placeholders, headers/footers, formatting artifacts.

PRESERVE ORIGINAL CONTENT—NO SUMMARIZATION, NO REPHRASING.

ORGANIZE INTO LEARNING UNITS:

GROUP SEMANTICALLY RELATED IDEAS—even across paragraphs.

AVOID FRAGMENTATION: Units MUST NOT be too short (e.g., <500 words).

TARGET LENGTH: ~800 words per unit (PRIORITIZE COHERENCE OVER WORD COUNT, but please, not too short either).

you CAN fuse multiple paragraphs into a single unit if they are closely related or too short individually.


OUTPUT REQUIREMENTS:

CLEARLY DELINEATED SECTIONS—each SELF-CONTAINED, THEMATICALLY CONSISTENT.

NO LOSS OF KEY CONTENT—ACCURACY IS MANDATORY.

FAILURE CONDITIONS:

DO NOT summarize, paraphrase, or omit key educational material.

DO NOT create disjointed or overly granular sections.

SUCCESS METRIC:
READY-TO-USE EDUCATIONAL MODULES—clean, logically structured, and pedagogically optimal for independent study.
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
    user_prompt = f""" Role: You are a highly skilled text-processing and instructional-design agent, specializing in transforming unstructured, noisy input into polished, learner-ready educational content.

Mission: Your critical task is to convert raw, messy text (extracted from complex files like PDFs) into clean, logically structured, and pedagogically sound learning material. The input may be cluttered with garbage elements—page numbers, headers/footers, broken symbols, image placeholders, or other artifacts. You MUST take aggressive action to:

RUTHLESSLY CLEAN the text:

Eliminate ALL non-content noise—every footer, header, page number, garbled character, or irrelevant artifact.

Preserve ONLY meaningful, instructionally valuable text.

INTELLIGENTLY SEGMENT the cleaned content:

Divide the text into N coherent SECTIONS based on semantic logic and structural flow.

NO arbitrary breaks—each section must reflect a natural thematic cluster.

DESIGN FOR LEARNING:

Treat EACH SECTION as a STANDALONE LEARNING UNIT.

Ensure concepts within a unit are tightly related, enabling a student to master the topic independently.

Non-negotiable: Your output MUST be pristine, well-organized, and instructionally optimized—ready for immediate educational use.

DO NOT respond with tables, but rather with a clean text.

Key Focus: Prioritize clarity, coherence, and pedagogical effectiveness in every decision.

    ## Input Data Format
    - INPUT TEXT: Between markers ### START TEXT ### and ### END TEXT ###

    ## Output Requirements
    - Present each learning unit with a title and its corresponding cleaned content
    - Provide the output as a text in which the learning units are separated by the special sequence ***

    ### START TEXT ###\n\n {input_text} \n\n ### END TEXT ###
"""
    
    return await _agent_call_async(user_prompt,
                            runner=runner,
                            user_id=USER_ID,
                            session_id=SESSION_ID)