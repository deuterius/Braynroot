import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
import logging
from typing import List, Dict, Any


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MentalMap:
    def __init__(self):
        self.graph = nx.Graph()
        self.node_labels = {}

    def add_node(self, node: str, label: str = None):
        """Add a node to the mental map."""
        self.graph.add_node(node)
        if label:
            self.node_labels[node] = label
        else:
            self.node_labels[node] = node 
    
    def add_edge(self, node1: str, node2: str, label: str = ""):
        """Add an edge between two nodes."""
        
        self.graph.add_edge(node1, node2, label=label)
        
        
    def get_edge_list(self) -> List[tuple]:
        """Get the list of edges in the graph."""
        return list(self.graph.edges())
    
    def get_node_list(self) -> List[str]:
        """Get the list of nodes in the graph."""
        return list(self.graph.nodes())
    
    def export_to_json(self, filename: str):
        """Export the graph to a JSON file."""
        data = nx.node_link_data(self.graph)
        with open(filename, 'w') as f:
            json.dump(data, f)
        logger.info(f"Graph exported to {filename}")
    
    def import_from_json(self, filename: str):
        """Import the graph from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        self.graph = nx.node_link_graph(data)
        self.node_labels = {node: node for node in self.graph.nodes()}
        logger.info(f"Graph imported from {filename}")
    
    def draw_graph(self, filename: str = "mental_map.png"):
        """Draw the graph and save it as an image."""
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=False, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
        
        # Draw labels
        labels = {node: self.node_labels[node] for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels=labels)
        
        plt.title("Mental Map")
        plt.savefig(filename)
        plt.close()