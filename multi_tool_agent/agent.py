
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

# Ignore all warnings
warnings.filterwarnings("ignore")

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDkMq3SUqW56rZ5EyrutxP-VbN8tJlinOs"
logging.basicConfig(level=logging.INFO)

prompt = """
    This agent is able to understand an input text and understand a conceptual graph related to that text.
    A graph is expressed in json format: each node (the elements of the "nodes" keys) is associated to a concept, and each 
    edge (the elements of the "links" keys) is associated to a sematic relation between nodes.
    This agent receives in input two graphs: 
    - G0 is the graph at time 0 (PAST)
    - G1 is the graph at time 1 (PRESENT)
    Your job is to give feedback and compare the two graphs and suggest if the current (G1) version has been improved or if it has introduced information that is not consistent or relevant with the input text. 

    DO NOT go overboard with changes, STICK to the ideas proposed by the user, CHANGE only the least possible to not intact the user workflow.

    You will receive a text that you will be using to provide proper feedback to the user, it acts as a ground truth, the text will start with the following markers ### START TEXT ### and will end with the ### END TEXT ### marker. After the text you will find the two graphs G0 and G1, the first one is the graph at time 0, the second one is the graph at time 1. The agent should be able to give a feedback only about the changes that have been done from G0 to G1. the graphs markers are the following: ### START GRAPH G0 ### and ### END GRAPH G0 ### for the first graph, and ### START GRAPH G1 ### and ### END GRAPH G1 ### for the second graph.
    
    Extra instructions might be provided in the following prompts, follow them CAREFULLY.
    """

root_agent = Agent(
    name="weather_time_agent",
    model=MODEL_GEMINI_2_0_FLASH,
    description=(
        "A helpful study assistant that helps student to create conceptul maps given a certain input text"
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
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

logger.info(f"Runner created for agent {runner.agent.name}")

async def _feedback_call_async(query: str, runner:Runner, user_id, session_id):
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
    

async def feedback(text: str, g1: str, g0: str):
    user_prompt = f"DO NOT respond using JSON format, the response should be accurate. DO NOT produce summaries, DO NOT introduce the reponse in a way that does not immediatly provides useful information such as \"I've reviewed the graphs and here's the feedback\". DO NOT mention the names of the graphs G0 and G1. Your responses will be suggestions and NOT actions. Justify your suggestions. \n ### START TEXT ### {text} ### END TEXT ###\n\n### START GRAPH G0 ###\n\n {g0} \n\n ### END GRAPH G0 ###\n\n ### START GRAPH G1 ###\n\n {g1} \n\n ### END GRAPH G1 ###"
    await _feedback_call_async(user_prompt,
                            runner=runner,
                            user_id=USER_ID,
                            session_id=SESSION_ID)


