import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
import logging
from typing import List, Dict, Any


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConceptualMap:
    def __init__(self, node_list: List[str] = None, edge_list: List[tuple] = None):
        """Creates a conceptual map graph. If node_list and edge_list are provided, it initializes the graph with those nodes and edges.
        node_list is a list of node names (strings) and edge_list is a list of tuples, where each tuple contains two node names and an optional label in third position.

        Args:
            node_list (List[str], optional): List of nodes used to initialize the map. Defaults to None.
            edge_list (List[tuple], optional): List of tuples containing the edges. Defaults to None.
        """
        self.graph = nx.Graph()
        self.node_labels = {}

        if node_list:
            for node in node_list:
                self.add_node(node)
        if edge_list:
            for edge in edge_list:
                if len(edge) == 2:
                    self.add_edge(edge[0], edge[1])
                elif len(edge) == 3:
                    self.add_edge(edge[0], edge[1], label=edge[2])
        
    def add_node(self, node: str, label: str = None):
        """Add a node to the mental map."""
        self.graph.add_node(node)
        if label:
            self.node_labels[node] = label
        else:
            self.node_labels[node] = node 
    
    def add_edge(self, node1: str, node2: str, label: str = ""):
        """Add an edge between two nodes."""
        if self.graph.has_node(node1) and self.graph.has_node(node2):
            if label:
                self.graph.add_edge(node1, node2, label=label)
            else:
                self.graph.add_edge(node1, node2)
        else:
            logger.warning(f"Cannot add edge from {node1} to {node2}: one or both nodes do not exist.")    

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
    
    
    def diff(self, other_map: 'ConceptualMap') -> List[Dict[str, Any]]:
        """Compare this mental map with another and return the differences."""
        nodes_diff = []
        edges_diff = []
        
        # Compare nodes
        for node in self.graph.nodes():
            if node not in other_map.graph.nodes():
                nodes_diff.append({"node": node})

        # Compare edges
        for edge in self.graph.edges(data=True):
            if edge not in other_map.graph.edges(data=True):
                edges_diff.append({"edge": edge})

        return ConceptualMap(nodes_diff, edges_diff)
    
    @staticmethod
    def get_empty_graph() -> 'ConceptualMap':
        """Return an empty graph."""
        return ConceptualMap()
    
    @staticmethod
    def get_empty_json_graph() -> str:
        """Return an empty graph in JSON format."""
        empty_graph = {
            "directed": False,
            "multigraph": False,
            "graph": {},
            "nodes": [],
            "links": []
        }
        return json.dumps(empty_graph)