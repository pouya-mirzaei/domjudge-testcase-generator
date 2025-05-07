# Test Case Generator Framework for Competitive Programming Contests

This framework helps you generate test cases for competitive programming problems in the DOMjudge format. It's designed to be flexible and easily adaptable to different problem types.

## Key Features

- Creates the correct directory structure for DOMjudge
- Supports both C++ and Python solution files to generate expected outputs
- Supports custom generator modules for different problem types
- Provides sample generators for common problem types

## Basic Usage

```bash
python test_case_generator.py problem_id solution.cpp --generator custom_generator.py
```

or with a Python solution:

```bash
python test_case_generator.py problem_id solution.py --generator custom_generator.py
```

This will:

1. Create a `problem_id` directory with DOMjudge structure
2. Compile your C++ solution file (if using C++) or use your Python solution directly
3. Use the custom generator module to create test cases
4. Run your solution on each test case to generate the expected outputs

## Directory Structure

The framework creates the following directory structure:

```
problem_id/
├── data/
│   ├── sample/    (visible to contestants)
│   │   ├── sample-1.in
│   │   ├── sample-1.ans
│   │   └── ...
│   └── secret/    (hidden from contestants)
│       ├── secret-1.in
│       ├── secret-1.ans
│       └── ...
```

## Creating Custom Generators

To create a custom generator for a specific problem type:

1. Create a Python file with a `Generator` class
2. Implement `generate_all_cases` and `generate_case` methods
3. Pass it to the framework using the `--generator` flag

Example of a minimal custom generator:

```python
class Generator:
    def generate_all_cases(self, framework):
        # Generate sample cases
        self.generate_case(framework, 1, {"n": 5}, is_sample=True)
        # Generate secret cases
        self.generate_case(framework, 1, {"n": 100})

    def generate_case(self, framework, case_num, params, is_sample=False):
        # Determine case directory and paths
        case_dir = framework.sample_dir if is_sample else framework.secret_dir
        if is_sample:
            base_name = f"sample-{case_num}"
        else:
            base_name = f"secret-{case_num}"

        input_file = os.path.join(case_dir, f"{base_name}.in")
        output_file = os.path.join(case_dir, f"{base_name}.ans")

        # Generate input according to problem specification
        with open(input_file, "w") as f:
            # Write problem-specific test case
            # ...

        # Generate output using the solution
        framework.generate_output_from_solution(input_file, output_file)
```

## Provided Generator Templates

The following generator templates are provided:

1. **Binary Search Problem Generator**: For counting elements less than or equal to queries
2. **Sorting Problem Generator**: For sorting arrays with various patterns
3. **Graph Problem Generator**: For generating graphs (undirected, directed, trees, etc.)

## Extending the Framework

You can easily create new generators for different problem types:

1. Copy one of the existing generators as a starting point
2. Modify the `generate_case` method to create test cases for your specific problem
3. Add your own parameters and test case generation logic

## Parameters for Test Case Generation

You can customize test cases using parameters. Common parameters include:

- `n`, `m`: Size parameters (array length, number of nodes, edges, etc.)
- `min_val`, `max_val`: Range for random values
- `pattern`: Specific patterns (e.g., "random", "ascending", "tree", etc.)
- Problem-specific parameters for your custom logic
