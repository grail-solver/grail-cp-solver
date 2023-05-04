from ortools.sat.python import cp_model
import numpy as np
import ast

class AllSolutionsPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__all_solutions = []

    def on_solution_callback(self):
        self.__solution_count += 1
        one_solution = []
        for variable in self.__variables:
            one_solution.append(
                {
                    'var_name': variable.Name(),
                    'value': self.Value(variable)
                }
            )
        self.__all_solutions.append(one_solution)
        if self.__solution_count >= 100:
            self.StopSearch()
    
    @property
    def all_solutions(self):
        return self.__all_solutions


def get_optimal_solutions(solver, model, all_variables):
    status = solver.Solve(model)
    opt_solution = []
    if status == cp_model.OPTIMAL:
        for var in all_variables:
            opt_solution.append({
                'var_name': var.Name(),
                'value': solver.Value(var)
            })
        opt_solution.append({
            'objective_value': solver.ObjectiveValue()
        })
        return opt_solution        
    else:
        return 'No solution found'
    
    
def main(variables, constraints, optimization):
    model = cp_model.CpModel()
    if not model:
        return
    
    optimize = False
    all_variables = []

    for var in variables:
        all_variables.append(add_variable(var, model))
    print("Variables OK")
    for ct in constraints:
        add_constraint(ct, model, all_variables)
    print("Constraints OK")
    
    if(len(optimization) > 0):
        optimize = True
        for opt in optimization:
            add_optimization_constraint(opt, model, all_variables)
            
            
    return model, all_variables, optimize


def add_variable(variable, model):
    upper_bound = 1000
    if (variable["type"] == "Integer"):
        if (variable["domaine_type"] == "INTERVAL"):
            if type(variable['domaine_values']) == str:
                domaine_values = ast.literal_eval(variable["domaine_values"])
            else:
                domaine_values = variable["domaine_values"]
            print(domaine_values)
            if len(domaine_values) <=1:
                return model.NewIntVar(domaine_values[0], upper_bound, variable["name"])
            else:
                first = upper_bound if domaine_values[0] == "inf" else int(domaine_values[0])
                last = upper_bound if domaine_values[1] == "inf" else int(domaine_values[1])
                return model.NewIntVar(first, last, variable["name"])
            
    elif (variable["type"] == "Float"):
        if (variable["domaine_type"] == "INTERVAL"):
            scale_factor = 10 # The precision we want the variable has, here it will be one digit after the comma.
            if type(variable['domaine_values']) == str:
                domaine_values = ast.literal_eval(variable["domaine_values"])
            else:
                domaine_values = variable["domaine_values"]
            if len(domaine_values) <=1:
                return model.NewIntVar(domaine_values[0], upper_bound, variable["name"])
            else:
                first = upper_bound if domaine_values[0] == "-" else int(domaine_values[0] * scale_factor)
                last = upper_bound if domaine_values[1] == "-" else int(domaine_values[1] * scale_factor)
                int_var = model.NewIntVar(first, last, variable["name"])
                return int_var / scale_factor


def add_constraint(constraint, model, all_variables):
    left_exp = convert_litteral_expression(constraint["left_part"], all_variables)
    right_exp = convert_litteral_expression(constraint["right_part"], all_variables)
    if constraint["relation"] == "<=":
        model.Add(left_exp <= right_exp)
    elif constraint["relation"] == ">=":
        model.Add(left_exp >= right_exp)
    elif constraint["relation"] == "<":
        model.Add(left_exp < right_exp)
    elif constraint["relation"] == ">":
        model.Add(left_exp > right_exp)
    elif constraint["relation"] == "!=":
        model.Add(left_exp != right_exp)
    elif constraint["relation"] == "==":
        model.Add(left_exp - right_exp == 0)


def add_optimization_constraint(opt_ct, model, all_variables):
    exp = convert_litteral_expression(opt_ct["exp"], all_variables)
    if(opt_ct["type"] == "MAXIMIZE"):
        model.Maximize(exp)
    else:
        model.Minimize(exp)
    

def convert_litteral_expression(litt_exp, all_variables):
    convert_exp = 0
    list_of_operators = ["+", "-", "*", "/"]
    previous_operator = ""
    for exp in litt_exp :
        if not previous_operator:
            if type(exp) == list:
                if len(exp) <= 1:
                    convert_exp+= all_variables[get_variable_id(exp[0])]
                else:
                    print('Here')
                    print(exp)
                    convert_exp+= exp[0] * all_variables[get_variable_id(exp[1])]
                    print('OK')

            elif exp in list_of_operators:
                previous_operator = exp
            else:
                try:
                    convert_exp+= int(exp)
                except Exception:
                    convert_exp+= all_variables[get_variable_id(exp)]
        else:
            if type(exp) == list:
                coef = 1
                var_name = ""
                if len(exp) <= 1:
                    var_name = exp[0]
                else:
                    coef = exp[0]
                    var_name = exp[1]

                if previous_operator == "+":
                    convert_exp+= coef * all_variables[get_variable_id(var_name)]
                elif previous_operator == "-":
                    convert_exp-= coef * all_variables[get_variable_id(var_name)]
                elif previous_operator == "*":
                    convert_exp*= coef * all_variables[get_variable_id(var_name)]
                elif previous_operator == "/":
                    convert_exp/= coef * all_variables[get_variable_id(var_name)]

            elif exp in list_of_operators:
                previous_operator = exp
            else:
                try:
                    value = int(exp)
                except Exception:
                    value = all_variables[get_variable_id(exp)]
                if previous_operator == "+":
                    convert_exp+= value
                elif previous_operator == "-":
                    convert_exp-= value
                elif previous_operator == "*":
                    convert_exp*= value
                elif previous_operator == "/":
                    convert_exp/= value

    return convert_exp


def get_variable_id(variable_name):
    var_id = variable_name.split("_")[1]
    return int(var_id)-1

def get_variable_name(var_denom, all_vars):
    var_id = int(var_denom.split("_")[1]) -1
    return all_vars[var_id].Name()


def get_variables(model):
    model_proto = model.Proto()
    variables = []
    for var_proto in model_proto.variables:
        var_name = var_proto.name
        variables.append({'var_name': var_name, 'var_domain': list(var_proto.domain)})
    return variables

def get_constraints(constraints, all_vars):
    constraint_strings = []
    for constraint in constraints:
        left_part = ""
        right_part = ""
        for term in constraint['left_part']:
            if isinstance(term, list):
                left_part += f"{term[0]}*{get_variable_name(term[1], all_vars)}"
            else:
                left_part += str(term)
            left_part += " "
        
        for term in constraint['right_part']:
            if isinstance(term, list):
                right_part += f"{term[0]}*{get_variable_name(term[1], all_vars)}"
            else:
                right_part += str(term)
            right_part += " "

        constraint_strings.append(f"{left_part} {constraint['relation']} {right_part}")

    return constraint_strings


def solve(variables, constraints, optimization):
    model, all_var, with_opt = main(variables, constraints, optimization)
    solver = cp_model.CpSolver()

    if with_opt:
        return get_optimal_solutions(solver, model, all_var)
    else:
        solver.parameters.enumerate_all_solutions = True
        all_solutions_printer = AllSolutionsPrinter(all_var)
        solver.Solve(model, all_solutions_printer)
        formatted_vars = get_variables(model)
        formatted_ct = get_constraints(constraints, all_var)

        return all_solutions_printer.all_solutions, formatted_vars, formatted_ct