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

    NOTE for MODIFICATIONs: If you want to modify the structure of the graph, add attrubutes, etc, you can modify the factory methods. For example, if you want to add a default attribute to each node, you can modify the node_attr_dict_factory method to return a dict with the default attribute.
    
    Examples
    --------
    """

    # TODO: We define the factory variables
    node_dict_factory = dict
    node_attr_dict_factory = dict
    adjlist_outer_dict_factory = dict
    adjlist_inner_dict_factory = dict
    edge_attr_dict_factory = dict
    graph_attr_dict_factory = dict


    def __init__(self, **attr):
        r"""
        Initialize a magnetic graph.

        Attributes
        ----------
        Note that we can add attributes that we haven't considered in this class. Here we describe the main attributes of the class, and those that we use in the methods.
            name: string, the name of the graph.
        """
        self.graph = self.graph_attr_dict_factory() 
        self._node = self.node_dict_factory()
        self._adj = self.adjlist_outer_dict_factory()
        self.graph.update(attr)


    @property
    def name(self):
        """
        String with the name of the graph. The name is stored in the graph as an attribute with key "name" (added in the init).If we haven't set a name it returns an empty string.
        """
        return self.graph.get("name", "")

    @name.setter
    def name(self, name):
        self.graph["name"] = name
    
    def __str__(self):
        """
        A string representation of the graph, with general information about the graph.
        """

        return "".join([
            type(self).__name__,
            f"named {self.name!r}" if self.name else "",
            f" with {self.number_of_nodes()} nodes and {self.number_of_edges()} edges"
        ])

    def number_of_nodes(self):
        return len(self._node)
    
    def number_of_edges(self, u=None, v=None):
        if u is None:
            return int(self.size())
        if v in self._adj[u]:
            return 1
        return 0
    

    @cached_property
    def degree(self, weight=None):
        # TODO (implement pq NetworkX ho fa complexe)
        pass


    def size(self, weight=None):
        s = sum(d for v, d in self.degree(weight=weight))
        return s // 2 if weight is None else s / 2