# optimise the deckles to minimise total wastage
from pulp import *

from Optimisation.deckle_optimisation import get_repetitive_deckle


def get_optimised_wastage_deckle(values, number_dict, position, max_width, min_arms):
    # empty array to store the output
    final_list_deckle = []
    while True:
        optimised_deckle = []
        last_choices = {v: 0 for v in values}
        prob = LpProblem("Deckle_Problem", LpMinimize)
        # create a dictionary with choice[3][1100] representing whether position 3 has width 1100
        choices = LpVariable.dicts("Choice", (position, values), cat="Binary")
        # defining the optimisation problem
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position)
        # A constraint ensuring each width has only one value
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
        prob += max_width - lpSum(choices[p][v] * v for v in values for p in position) <= 650
        # time limit in completion of the optimisation exercise to give the best result within this time
        prob.solve(PULP_CBC_CMD(timeLimit=1))
        # add deckle in output if all conditions are met or else return false
        if LpStatus[prob.status] == 'Optimal':
            for p in position:
                for v in values:
                    if value(choices[p][v]) == 1:
                        last_choices[v] += 1
                        optimised_deckle.append(v)
                        number_dict[v] -= 1
            for v in prob.variables():
                if v.varValue > 0:
                    print(v.name, "=", v.varValue)
        print(last_choices)
        # for v in values:
        #   last_choiceslpSum(choices[p][v] for p in position)
        # list_of_optimised_deckle.append(optimised_deckle)
        # for v in distinct_optimised_deckle:
        #    print("Sum of choices[w][v] for w in widths is ")
        #    print(sum(choices[w][v].varValue for w in widths))
        #    print(len(optimised_deckle))
        # prob+=lpSum(choices[w][optimised_deckle[0]] for w in widths)<=2
        # prob.solve(PULP_CBC_CMD(timeLimit=1))
        # if LpStatus[prob.status] == 'Optimal':
        #    for w in widths:
        #        for v in values:
        #            if value(choices[w][v]) == 1:
        #                optimised_deckle_2.append(v)
        #                #number_dict[v] -= 1
        #                if v not in distinct_optimised_deckle:
        #                    distinct_optimised_deckle.append(v)
        #    for v in prob.variables():
        #        if v.varValue > 0:
        #            print("Solution 2")
        #            print(v.name, "=", v.varValue)
        status = prob.status
        if status != 1:
            break
        optimised_deckle.sort()
        final_list_deckle.append(optimised_deckle)
        final_list_deckle, number_dict = get_repetitive_deckle(final_list_deckle, optimised_deckle, number_dict)
        if sum(number_dict.values()) == 0:
            break
    return final_list_deckle, number_dict

