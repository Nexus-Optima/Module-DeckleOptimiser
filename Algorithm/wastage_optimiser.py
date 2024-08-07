# optimise the deckles to minimise total wastage
from pulp import *

from Optimisation.deckle_optimisation import get_repetitive_deckle


def get_optimised_wastage_deckle(values, number_dict, position, max_width, min_arms):
    # empty array to store the output
    final_list_deckle = []
    while True:
        total_width = sum(key*value for key,value in number_dict.items())
        total_sets = (total_width // max_width) + 1
        min_repetitions = min(4, (total_sets//5)+2)
        optimised_deckle = []
        prob = LpProblem("Deckle_Problem", LpMinimize)
        # create a dictionary with choice[3][1100] representing whether position 3 has width 1100
        choices = LpVariable.dicts("Choice", (position, values), cat="Binary")
        # defining the optimisation problem
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position)
        # A constraint ensuring each width has only one value
        for v in values:
            if number_dict.get(v) > 0:
                prob += lpSum(choices[p][v] for p in position) / number_dict.get(v) <= 1/min_repetitions
        for p in position:
            if p <= min_arms:
                prob += lpSum([choices[p][v] for v in values]) == 1
            else:
                prob += lpSum([choices[p][v] for v in values]) <= 1
        # A constraint to ensure number of positions are not more than total number of widths of that value
        for v in values:
            prob += lpSum([choices[p][v] for p in position]) <= number_dict.get(v)
        # total width is positive
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position) >= 0
        # total width threshold as 650
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position) <= 450
        # time limit in completion of the optimisation exercise to give the best result within this time
        prob.solve(PULP_CBC_CMD(timeLimit=5))
        # add deckle in output if all conditions are met or else return false
        if LpStatus[prob.status] == 'Optimal':
            for p in position:
                for v in values:
                    if value(choices[p][v]) == 1:
                        optimised_deckle.append(v)
                        number_dict[v] -= 1
            for v in prob.variables():
                if v.varValue > 0:
                    print(v.name, "=", v.varValue)
        status = prob.status
        if status != 1:
            break
        optimised_deckle.sort()
        final_list_deckle.append(optimised_deckle)
        final_list_deckle, number_dict = get_repetitive_deckle(final_list_deckle, optimised_deckle, number_dict)
        if sum(number_dict.values()) == 0:
            break
    return final_list_deckle, number_dict

