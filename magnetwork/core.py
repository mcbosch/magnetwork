import numpy as np
from functools import cached_property 

"""
Simplified implementation of magnetic graphs in Python. The structure is inspired by NetworkX but focuses on magnetic graphs. Moreover, in this repository, I will implement only the necessary methods to work with magnetic graphs, compute it's Laplacian and spectrum, be able to work with different potential functions, and visualize this graphs.

In this file, we define the MagGraph class, an some of the most basic methods. We won't define a basic class of Graph for undirected graphs, since we can use NetworkX for that. Moreover, if you want to work with both, magnetic and undirected graphs, you can consider a magnetic graph with a zero potential, or any potential cohomologous with zero.
"""

class MagGraph:
    """
    NOTE: If you are not used to NetworkX, please read the following description carefully. And if you don't know anythig about Magnetic Graphs, please read the survey: https://arxiv.org/??????. Please, cite the survey if you use this code for research. 

    Base class for magnetic graphs.
    
    A magnetic graph stoores the nodes and edges with optional data. The edges are considered directed, but we have the two directions for each edge. Also, we have a potential function that assigns a value between 0 and 2pi to each edge. 
    Self-loops are allowed but multiedges are not (two edges in diferent directions is not considered a multiedge). The only restriction for nodes is tha they must be a hashable python object.

    How is stored the data
    ----------------------
    This class use a structure dict-of-dict-of-dict to store the graph structure and data.:

        >>> node_dict = {node1: adjlist_dict1,
                         node2: adjlist_dict2,
                         ...}
        >>> adjlist_dict = {neighbor1: edge_attr_dict,
                            neighbor2: edge_attr_dict,
                            ...}
        >>> edge_attr_dict = {attr1: value1,
                              attr2: value2,
                              ...}
    where node_dict is the main structure that stores the graph, adjlist_dict stores the neighbors of each node, and edge_attr_dict stores the attributes of each edge. This dictionaries are built with the methods node_dict_fatcory, adjlist_dict_factory and edge_attr_dict_factory,etc. That can be modified to change the structure of the graph.

    node_dict_factory : function, (default: dict)
        Factory function to be used to create the dict containing node
        attributes, keyed by node id.
        It should require no arguments and return a dict-like object
        Note that in the dict-of-dict-of-dict, introduced above, for the graph structure,
        there isn't the node attribute dict, so it will be a different attribute of the class.

    node_attr_dict_factory: function, (default: dict)
        Factory function to be used to create the node attribute
        dict which holds attribute values keyed by attribute name.
        It should require no arguments and return a dict-like object

    adjlist_outer_dict_factory : function, (default: dict)
        Factory function to be used to create the outer-most dict
        in the data structure that holds adjacency info keyed by node.
        It should require no arguments and return a dict-like object.

    adjlist_inner_dict_factory : function, (default: dict)
        Factory function to be used to create the adjacency list
        dict which holds edge data keyed by neighbor.
        It should require no arguments and return a dict-like object

    edge_attr_dict_factory : function, (default: dict)
        Factory function to be used to create the edge attribute
        dict which holds attribute values keyed by attribute name.
        It should require no arguments and return a dict-like object.

    graph_attr_dict_factory : function, (default: dict)
        Factory function to be used to create the graph attribute
        dict which holds attribute values keyed by attribute name.
        It should require no arguments and return a dict-like object.
    
    Examples
    --------
    """

    # TODO: Anylize previous methods
    # Consider necessary and not necessary methods: in this repo will be only the necessary ones. It will be a extended repository for more complex methods, to merge with networkx or other libraries.

    def __init__(self, incoming_graph_data=None, **attr):
        r"""
        Initialize a magnetic graph.
        """
        self.graph = {}
        self._node = {}
        self._adj = {}
        
        self.graph.update(attr)

    def add_node(self, node_for_adding, **attr):
        if node_for_adding not in self._node:
            if node_for_adding is None:
                raise ValueError("None object cannot be a node.")
            self._adj[node_for_adding] = {}
            attr_dict = self.node[node_for_adding] = self.node_attr_dict_factory()

    def add_nodes_from(self, nodes_for_adding, **attr):
        pass
        
    # TODO:
    def __str__(self):
        pass

    def __iter__(self):
        pass

    def __contains__(self, node):
        pass

    def __len__(self):
        pass

    def __getitem__(self, node):
        pass

    

    def remove_node(self, node):
        pass

    def remove_nodes_from(self, nodes):
        pass

    @cached_property # Note: Cached property is used to cache the result of the property, so it is not computed again.
    def nodes(self):
        pass

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        pass

    def add_edges_from(self, ebunch_to_add, **attr):
        pass

    def add_weighted_edges_from(self, ebunch_to_add, weight='weight', **attr):
        pass

    def remove_edge(self, u, v):
        pass

    def remove_edges_from(self, ebunch):
        pass

    def update(self, edges=None, nodes=None):
        """
        Updates a graph using edges and nodes as an input.
        """
        if edges is not None:
            if nodes is not None:
                self.add_nodes_from(nodes)
                self.add_edges_from(edges)
            else:
                # check if edges is a Graph object
                try:
                    graph_nodes = edges.nodes
                    graph_edges = edges.edges
                except AttributeError:
                    # edge not Graph-like
                    self.add_edges_from(edges)
                else:  # edges is Graph-like
                    self.add_nodes_from(graph_nodes.data())
                    self.add_edges_from(graph_edges.data())
                    self.graph.update(edges.graph)
        elif nodes is not None:
            self.add_nodes_from(nodes)

    def has_edge(self, u, v):
        pass

    def neighbors(self, node):
        pass

    @cached_property
    def edges(self):
        pass

    # TODO: ... there are more methods to implement, see networkx documentation.
    