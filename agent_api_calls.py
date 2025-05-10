import asyncio
from multi_tool_agent.agent import feedback, suggest_addition
from google.genai import types
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    text = """
    The Cat (Felis catus): Scientific Definition and Characteristics
The domestic cat (Felis catus), commonly referred to as the cat, is a carnivorous mammal belonging to the family Felidae, within the order Carnivora. It is a domesticated subspecies of the wildcat (Felis silvestris), with which it shares a close genetic and morphological relationship.
Cats are nocturnal predators with highly developed senses, including acute night vision, directional hearing, and a refined sense of smell. Their musculoskeletal structure allows for exceptional agility, balance, and jumping ability, making them highly efficient hunters.
Domestication of the cat is estimated to have occurred approximately 9,000 years ago in the Near East, likely in agricultural communities where wildcats were attracted by rodent populations around grain stores. Unlike dogs, cats underwent a relatively mild domestication process, retaining many behavioral traits of their wild ancestors.
The social behavior of cats is variable. While traditionally considered solitary animals, domestic cats can adapt to complex social environments and form bonds with both humans and other animals. Some colonies of feral cats even display forms of cooperative behavior.
In biology, the cat serves as a model organism for studying predatory behavior, vision in low-light conditions, and inherited feline diseases. Moreover, cats play an important role in understanding the dynamics of human-animal interaction and the process of animal domestication.
"""
    g0 = """{
    "directed": false,
    "multigraph": false,
    "graph": { },
    "nodes": [
      {"id": "cat"}
    ],
    "links": [
    ]
}"""

    g1 = """
    {
    "directed": false,
    "multigraph": false,
    "graph": { },
    "nodes": [
      {"id": "cat"},
      {"id": "feline"},
      {"id": "domesticated"},
      {"id": "dog"}
    ],
    "links": [
      {"source": "cat", "target": "domesticated"},
      {"source": "dog", "target": "domesticated"},
      {"source": "cat", "target": "feline"},
      
    ]
}"""

    g2 = """
    {
    "directed": false,
    "multigraph": false,
    "graph": { },
    "nodes": [
      {"id": "cat"},
      {"id": "feline"},
      {"id": "domesticated"},
      {"id": "dog"}
    ],
    "links": [
      {"source": "cat", "target": "domesticated"},
      {"source": "dog", "target": "domesticated"},
      {"source": "cat", "target": "feline"},
    ]
}
"""
    try:
        # asyncio.run(feedback(text=text, g0=g1, g1=g2))
        asyncio.run(suggest_addition(text=text, g0=g1, g1=g2))
    except Exception as e:
        print(f"An error occurred: {e}")