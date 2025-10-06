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

    An important attribute for edges that we always should have, is the potential. By default is setted on 0, and can be any number between 0 and 2*pi. If it's setted to a number out of the specified intervval, the potential is setted to that number mod 2*pi.

    We build functions to create dictionaries which specifies what is created for each dictionary. To make it easier in tracking errors.

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
    node_dict_factory = dict
    node_attr_dict_factory = dict
    adjlist_outer_dict_factory = dict
    adjlist_inner_dict_factory = dict
    edge_attr_dict_factory = dict
    graph_attr_dict_factory = dict

    # DONE
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

    # DONE
    @property
    def name(self):
        """
        String with the name of the graph. The name is stored in the graph as an attribute with key "name" (added in the init).If we haven't set a name it returns an empty string.
        """
        return self.graph.get("name", "")

    # DONE
    @name.setter
    def name(self, name):
        self.graph["name"] = name
    
    # DONE
    def __str__(self):
        """
        A string representation of the graph, with general information about the graph.

        Example
        -------
            >>> G = MagGraph(name='Graph Example')
            >>> print(G)
                MagGraph named 'Graph Example' with 0 nodes and 0 edges
        """

        return "".join([
            type(self).__name__,
            f" named {self.name!r}" if self.name else "",
            f" with {self.number_of_nodes()} nodes and {self.number_of_edges()} edges"
        ])

    # DONE
    def __iter__(self):
        return iter(self._node)
    
    # DONE
    def __contains__(self, n):
        try:
            return n in self._node
        except TypeError:
            return False
    
    # DONE
    def __len__(self):
        return len(self._node)
    
    # DONE
    def __getitem__(self, n):
        """
        Return the adjacency dictionary for node n.
        """
        return self._adj[n]
    
    # DONE
    def add_node(self, n, **attr):
        """
        Add a single node n and update node attributes.

        Parameters
        ----------
        n : hashable
            A node
        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to the node as key=value pairs.
            Node attributes are stored in the node attribute dict
            (see node_attr_dict_factory).
        """
        if n is None:
            raise ValueError("None cannot be a node")
        
        if n not in self._node:
            self._adj[n] = self.adjlist_inner_dict_factory()
            self._node[n] = self.node_attr_dict_factory()
        self._node[n].update(attr)
    
    # DONE
    def add_nodes_from(self, nodes, **attr):
        for n in nodes:
            if n is None:
                raise ValueError("None cannot be a node")
            if n not in self._node:
                self._adj[n] = self.adjlist_inner_dict_factory()
                self._node[n] = self.node_attr_dict_factory()
            self._node[n].update(attr)
    
    # DONE
    def remove_node(self, n):
        
        try:
            nbrs = list(self._adj[n]) # list of neighbors
            del self._node[n]
        except KeyError:
            raise KeyError(f"The node {n} is not in the graph")
        
        for u in nbrs:
            del self._adj[u][n]
        del self._adj[n]
    
    # DONE
    def remove_nodes_from(self, nodes):

        for n in nodes:
            try:
                del self._node[n]
                for u in list(self._adj[n]):
                    del self._adj[u][n]
                del self._adj[n]
            except KeyError:
                pass
    
    # TODO
    @cached_property
    def nodes(self):
        pass
    
    # DONE
    def number_of_nodes(self):
        return len(self._node)
    
    # DONE
    def number_of_edges(self, u=None, v=None):
        if u is None:
            return int(self.size())
        if v in self._adj[u]:
            return 1
        return 0
    
    # TODO
    @cached_property
    def degree(self, weight=None):
        # Returns the number of edges.
        # NOTE: In magnetic Graphs, we consider always the two directions of the edges. Thus we don't divide by 2.
        # NOTE: Add a Degree Class so it's compatible with NetworkX.
        d = 0
        for item in self._adj.items(): d+=len(item[1])
        return d

    # TODO: Revisar funció
    def size(self, weight=None):
        return 0
        s = sum(d for v, d in self.degree(weight=weight))
        return s // 2 if weight is None else s / 2
    
    # DONE
    def add_edge(self, u, v, potential = 0, **attr):
        # The potential is setted in the direction u -> v

        # Add nodes to the graph if they aren't in the graph
        if u not in self._node:
            if u is None:
                raise ValueError("The nodes can't be None objects")
            self._adj[u] = self.adjlist_outer_dict_factory()
            self._node[u] = self.node_attr_dict_factory()
        if v not in self._node:
            if v is None:
                raise ValueError("The nodes can't be None objects")
            self._adj[v] = self.adjlist_outer_dict_factory()
            self._node[v] = self.node_attr_dict_factory()
        # Add the edge
        datadict_d1 = self._adj[u].get(v, self.edge_attr_dict_factory())
        datadict_d1.update(attr)
        datadict_d1['potential'] = potential

        datadict_d2 = self._adj[v].get(u, self.edge_attr_dict_factory())
        datadict_d2.update(attr)
        datadict_d2['potential'] = -potential
        
        self._adj[u][v] = datadict_d1
        self._adj[v][u] = datadict_d2

    # DONE   
    def add_edges_from(self, edges, **attr):
        """
        Parameters
        ----------
            edges: a list with the edges to add. We have two options for each element
                · 2-tuple (u, v) --> potential is setted to 0
                · 3-tuple (u, v, dd) --> dd is a dictionary containing edge data
        """
        for e in edges:
            if len(e) == 2:
                u, v = e
                dd = {}
            elif len(e) == 3:
                u, v, dd = e
            else:
                raise ValueError(f"Tuple {e} must be 2-tuple or 3-tuple")
        
        potential = dd.pop('potential') if 'potential' in dd else 0

        if u not in self._node:
            if u is None:
                raise ValueError("The nodes can't be None objects")
            self._adj[u] = self.adjlist_outer_dict_factory()
            self._node[u] = self.node_attr_dict_factory()
        if v not in self._node:
            if v is None:
                raise ValueError("The nodes can't be None objects")
            self._adj[v] = self.adjlist_outer_dict_factory()
            self._node[v] = self.node_attr_dict_factory()

        # Add the edge
        datadict_d1 = self._adj[u].get(v, self.edge_attr_dict_factory())
        datadict_d1.update(attr)
        datadict_d1.update(dd)
        datadict_d1['potential'] = potential

        datadict_d2 = self._adj[v].get(u, self.edge_attr_dict_factory())
        datadict_d2.update(attr)
        datadict_d2.update(dd)
        datadict_d2['potential'] = -potential
        
        self._adj[u][v] = datadict_d1
        self._adj[v][u] = datadict_d2
    
    # TODO
    def remove_edge(self, u, v):
        pass

    # TODO
    def remove_edges_from(self, edges):
        pass

    # TODO
    def has_edge(self, u, v):
        pass

    # TODO
    def neighbors(self, u):
        pass

    # TODO
    def edges(self):
        pass

    # TODO
    def clear(self):
        pass

    # TODO
    def clear_edges(self):
        pass

    # TODO
    def number_of_edges(self):
        pass

    # TODO
    def update_potential(self, u, v, potential):
        pass

    # TODO
    def update_outer_potentials(self, u, potentials):
        pass

    # TODO 
    def update_all_potentials(self, potentials):
        pass