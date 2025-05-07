#!/usr/bin/env python3
import os
import random
import argparse
import subprocess
import shutil
import tempfile
import importlib.util
import sys

class DOMjudgeTestGenerator:
    """
    A flexible test case generator for competitive programming contests that follows DOMjudge format.
    This framework can be extended for different problem types.
    """
    def __init__(self, problem_id, solution_file, generator_module=None):
        self.problem_id = problem_id
        self.solution_file = solution_file
        self.generator_module = generator_module
        
        # Create DOMjudge directory structure
        self.base_dir = f"{problem_id}"
        self.data_dir = os.path.join(self.base_dir, "data")
        self.sample_dir = os.path.join(self.data_dir, "sample")
        self.secret_dir = os.path.join(self.data_dir, "secret")
        
        # Create directories if they don't exist
        for directory in [self.base_dir, self.data_dir, self.sample_dir, self.secret_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Compile the solution if it's C++
        self.executable = None
        if solution_file.endswith(".cpp"):
            self.compile_solution()
            
        # Load custom generator module if provided
        self.generator = None
        if generator_module:
            self.load_generator_module(generator_module)
    
    def compile_solution(self):
        """Compile the C++ solution"""
        compiled_name = os.path.join(tempfile.gettempdir(), f"{self.problem_id}_solution")
        try:
            subprocess.run(
                ["g++", "-std=c++17", "-O2", self.solution_file, "-o", compiled_name],
                check=True,
                stderr=subprocess.PIPE
            )
            self.executable = compiled_name
            print(f"Successfully compiled {self.solution_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling solution: {e.stderr.decode()}")
            exit(1)
    
    def load_generator_module(self, module_path):
        """Load a custom Python module that defines test case generation logic"""
        try:
            spec = importlib.util.spec_from_file_location("generator_module", module_path)
            generator_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(generator_module)
            
            # The module should have a Generator class
            if hasattr(generator_module, "Generator"):
                self.generator = generator_module.Generator()
            else:
                print(f"Error: {module_path} does not contain a Generator class")
                exit(1)
                
            print(f"Successfully loaded generator module: {module_path}")
        except Exception as e:
            print(f"Error loading generator module: {e}")
            exit(1)
    
    def generate_all_cases(self):
        """
        Generate all test cases by delegating to the custom generator module if available,
        or using the default generation logic otherwise.
        """
        if self.generator and hasattr(self.generator, "generate_all_cases"):
            # Use custom generator
            self.generator.generate_all_cases(self)
        else:
            # Use default generation logic
            print("Warning: No custom generator provided. Using default test case generation.")
            print("For complex problems, consider creating a custom generator module.")
            self.default_generate_all_cases()
    
    def default_generate_all_cases(self):
        """Default implementation for test case generation"""
        # Generate sample test cases (visible to contestants)
        self.generate_case(1, params={"small": True}, is_sample=True)
        self.generate_case(2, params={"small": True}, is_sample=True)
        
        # Generate secret test cases (hidden from contestants)
        # Corner cases
        self.generate_case(1, params={"corner_case": True})
        self.generate_case(2, params={"corner_case": True, "type": "min"})
        
        # Medium test cases
        self.generate_case(3, params={"size": "medium"})
        self.generate_case(4, params={"size": "medium", "pattern": "random"})
        
        # Large test cases
        self.generate_case(5, params={"size": "large"})
        self.generate_case(6, params={"size": "max", "pattern": "worst_case"})
        
        # Test cases with specific patterns
        self.generate_case(7, params={"size": "large", "pattern": "random"})
        self.generate_case(8, params={"size": "large", "pattern": "special"})
        
        print(f"Generated test cases in directory: {self.base_dir}")
        print(f"- Sample cases: {self.sample_dir}")
        print(f"- Secret cases: {self.secret_dir}")
    
    def generate_case(self, case_num, params=None, is_sample=False):
        """
        Generate a single test case with input and output files.
        Delegates to custom generator if available, otherwise uses default_generate_case.
        
        Args:
            case_num: Test case number
            params: Dictionary of parameters for test case generation
            is_sample: Whether this is a sample test case
        """
        if self.generator and hasattr(self.generator, "generate_case"):
            # Use custom generator
            self.generator.generate_case(self, case_num, params, is_sample)
        else:
            # Use default implementation
            self.default_generate_case(case_num, params, is_sample)
    
    def default_generate_case(self, case_num, params=None, is_sample=False):
        """
        Default implementation for generating a single test case.
        This should be overridden by problem-specific generators.
        """
        # Determine which directory to use
        case_dir = self.sample_dir if is_sample else self.secret_dir
        
        # Set up file paths
        if is_sample:
            # Sample cases use format: sample-<testid>.in, sample-<testid>.ans
            base_name = f"sample-{case_num}"
        else:
            # Secret cases use format: secret-<testid>.in, secret-<testid>.ans
            base_name = f"secret-{case_num}"
        
        input_file = os.path.join(case_dir, f"{base_name}.in")
        output_file = os.path.join(case_dir, f"{base_name}.ans")
        
        # Default parameters
        params = params or {}
        size = params.get("size", "small")
        pattern = params.get("pattern", "random")
        
        # Generate a simple input file (this should be overridden for specific problems)
        with open(input_file, "w") as f:
            f.write("This is a placeholder test case.\n")
            f.write(f"You should implement a custom generator for problem {self.problem_id}.\n")
            f.write(f"Parameters: {params}\n")
        
        # Generate output by running the solution
        if self.executable:
            self.generate_output_from_solution(input_file, output_file)
        
        print(f"Generated {'sample' if is_sample else 'secret'} test case {case_num}")
    
    def generate_output_from_solution(self, input_file, output_file):
        """Generate output by running the compiled solution"""
        try:
            with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
                subprocess.run(
                    [self.executable],
                    stdin=infile,
                    stdout=outfile,
                    check=True,
                    timeout=10  # 10 second timeout to prevent hanging
                )
        except subprocess.TimeoutExpired:
            print(f"Warning: Solution timed out on {input_file}.")
            # Create an empty output file
            open(output_file, 'w').close()
        except subprocess.CalledProcessError as e:
            print(f"Error running solution on {input_file}: {e}")
            # Create an empty output file
            open(output_file, 'w').close()


def main():
    parser = argparse.ArgumentParser(description='Generate DOMjudge-compatible test cases')
    parser.add_argument('problem_id', type=str, help='Problem ID or name')
    parser.add_argument('solution_file', type=str, help='Path to the solution file (C++)')
    parser.add_argument('--generator', type=str, help='Path to a custom generator module (Python)')
    
    args = parser.parse_args()
    
    generator = DOMjudgeTestGenerator(
        problem_id=args.problem_id,
        solution_file=args.solution_file,
        generator_module=args.generator
    )
    generator.generate_all_cases()

if __name__ == "__main__":
    main()
