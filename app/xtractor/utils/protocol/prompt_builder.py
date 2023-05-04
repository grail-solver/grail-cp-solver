import os

# Read variable files and build variable structure
variables = ""
variables_path = os.path.join('app', 'xtractor', 'utils', 'protocol', 'variables')

for filename in os.listdir(variables_path):
    with open(f"{variables_path}/{filename}", "r") as f:
        variables += f.read() + "\n"
variable_struct = f"{variables}"

# Read constraint files and build constraint structure
constraints = ""
constraints_path = os.path.join('app','xtractor', 'utils', 'protocol', 'constraints')

for filename in os.listdir(constraints_path):
    with open(f"{constraints_path}/{filename}", "r") as f:
        constraints += f.read() + "\n"
constraint_struct = f"{constraints}"

# Build prompt
prompt = f"Analyzes this constraint satisfaction problem, then extracts the variables and constraints: '<problem>'. The variables must be encoded on this way: '{variable_struct}' and the constraints on this way '{constraint_struct}'"
error_prompt = f"Analyzes this constraint satisfaction problem, then extracts the variables and constraints: '<problem>'. The variables must be encoded on this way: '{variable_struct}' and the constraints on this way '{constraint_struct}'. Retry as the current execution do not match the protocol causing this error : <error>"
