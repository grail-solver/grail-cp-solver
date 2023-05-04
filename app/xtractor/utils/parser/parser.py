import re
import json
from app.xtractor.utils.llm.gpt import gpt
from app.xtractor.utils.parser.equation import prompt_equation

def parse_text(text):
    # replace newlines and spaces with empty string
    flat_text = text.replace("\n", "").replace(" ", "").replace("(", "").replace(")", "")

    # Define regex patterns for variables and equations
    variable_pattern = r"Variables:{(.*)}"
    equation_pattern = r"Constraints:{(.*)}"

    # Check if the patterns match in the text
    if not re.search(variable_pattern, flat_text, re.DOTALL):
        raise ValueError("Could not find variables in the text")

    if not re.search(equation_pattern, flat_text, re.DOTALL):
        raise ValueError("Could not find equations in the text")

    # Extract the variables and equations from the text
    variables_text = re.search(variable_pattern, flat_text.split('Constraints')[0]).group(1)
    equations_text = re.search(equation_pattern, 'Constraints' + flat_text.split('Constraints')[1]).group(1)

    return variables_text, equations_text


def format_variables(variables_text):
    variables = {}
    for variable_match in re.findall(r"(\w+):{(.+?)}", variables_text):
        variable_name = variable_match[0]
        variable_text = "{" + variable_match[1] + "}"
        variable = eval(variable_text)
        variable['domaine_values'] = eval(variable['domaine_values'])
        variables[variable_name] = variable

    variables_array = [variable for variable in variables.values()]
    return variables_array


def format_constraints(equations_text):
    equation_name_pattern = r'Var_\d+'
    output_pattern = r'"constraints":\s*\[(.*?)\]'

    if not re.search(equation_name_pattern, equations_text, re.DOTALL):
        raise ValueError("Equation name could not match pattern: Var_\d+")

    prompt = prompt_equation
    prompt = prompt.replace('<equation>', equations_text)

    output = gpt(prompt)

    match = re.search(output_pattern, output, re.DOTALL)
    if not match:
        return format_constraints(equations_text)
    else:
        equations = json.loads('{'+output+'}')
    return equations