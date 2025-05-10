import json
from typing import Dict, List, Tuple, Any, Optional, Union

class GraphValidationError(Exception):
    """Custom exception for graph validation errors."""
    pass

def validate_and_parse_graph_json(json_string: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validates and parses a JSON string representing a graph.
    
    Args:
        json_string (str): String containing JSON representation of a graph
        
    Returns:
        Tuple[Dict[str, Any], List[str]]: Tuple containing:
            - The validated graph as a Python dictionary
            - List of warnings (if any)
            
    Raises:
        GraphValidationError: If the JSON is invalid or missing required graph structure
    """
    warnings = []
    
    # Step 1: Basic JSON validation
    try:
        graph_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise GraphValidationError(f"Invalid JSON: {str(e)}")
    
    # Step 2: Check if it's a dictionary
    if not isinstance(graph_data, dict):
        raise GraphValidationError("JSON must represent an object (dictionary)")
    
    # Step 3: Check for required keys
    required_keys = ["directed", "multigraph", "graph", "nodes", "links"]
    missing_keys = [key for key in required_keys if key not in graph_data]
    
    if missing_keys:
        raise GraphValidationError(f"Missing required keys: {', '.join(missing_keys)}")
    
    # Step 4: Validate types of top-level properties
    if not isinstance(graph_data["directed"], bool):
        raise GraphValidationError("'directed' must be a boolean")
        
    if not isinstance(graph_data["multigraph"], bool):
        raise GraphValidationError("'multigraph' must be a boolean")
        
    if not isinstance(graph_data["graph"], dict):
        raise GraphValidationError("'graph' must be an object")
        
    if not isinstance(graph_data["nodes"], list):
        raise GraphValidationError("'nodes' must be an array")
        
    if not isinstance(graph_data["links"], list):
        raise GraphValidationError("'links' must be an array")
    
    # Step 5: Validate nodes structure
    node_ids = set()
    for i, node in enumerate(graph_data["nodes"]):
        if not isinstance(node, dict):
            raise GraphValidationError(f"Node at position {i} must be an object")
            
        if "id" not in node:
            raise GraphValidationError(f"Node at position {i} is missing required 'id' field")
            
        node_id = node["id"]
        if node_id in node_ids:
            warnings.append(f"Duplicate node ID found: '{node_id}'")
        node_ids.add(node_id)
    
    # Step 6: Validate links structure
    for i, link in enumerate(graph_data["links"]):
        if not isinstance(link, dict):
            raise GraphValidationError(f"Link at position {i} must be an object")
            
        # Check required fields
        for field in ["source", "target"]:
            if field not in link:
                raise GraphValidationError(f"Link at position {i} is missing required field '{field}'")
        
        # Check if source and target exist in nodes
        if link["source"] not in node_ids:
            raise GraphValidationError(f"Link at position {i} references nonexistent source node '{link['source']}'")
            
        if link["target"] not in node_ids:
            raise GraphValidationError(f"Link at position {i} references nonexistent target node '{link['target']}'")
        
        # Check if label exists (highly recommended for graph visualization)
        if "label" not in link:
            warnings.append(f"Link from '{link['source']}' to '{link['target']}' is missing a 'label'")
    
    # Return the validated graph data and any warnings
    return graph_data, warnings


def convert_to_networkx(graph_data: Dict[str, Any]) -> 'nx.Graph':
    """
    Converts the validated graph data to a NetworkX graph.
    
    Args:
        graph_data (Dict[str, Any]): Validated graph data
        
    Returns:
        nx.Graph: NetworkX graph object
        
    Note:
        This function requires NetworkX to be installed.
        Install with: pip install networkx
    """
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("NetworkX is required but not installed. Install with: pip install networkx")
    
    # Create the appropriate graph type
    if graph_data["directed"]:
        G = nx.DiGraph()
    elif graph_data["multigraph"]:
        G = nx.MultiGraph()
    else:
        G = nx.Graph()
    
    # Add graph attributes
    G.graph.update(graph_data["graph"])
    
    # Add nodes with attributes
    for node in graph_data["nodes"]:
        node_id = node.pop("id")
        G.add_node(node_id, **node)
    
    # Add edges with attributes
    for link in graph_data["links"]:
        source = link.pop("source")
        target = link.pop("target")
        G.add_edge(source, target, **link)
    
    return G


def process_graph_string(json_string: str) -> Dict[str, Any]:
    """
    Process and validate a JSON string representing a graph.
    
    Args:
        json_string (str): String containing JSON representation of a graph
        
    Returns:
        Dict[str, Any]: The validated graph as a Python dictionary
        
    Raises:
        GraphValidationError: If the JSON is invalid or the graph structure is incorrect
    """
    try:
        graph_data, warnings = validate_and_parse_graph_json(json_string)
        
        # Print any warnings
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        
        # Optionally convert to NetworkX (commented out by default)
        # nx_graph = convert_to_networkx(graph_data)
        
        return graph_data
        
    except GraphValidationError as e:
        print(f"Error validating graph: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise


# Example usage
if __name__ == "__main__":
    # Example valid graph JSON
    valid_json = """{
        "directed": false,
        "multigraph": false,
        "graph": {},
        "nodes": [
            {"id": "Concept1"},
            {"id": "Concept2"},
            {"id": "Concept3"}
        ],
        "links": [
            {"label": "relates to", "source": "Concept1", "target": "Concept2"},
            {"label": "includes", "source": "Concept2", "target": "Concept3"}
        ]
    }"""
    
    # Example with issues
    invalid_json = """{
        "directed": false,
        "multigraph": false,
        "graph": {},
        "nodes": [
            {"id": "Concept1"},
            {"id": "Concept2"}
        ],
        "links": [
            {"label": "relates to", "source": "Concept1", "target": "Concept2"},
            {"source": "Concept2", "target": "Concept3"}
        ]
    }"""
    
    # Test valid JSON
    try:
        result = process_graph_string(valid_json)
        print("\nValid graph processed successfully:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Failed processing valid graph: {e}")
    
    # Test invalid JSON
    print("\nTesting invalid JSON:")
    try:
        result = process_graph_string(invalid_json)
    except Exception as e:
        print(f"Expected error handling: {e}")