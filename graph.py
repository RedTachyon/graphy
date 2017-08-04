from random import random, choice
from time import time


class Graph:
    '''
    Example of usage:
    
    graph = Graph(500, 4)
    graph.WS_model(0.5)
    '''
    
    def __init__(self, num_nodes, mean_deg=2):
        '''Class containing information about a single graph, mainly for the WS small world model'''
        self.size = num_nodes
        self.N = num_nodes
        self.K = mean_deg
        self.nodes = list(range(num_nodes))
        self.edge_dict = {n: [] for n in self.nodes}
        self.edges = []
        
    def degree(self, node):
        assert node in self.nodes
        if node in self.edge_dict:
            return len(self.edge_dict[node])
        else:
            return 0
    
    def _edges_to_edge_dict(self):
        '''Changes the dict representation of edges to fit the list representation'''
        edge_dict = {}
        for i, j in self.edges:
            self._add_to_dict(edge_dict, i, j)
            self._add_to_dict(edge_dict, j, i)
        
        self.edge_dict = edge_dict
        
    def _edge_dict_to_edges(self):
        '''Changes the list representation of edges to fit the dict representation'''
        edges = []
        for i in self.edge_dict:
            for j in self.edge_dict[i]:
                n1, n2 = i, j
                if (n1, n2) not in edges and (n2, n1) not in edges:
                    edges.append((n1,n2))
        self.edges = edges
        
    def _add_to_dict(self, dic, key, value):
        '''Adds value as part of dic[key], hopefully type(dic[key]) == list'''
        if key in dic:
            if value not in dic[key]:
                dic[key].append(value)
        else:
            dic[key] = [value]
            
    def add_edge(self, n1, n2):
        '''Adds edge n1-n2 to list and dict'''
        self.check(n1, n2)
        
        self._add_to_dict(self.edge_dict, n1, n2)
        self._add_to_dict(self.edge_dict, n2, n1)
        
        if (n1, n2) not in self.edges and (n2, n1) not in self.edges:
            self.edges.append((n1,n2))
    
    def remove_edge(self, n1, n2):
        '''Removes edge n1-n2 from list and dict'''
        self.check(n1, n2)
        assert (n1,n2) in edges or (n2,n1) in edges
        if (n1,n2) in self.edges:
            self.edges.remove((n1,n2))
        elif (n2,n1) in self.edges:
            self.edges.remove((n2,n1))
        self.edge_dict[n1].remove(n2)
        self.edge_dict[n2].remove(n1)
        
        
    def check(self, *args):
        '''Checks if all arguments are nodes'''
        for n in args:
            assert n in self.nodes
    
    def _WS_check(self, n1, n2):
        '''Checks if nodes n1, n2 should be connected in the first step of WS model'''
        self.check(n1, n2)
        mod = (self.N - 1 - (self.K/2))
        
        return ((abs(n1 - n2) % mod) <= (self.K / 2)) and ((abs(n1-n2) % mod) > 0)

    def _swap_connection(self, n1, n2, n3):
        '''Swaps n1-n2 edge to n1-n3 edge'''
        if (n1, n2) in self.edges:
            self.edges.remove((n1,n2))
            self.edges.append((n1,n3))
        elif (n2, n1) in self.edges:
            self.edges.remove((n2,n1))
            self.edges.append((n1,n3))
       
        self._edges_to_edge_dict()
        
    def _prepare_copy_nodes(self, n1):
        '''Returns a copy of the list of nodes, excluding n1 and all its neighbours'''
        temp_nodes = self.nodes[:]
        temp_nodes.remove(n1)
        for n2 in self.edge_dict[n1]:
            temp_nodes.remove(n2)
        return temp_nodes
    
    def _slow_base_WS(self):
        '''Creates edges for the base WS model'''
        assert len(self.edges) == 0
        
        for i in self.nodes:
            for j in self.nodes:
                if self._WS_check(i,j):
                    self.add_edge(i,j)
                    
    def _base_WS(self):
        '''Creates edges for the base WS model, hopefully more efficiently'''
        assert len(self.edges) == 0
        
        for n in self.nodes:
            for k in range(-self.K//2, self.K//2):
                if k != 0:
                    self.add_edge(n, (n + k) % self.N)
            
                    
    def _rewire_WS(self, prob, debug=False):
        '''Rewires edges to create the small world structure'''
        assert prob >= 0
        assert prob <= 1
        
        temp_edges = self.edges[:]
        for i in self.nodes[:-1]:
            for j in self.edge_dict[i]:
                if i < j:
                    if debug: print('Considering edge %d%d' % (i,j));
                    test = random()
                    if test < prob:
                        copy_nodes = self._prepare_copy_nodes(i)
                        k = choice(copy_nodes)
                        if debug: print('Swapping edge %d%d for %d%d \n' % (i,j,i,k));
                        self._swap_connection(i, j, k)
        
        
    def WS_model(self, prob, debug=False, timed=False):
        '''Turns an empty graph into a small worlds graph'''
        if timed:
            start = time()
        assert len(self.edges) == 0
        self._base_WS()
        if timed:
            step = time()
        self._rewire_WS(prob, debug)
        if timed:
            end = time()
            print('Time for base: %f, time for rewire: %f' % (step - start, end - step))
            return end-step
        
        
    def dijkstra(self, initial):
        visited = {initial: 0}
        path = {}
        
        nodes = set(self.nodes)
        
        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break
            
            nodes.remove(min_node)
            current_weight = visited[min_node]
            
            for edge in self.edge_dict[min_node]:
                weight = current_weight + 1
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node
                    
        return visited, path
    
    def all_distances(self):
        all_distances = {}
        for node in self.nodes:
            distances, _ = self.dijkstra(node)
            for node2 in distances:
                if (node, node2) not in all_distances and (node2, node) not in all_distances:
                    all_distances[(node, node2)] = distances[node2]
                    
        return all_distances