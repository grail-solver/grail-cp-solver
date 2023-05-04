from app.xtractor.utils.protocol.prompt_builder import prompt, error_prompt
from app.xtractor.utils.parser import parser
from app.xtractor.utils.llm.gpt import gpt

"""
Edit the value of this variable to define how many try can be done when error occur
"""
REQUEST_ATTEMPTS = 1


def grail_extractor(problem: str, error: str = '', tries: int = 0):
    if error:
        formatted_prompt = error_prompt.replace('<problem>', problem)
        formatted_prompt = formatted_prompt.replace('<error>', error)
    else:
        formatted_prompt = prompt.replace('<problem>', problem)

    # Extract data using GPT-LLM
    output = gpt(formatted_prompt)

    # Parse output
    try:
        variables_text, equations_text = parser.parse_text(output)
        variables = parser.format_variables(variables_text)
        equations = parser.format_constraints(equations_text)

        equations['variables'] = variables
        equations['llm_status'] = 'success'

        return equations
    except Exception as e:
        print("Error:", e)
        if tries < REQUEST_ATTEMPTS:
            # Recursively call function with added error message
            return grail_extractor(problem, str(e), tries+1)
        else:
            return {"llm_status": 'fail', "llm_trace": str(e)}
