from ortools.sat.python import cp_model
import numpy as np

class AllSolutionsPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, solver):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solver = solver
        self.__solution_count = 0
        self.__all_solutions = []

    def on_solution_callback(self):
        self.__solution_count += 1
        print('Solution %i:' % self.__solution_count)
        for variable in self.__variables:
            self.__all_solutions.append(
                {
                    'var_name': variable.Name(),
                    'value': self.__solver.Value(variable)
                }
            )
            # print('%s = %i' % (variable.Name(), self.Value(variable)))


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
            'Objective value': solver.ObjectiveValue()
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
    variable_list = [[v.id, v.name, v.type, v.domain_type, v.domain_value, v.problem_id] for v in variables]
    variable_dict_list = [dict(zip(['id', 'name', 'type', 'domain_type', 'domain_value', 'problem_id'], v)) for v in variable_list]

    for var in variable_dict_list:
        all_variables.append(add_variable(var, model))

    ct_list = [[ct.left_part, ct.right_part, ct.metric] for ct in constraints]
    ct_dict_list = [dict(zip(['left_part', 'right_part', 'metric'], ct)) for ct in ct_list]
    for ct in ct_dict_list:
        add_constraint(ct, model, all_variables)
    
    opt_list = [[opt.exp, opt.type] for opt in optimization]
    opt_dict_list = [dict(zip(['exp', 'type'], opt)) for opt in opt_list]
    if(len(opt_dict_list) > 0):
        optimize = True
        for opt in opt_dict_list:
            add_optimization_constraint(opt, model, all_variables)
            
            
    return model, all_variables, optimize


def add_variable(variable, model):
    if (variable["type"][0] == "INTEGER"):
        if (variable["domain_type"][0] == "INTERVAL"):
            domain_value = variable["domain_value"][0]
            first = np.NINF if domain_value[0] == "-" else int(domain_value[0])
            last = np.Inf if domain_value[1] == "-" else int(domain_value[1])
            return model.NewIntVar(first, last, variable["name"][0])


def add_constraint(constraint, model, all_variables):
    left_exp = convert_litteral_expression(constraint["left_part"], all_variables)
    right_exp = convert_litteral_expression(constraint["right_part"], all_variables)
    if constraint["metric"] == "<=":
        model.Add(left_exp <= right_exp)
    elif constraint["metric"] == ">=":
        model.Add(left_exp >= right_exp)
    elif constraint["metric"] == "<":
        model.Add(left_exp < right_exp)
    elif constraint["metric"] == ">":
        model.Add(left_exp > right_exp)
    elif constraint["metric"] == "!=":
        model.Add(left_exp != right_exp)
    elif constraint["metric"] == "==":
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
                convert_exp+= exp[0] * all_variables[get_variable_id(exp[1])]
            elif exp in list_of_operators:
                previous_operator = exp
            else:
                convert_exp+= exp
        else:
            if type(exp) == list:
                if previous_operator == "+":
                    convert_exp+= exp[0] * all_variables[get_variable_id(exp[1])]
                elif previous_operator == "-":
                    convert_exp-= exp[0] * all_variables[get_variable_id(exp[1])]
                elif previous_operator == "*":
                    convert_exp*= exp[0] * all_variables[get_variable_id(exp[1])]
                elif previous_operator == "/":
                    convert_exp/= exp[0] * all_variables[get_variable_id(exp[1])]

            elif exp in list_of_operators:
                previous_operator = exp
            else:
                if previous_operator == "+":
                    convert_exp+= exp
                elif previous_operator == "-":
                    convert_exp-= exp
                elif previous_operator == "*":
                    convert_exp*= exp
                elif previous_operator == "/":
                    convert_exp/= exp

    return convert_exp


def get_variable_id(variable_name):
    var_id = variable_name.split("_")[1]
    return int(var_id)


def solve(variables, constraints, optimization):
    model, all_var, with_opt = main(variables, constraints, optimization)
    solver = cp_model.CpSolver()

    if with_opt:
        return get_optimal_solutions(solver, model, all_var)
    else:
        all_solutions_printer = AllSolutionsPrinter(all_var, solver)
        solver.SearchForAllSolutions(model, all_solutions_printer)
        print(all_solutions_printer.__all_solutions)
        return all_solutions_printer.__all_solutions