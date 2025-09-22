import numpy as np

"""
Description
"""

class MagGraph:
    """
    Base class for magnetic graphs.
    
    A magnetic graph stoores the nodes and edges with optional data. The edges are considered directed, but we have the two directions for each edge. Also, we have a potential function that assigns a value between 0 and 2pi to each edge. 

    Self-loops are allowed but multiedges are not. The only restriction for nodes is tha they must be a hashable python object.

    Parameters
    ----------

    See Also
    --------
        · https://arxiv.org/?????? A survey on Magnetic Graphs
    
    Examples
    --------
        >>> from magnetwork.core import MagGraph
        >>> G = MagGraph(n=3, edges=[(0, 1), (1, 2)], potential={0: 0, 1: np.pi/2, 2: np.pi})
        >>> print(G.n_nodes)
        3
        >>> print(G.edges)
        [(0, 1), (1, 2)]
        >>> print(G.potential)
        {0: 0, 1: 1.5707963267948966, 2: 3.141592653589793}
    """

    def __init__(self, n:int = 0, edges: list = None, potential: dict = None):
        r"""
        Initialize a magnetic graph.
        """
        self.n_nodes = n
        self.edges = edges if edges is not None else []
        self.nodes_d = {i: [] for i in range(n)}
        self.potential = potential if potential is not None else {i: 0 for i in range(n)}

r"""
    TODO
    - Write a structure that we want (atributes, methods, etc)
    - Build subclasses for Laplacian, Adjacency, etc.
    - Build methods for:
        - Adding/removing nodes/edges
        - Getting neighbors
        - Getting degree
        - Getting adjacency matrix
        - Getting Laplacian matrix
        - Getting eigenvalues/eigenvectors
        - Adding weights
    - Define GSP functions and pooling methods
    - Write docstrings
    - Implement methods
    - Write tests
"""

    pass