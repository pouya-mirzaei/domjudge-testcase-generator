#!/usr/bin/env python3
"""
Custom generator for sorting problem.
This generator creates test cases for a typical sorting problem
where we need to sort an array and perform operations on it.
"""

import random
import os

class Generator:
    """Custom generator for sorting problem"""
    
    def generate_all_cases(self, framework):
        """Generate all test cases for the sorting problem"""
        # Sample test cases
        self.generate_case(framework, 1, {"n": 5, "max_val": 20, "min_val": 1}, is_sample=True)
        self.generate_case(framework, 2, {"n": 10, "max_val": 100, "min_val": 1}, is_sample=True)
        
        # Corner cases
        self.generate_case(framework, 1, {"n": 1, "max_val": 10**9, "min_val": 10**9})
        self.generate_case(framework, 2, {"n": 5, "max_val": 10, "min_val": 10, "pattern": "all_same"})
        
        # Medium test cases
        self.generate_case(framework, 3, {"n": 100, "max_val": 10**5, "min_val": 1})
        self.generate_case(framework, 4, {"n": 1000, "max_val": 10**6, "min_val": 1})
        
        # Large test cases
        self.generate_case(framework, 5, {"n": 10**5, "max_val": 10**9, "min_val": 1})
        self.generate_case(framework, 6, {"n": 2*10**5, "max_val": 10**9, "min_val": 1})
        
        # Specific patterns
        self.generate_case(framework, 7, {"n": 10**4, "max_val": 10**9, "min_val": 1, "pattern": "random"})
        self.generate_case(framework, 8, {"n": 10**4, "max_val": 10**9, "min_val": 1, "pattern": "ascending"})
        self.generate_case(framework, 9, {"n": 10**4, "max_val": 10**9, "min_val": 1, "pattern": "descending"})
        self.generate_case(framework, 10, {"n": 10**4, "max_val": 10**9, "min_val": -10**9, "pattern": "alternating"})
    
    def generate_case(self, framework, case_num, params, is_sample=False):
        """Generate a single test case for the sorting problem"""
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
        n = params.get("n", 10)
        min_val = params.get("min_val", 1)
        max_val = params.get("max_val", 100)
        pattern = params.get("pattern", "random")
        
        # Generate input
        with open(input_file, "w") as f:
            f.write(f"{n}\n")
            
            # Generate array values based on pattern
            if pattern == "random":
                arr = [random.randint(min_val, max_val) for _ in range(n)]
            elif pattern == "ascending":
                arr = sorted([random.randint(min_val, max_val) for _ in range(n)])
            elif pattern == "descending":
                arr = sorted([random.randint(min_val, max_val) for _ in range(n)], reverse=True)
            elif pattern == "all_same":
                arr = [random.randint(min_val, max_val)] * n
            elif pattern == "alternating":
                arr = [random.randint(min_val, 0) if i % 2 == 0 else random.randint(1, max_val) for i in range(n)]
            elif pattern == "almost_sorted":
                arr = sorted([random.randint(min_val, max_val) for _ in range(n)])
                # Swap a few elements to make it almost sorted
                for _ in range(min(5, n // 10)):
                    i, j = random.sample(range(n), 2)
                    arr[i], arr[j] = arr[j], arr[i]
            else:
                arr = [random.randint(min_val, max_val) for _ in range(n)]
            
            f.write(" ".join(map(str, arr)) + "\n")
        
        # Generate output using the C++ solution
        framework.generate_output_from_solution(input_file, output_file)
        
        # Fallback: If the solution fails or if no solution is provided, generate output using Python
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            self.generate_output_with_python(input_file, output_file)
        
        print(f"Generated {'sample' if is_sample else 'secret'} test case {case_num}")
    
    def generate_output_with_python(self, input_file, output_file):
        """Backup method to generate output in Python if C++ solution fails"""
        with open(input_file, "r") as f:
            n = int(f.readline().strip())
            if n == 0:  # Handle empty array case
                arr = []
            else:
                arr = list(map(int, f.readline().strip().split()))
        
        # Sort the array (this is a basic sorting problem)
        arr.sort()
        
        # Write the sorted array to output file
        with open(output_file, "w") as f:
            f.write(" ".join(map(str, arr)) + "\n")
