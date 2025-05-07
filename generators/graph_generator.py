#!/usr/bin/env python3
"""
Custom generator for graph problems.
This generator creates test cases for graph problems like
shortest paths, MST, connectivity, etc.
"""

import random
import os

class Generator:
    """Custom generator for graph problems"""
    
    def generate_all_cases(self, framework):
        """Generate all test cases for the graph problem"""
        # Sample test cases
        self.generate_case(framework, 1, {"n": 5, "m": 7, "graph_type": "undirected"}, is_sample=True)
        self.generate_case(framework, 2, {"n": 7, "m": 10, "graph_type": "undirected", "weights": True}, is_sample=True)
        
        # Corner cases
        self.generate_case(framework, 1, {"n": 1, "m": 0, "graph_type": "undirected"})  # Single node
        self.generate_case(framework, 2, {"n": 2, "m": 1, "graph_type": "undirected"})  # Two nodes, one edge
        
        # Line graph
        self.generate_case(framework, 3, {"n": 50, "graph_type": "line"})
        
        # Tree
        self.generate_case(framework, 4, {"n": 100, "graph_type": "tree"})
        
        # Complete graph
        self.generate_case(framework, 5, {"n": 20, "graph_type": "complete", "weights": True})
        
        # Dense graph
        self.generate_case(framework, 6, {"n": 1000, "m": 10000, "graph_type": "undirected", "weights": True})
        
        # Sparse graph
        self.generate_case(framework, 7, {"n": 10000, "m": 15000, "graph_type": "undirected"})
        
        # Maximum constraints
        self.generate_case(framework, 8, {"n": 100000, "m": 200000, "graph_type": "undirected"})
        
        # Directed graph
        self.generate_case(framework, 9, {"n": 1000, "m": 5000, "graph_type": "directed", "weights": True})
        
        # Bipartite graph
        self.generate_case(framework, 10, {"n": 500, "graph_type": "bipartite", "weights": True})
    
    def generate_case(self, framework, case_num, params, is_sample=False):
        """Generate a single test case for a graph problem"""
        # Determine which directory to use
        case_dir = framework.sample_dir if is_sample else framework.secret_dir
        
        # Set up file paths
        if is_sample:
            base_name = f"sample-{case_num}"
        else:
            base_name = f"secret-{case_num}"
        
        input_file = os.path.join(case_dir, f"{base_name}.in")
        output_file = os.path.join(case_dir, f"{base_name}.ans")
        
        # Extract parameters with defaults
        n = params.get("n", 10)  # Number of nodes
        m = params.get("m", None)  # Number of edges (optional)
        graph_type = params.get("graph_type", "undirected")
        weights = params.get("weights", False)  # Whether edges have weights
        min_weight = params.get("min_weight", 1)
        max_weight = params.get("max_weight", 1000)
        
        # Generate graph based on type
        edges = []
        
        if graph_type == "line":
            # Line graph: n-1 edges connecting nodes in sequence
            edges = [(i, i+1) for i in range(1, n)]
            m = n - 1
            
        elif graph_type == "tree":
            # Random tree: n-1 edges forming a tree
            edges = []
            # Start with node 1
            connected = {1}
            remaining = set(range(2, n+1))
            
            # Add n-1 edges to form a tree
            while remaining:
                u = random.choice(list(connected))
                v = random.choice(list(remaining))
                edges.append((u, v))
                connected.add(v)
                remaining.remove(v)
            m = n - 1
            
        elif graph_type == "complete":
            # Complete graph: all possible edges
            edges = [(i, j) for i in range(1, n+1) for j in range(i+1, n+1)]
            m = n * (n - 1) // 2
            
        elif graph_type == "bipartite":
            # Bipartite graph: two parts with random connections
            part1_size = n // 2
            part1 = list(range(1, part1_size + 1))
            part2 = list(range(part1_size + 1, n + 1))
            
            # Generate random edges between parts
            m = min(m or (n * 3), len(part1) * len(part2))
            possible_edges = [(u, v) for u in part1 for v in part2]
            edges = random.sample(possible_edges, m)
            
        else:  # "undirected" or "directed"
            # If m is not specified, create a reasonably connected graph
            if m is None:
                m = min(n * 2, n * (n - 1) // 2)  # 2*n edges or complete graph if n is small
                
            # Generate random edges
            if graph_type == "directed":
                # For directed graph
                possible_edges = [(i, j) for i in range(1, n+1) for j in range(1, n+1) if i != j]
                m = min(m, len(possible_edges))
                edges = random.sample(possible_edges, m)
            else:
                # For undirected graph
                possible_edges = [(i, j) for i in range(1, n+1) for j in range(i+1, n+1)]
                m = min(m, len(possible_edges))
                edges = random.sample(possible_edges, m)
        
        # Add weights if needed
        if weights:
            edges = [(u, v, random.randint(min_weight, max_weight)) for u, v in edges]
        
        # Write to input file
        with open(input_file, "w") as f:
            f.write(f"{n} {m}\n")
            
            for edge in edges:
                if weights:
                    u, v, w = edge
                    if graph_type == "directed":
                        f.write(f"{u} {v} {w}\n")
                    else:
                        f.write(f"{u} {v} {w}\n")
                else:
                    u, v = edge
                    if graph_type == "directed":
                        f.write(f"{u} {v}\n")
                    else:
                        f.write(f"{u} {v}\n")
        
        # Generate output using the C++ solution
        framework.generate_output_from_solution(input_file, output_file)
        
        print(f"Generated {'sample' if is_sample else 'secret'} test case {case_num}")
