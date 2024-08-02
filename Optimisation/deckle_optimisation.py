from Utils.utils import array_to_dict, compare_dict_values
from pulp import *

# to find out if repetition of deckle is possible
def get_repetitive_deckle(final_list_deckle, optimised_deckle, number_dict):
    while True:
        optimised_dict = array_to_dict(optimised_deckle)
        result = compare_dict_values(optimised_dict, number_dict)
        if result:
            final_list_deckle.append(optimised_deckle)
            for key in optimised_dict:
                number_dict[key] = number_dict[key] - optimised_dict[key]
        else:
            break

    return final_list_deckle, number_dict

def get_repetitive_deckle_optional(final_list_deckle, optimised_deckle, option_and_must_dict, residual_dict):
    while True:
        optimised_dict = array_to_dict(optimised_deckle)
        result = compare_dict_values(optimised_dict, option_and_must_dict)
        if result:
            final_list_deckle.append(optimised_deckle)
            for key in optimised_dict:
                option_and_must_dict[key] = option_and_must_dict[key] - optimised_dict[key]
                if key in residual_dict:
                    if residual_dict[key] >= optimised_dict[key]:
                        residual_dict[key] = residual_dict[key] - optimised_dict[key]
                    else:
                        residual_dict[key] = 0
        else:
            break

    return final_list_deckle, option_and_must_dict, residual_dict
# to combine optional deckles and complete residual must make deckles planning
def get_combined_optional_must_make(residual_dict, must_make_values, optional_values, optional_number_dict):
    option_and_must_dict = residual_dict.copy()
    option_and_must_values = must_make_values.copy()
    for key in optional_number_dict.keys():
        if key in option_and_must_dict.keys():
            option_and_must_dict[key] += optional_number_dict[key]
        else:
            option_and_must_dict[key] = optional_number_dict[key]
    for i in optional_values:
        if i not in must_make_values:
            option_and_must_values.append(i)
    return option_and_must_dict, option_and_must_values


def optimise_residual_deckle(values, option_and_must_dict, residual_dict, position, max_width, min_arms,
                             final_list_deckle):
    min_repetitions = 3
    while True:
        optimised_deckle = []
        prob = LpProblem("Deckle_Problem", LpMinimize)
        choices = LpVariable.dicts("Choice", (position, values), cat="Binary")
        obj_value = LpVariable("obj_value", lowBound=0, cat="Continuous")
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position)
        # A constraint to ensure obj value is the maximum of the number of times the value comes divided by the total number of values in dictionary for all values
        for v in values:
            if v in residual_dict and residual_dict.get(v) > 0:
                prob += lpSum(choices[p][v] for p in position) / residual_dict.get(v) <= 1/min_repetitions
        prob += lpSum(choices[p][v] for p in position for v in residual_dict.keys()) >= 1
        for p in position:
            if p <= min_arms:
                prob += lpSum([choices[p][v] for v in values]) == 1
            else:
                prob += lpSum([choices[p][v] for v in values]) <= 1
            # A constraint to ensure number of positions are not more than total number of widths of that value
        for v in values:
            prob += lpSum([choices[p][v] for p in position]) <= option_and_must_dict.get(v)
            # total width is positive
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position) >= 0
        # total width threshold as 200
        # prob += max_width - lpSum(choices[p][v] * v for v in values for p in position) <= 800
        prob.solve(PULP_CBC_CMD(timeLimit=5))
        if LpStatus[prob.status] == 'Optimal':
            for p in position:
                for v in values:
                    if value(choices[p][v]) == 1:
                        optimised_deckle.append(v)
                        option_and_must_dict[v] -= 1
                        if v in residual_dict and residual_dict.get(v) > 0:
                            residual_dict[v] -= 1
            for v in prob.variables():
                if v.varValue > 0:
                    print(v.name, "=", v.varValue)
            optimised_deckle.sort()
            final_list_deckle.append(optimised_deckle)
            final_list_deckle, option_and_must_dict, residual_dict = get_repetitive_deckle_optional(final_list_deckle,
                                                                                                    optimised_deckle,
                                                                                                    option_and_must_dict,
                                                                                                    residual_dict)
        status = prob.status
        if status != 1:
            min_repetitions -= 1
        if min_repetitions == 0:
            break
        if sum(residual_dict.values()) == 0:
            break
    return final_list_deckle, option_and_must_dict, residual_dict
