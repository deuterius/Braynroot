import re
import json

def extract_json_and_text(response_text):
    """
    Extract the first valid JSON object from a text response and return both the JSON and the text.
    
    Args:
        response_text (str): The complete response from the Graph Suggestion API
        
    Returns:
        tuple: (json_object, explanatory_text)
            - json_object: The parsed JSON object as a Python dictionary
            - explanatory_text: The text portion of the response
    """
    # This regex pattern finds JSON objects starting with { and ending with }
    # It handles nested braces by counting opening and closing braces
    json_pattern = r'({(?:[^{}]|(?R))*})'
    
    # For simpler implementation without recursive patterns, we can use this approach:
    def find_matching_brace(text, start_pos):
        """Find the position of the matching closing brace."""
        count = 1
        pos = start_pos
        
        while count > 0 and pos < len(text):
            pos += 1
            if pos >= len(text):
                break
            if text[pos] == '{':
                count += 1
            elif text[pos] == '}':
                count -= 1
                
        return pos if count == 0 else -1
    
    # Find the first opening brace
    open_pos = response_text.find('{')
    if open_pos == -1:
        return None, response_text
    
    # Find matching closing brace
    close_pos = find_matching_brace(response_text, open_pos)
    if close_pos == -1:
        return None, response_text
    
    # Extract the JSON string and the text
    json_str = response_text[open_pos:close_pos+1]
    
    # Determine explanatory text (could be before, after, or both)
    before_text = response_text[:open_pos].strip()
    after_text = response_text[close_pos+1:].strip()
    explanatory_text = (before_text + " " + after_text).strip()
    
    # Parse the JSON string
    try:
        # json_obj = json.loads(json_str)
        return json_str, explanatory_text
    except json.JSONDecodeError:
        return None, response_text


# Example usage
if __name__ == "__main__":
    # Sample response with JSON and explanatory text
    sample_response = """
    I've added a new concept "Photosynthesis" and connected it to "Plants" with the relationship "occurs in".
    These concepts appear in paragraph 2 of the text.
    
    {
      "directed": false,
      "multigraph": false,
      "graph": {},
      "nodes": [
        {"id": "Plants"},
        {"id": "Sunlight"},
        {"id": "Photosynthesis"}
      ],
      "links": [
        {"label": "require", "source": "Plants", "target": "Sunlight"},
        {"label": "occurs in", "source": "Photosynthesis", "target": "Plants"}
      ]
    }
    
    I hope this helps expand your understanding!
    """
    
    json_object, text_explanation = extract_json_and_text(sample_response)
    
    print("EXTRACTED JSON OBJECT:")
    print(json.dumps(json_object, indent=2))
    print("\nEXTRACTED TEXT:")
    print(text_explanation)