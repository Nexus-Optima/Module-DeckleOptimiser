from pulp import *
from collections import defaultdict
import pandas as pd
import numpy as np
from collections import Counter
import Constants.parameters as prms

# converts an array to a dictionary with the count being the value
def array_to_dict(arr):
    counts = defaultdict(int)
    for num in arr:
        counts[num] += 1
    return dict(counts)


# compares the values between two dictionaries
def compare_dict_values(dict1, dict2):
    for key in dict1:
        if key not in dict2 or dict1[key] > dict2[key]:
            return False
    return True


# optimise the deckles to minimise total wastage
def get_optimised_wastage_deckle(values, number_dict, position, max_width, min_arms):
    # empty array to store the output
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
    return optimised_deckle, number_dict, status


# optimise the deckles to minimise total number of knive changes
def get_optimised_knives_deckle(values, number_dict, position, max_width, min_arms):
    optimised_deckle = []
    prob = LpProblem("Deckle_Problem", LpMinimize)
    minimum_function = []
    choices = LpVariable.dicts("Choice", (position, values), cat="Binary")
    obj_value = LpVariable("obj_value", lowBound=0, cat="Continuous")
    prob += obj_value
    # A constraint to ensure obj value is the maximum of the number of times the value comes divided by the total number of values in dictionary for all values
    for v in values:
        if number_dict.get(v) > 0:
            prob += obj_value >= lpSum(choices[p][v] for p in position) / number_dict.get(v)
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
    # total width threshold as 200
    prob += max_width - lpSum(choices[p][v] * v for v in values for p in position) <= 200
    prob.solve(PULP_CBC_CMD(timeLimit=1))
    if LpStatus[prob.status] == 'Optimal':
        for p in position:
            for v in values:
                if value(choices[p][v]) == 1:
                    optimised_deckle.append(v)
                    number_dict[v] -= 1
        for v in prob.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)
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
    return optimised_deckle, number_dict, status


# to find out if repetition of deckle is possible
def get_repetitive_deckle(optimised_deckle, number_dict):
    optimised_dict = array_to_dict(optimised_deckle)
    result = compare_dict_values(optimised_dict, number_dict)
    if result:
        for key in optimised_dict:
            number_dict[key] = number_dict[key] - optimised_dict[key]
    return optimised_deckle, number_dict, result


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

def optimise_deckle(data, minimum_trim):
    product_type = data['TYPE'].iloc[0]
    product_ID = data['ID'].iloc[0]
    product_OD = data['OD'].iloc[0]
    product_length = data['SAP LENGTH'].iloc[0]
    df_width_roll = data[['WIDTH', 'NO.OF ROLL']].dropna()
    df_width_roll['NO.OF ROLL'] = np.ceil(df_width_roll['NO.OF ROLL'])
    grouped_df_width_roll = df_width_roll.groupby('WIDTH')['NO.OF ROLL'].sum().reset_index()
    must_make_values = grouped_df_width_roll['WIDTH'].tolist()
    must_make_number_repetitions = grouped_df_width_roll['NO.OF ROLL'].tolist()
    # optional_values = [450,550,625,750,950,1080]
    # optional_number = [15,4,12,16,3,15]
    # optional_number_dict = dict(zip(optional_values,optional_number))
    position = range(1, prms.max_arms + 1)
    must_make_number_dict = dict(zip(must_make_values, must_make_number_repetitions))
    residual_dict = must_make_number_dict.copy()
    possible_width = prms.max_width - prms.minimum_trim
    flag = 1
    final_list_deckles = []
    if minimum_trim == 0:
        while flag == 1:
            op_deckle, residual_dict, flag = get_optimised_knives_deckle(must_make_values, residual_dict, position, possible_width,
                                                                          prms.min_arms)
            op_deckle = sorted(op_deckle)
            if flag == 1:
                final_list_deckles.append(op_deckle)
                repeat_flag = 1
                while repeat_flag == 1:
                    op_deckle, residual_dict, repeat_flag = get_repetitive_deckle(op_deckle, residual_dict)
                    if repeat_flag == 1:
                        final_list_deckles.append(op_deckle)
    else:
        while flag == 1:
            op_deckle, residual_dict, flag = get_optimised_wastage_deckle(must_make_values, residual_dict, position,
                                                                         possible_width,
                                                                         prms.min_arms)
            op_deckle = sorted(op_deckle)
            if flag == 1:
                final_list_deckles.append(op_deckle)
                repeat_flag = 1
                while repeat_flag == 1:
                    op_deckle, residual_dict, repeat_flag = get_repetitive_deckle(op_deckle, residual_dict)
                    if repeat_flag == 1:
                        final_list_deckles.append(op_deckle)
    # print(residual_dict)
    # for i in final_list_deckles:
    #     print(sum(i))
    final_list_width = []
    final_list_trim = []
    for i in final_list_deckles:
        final_list_width.append(sum(i))
        final_list_trim.append(prms.max_width - sum(i))
    final_list_deckles_tuples = [tuple(lst) for lst in final_list_deckles]
    count_dict = dict(Counter(final_list_deckles_tuples))
    df = pd.DataFrame(final_list_deckles)
    df['Trim'] = final_list_trim
    df['Total width'] = final_list_width
    df['Type'] = product_type
    df['Core ID']=product_ID
    df['Roll OD'] = product_OD
    df['Length'] = product_length
    placeholder = -99999
    df = df.fillna(placeholder)
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    df = df.rename(columns = {'size': 'Sets'})
    df = df.replace(placeholder, np.nan)
    num_of_knive_changes = len(df)
    total_trim = sum(final_list_trim)
    print('Knive changes: ', num_of_knive_changes)
    print("Total trim: ", total_trim)
    completed_dict={}
    for key in must_make_number_dict:
        if key in residual_dict:
            completed_dict[key]=must_make_number_dict[key]-residual_dict[key]
    return completed_dict, df
   # excel_file_path = 'output.xlsx'
   # df.to_excel(excel_file_path, index=False)

# In[5]:

# option_and_must_dict, option_and_must_values = get_combined_optional_must_make(residual_dict,must_make_values,optional_values, optional_number_dict)
# flag = 1
# while flag == 1:
#     op_deckle, option_and_must_dict, flag = get_optimised_wastage_deckle(option_and_must_values,option_and_must_dict,widths,max_width, min_arms)
#     print(op_deckle)
#     for i in op_deckle:
#         if i in must_make_values and residual_dict[i]!=0:
#             residual_dict[i]-=1
#         print(residual_dict)
#     print(sum(residual_dict.values()))
#     final_list_deckles.append(op_deckle)
#     if sum(residual_dict.values()) == 0:
#         break
#
# unique_list_deckle = []
# for i in final_list_deckles:
#     i.sort()
#     if i in unique_list_deckle:
#         continue
#     else:
#         unique_list_deckle.append(i)
# for i in final_list_deckles:
#     print(sum(i))
#
#
# # In[40]:
#
#
# print(option_and_must_dict)


# In[ ]:




