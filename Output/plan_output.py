import pandas as pd
import numpy as np

from Optimisation.deckle_optimisation import get_combined_optional_must_make, optimise_residual_deckle
from Output.customer_output import customer_table
import Constants.parameters as prms


def process_final_list(final_list_deckles):
    final_list_width = [sum(i) for i in final_list_deckles]
    final_list_trim = [prms.max_width - sum(i) for i in final_list_deckles]
    return final_list_width, final_list_trim


def create_deckles_tuples(final_list_deckles):
    return [tuple(lst) for lst in final_list_deckles]


def create_product_info(data):
    product_type = data['TYPE'].iloc[0]
    product_ID = data['ID'].iloc[0]
    product_OD = data['OD'].iloc[0]
    product_length = data['SAP LENGTH'].iloc[0]
    return product_type, product_ID, product_OD, product_length


def create_dataframe(final_list_deckles, final_list_trim, final_list_width, product_info):
    placeholder = -99999
    df = pd.DataFrame(final_list_deckles)
    df['Trim'] = final_list_trim
    df['Total width'] = final_list_width
    df['Type'] = product_info[0]
    df['Core ID'] = product_info[1]
    df['Roll OD'] = product_info[2]
    df['Length'] = product_info[3]
    df = df.fillna(placeholder)
    df = df.groupby(df.columns.tolist(), as_index=False).size()
    df = df.rename(columns={'size': 'Sets'})
    df = df.replace(placeholder, np.nan)
    return df


def calculate_knive_changes_and_trim(df, final_list_trim):
    num_of_knive_changes = len(df)
    total_trim = sum(final_list_trim)
    print('Knive changes:', num_of_knive_changes)
    print("Total trim:", total_trim)
    return num_of_knive_changes, total_trim


def calculate_completed_dict(must_make_number_dict, residual_dict):
    completed_dict = {key: must_make_number_dict[key] - residual_dict.get(key, 0) for key in must_make_number_dict}
    return completed_dict


def create_output(residual_dict, must_make_values, optional_values, optional_number_dict, position, possible_width,
                  final_list_deckles, data):
    option_and_must_dict, option_and_must_values = get_combined_optional_must_make(residual_dict, must_make_values,
                                                                                   optional_values,
                                                                                   optional_number_dict)
    final_list_deckles, option_and_must_dict, residual_dict = optimise_residual_deckle(option_and_must_values,
                                                                                       option_and_must_dict,
                                                                                       residual_dict, position,
                                                                                       possible_width, prms.min_arms,
                                                                                       final_list_deckles)

    final_list_width, final_list_trim = process_final_list(final_list_deckles)
    # final_list_deckles_tuples = create_deckles_tuples(final_list_deckles)
    product_info = create_product_info(data)

    df = create_dataframe(final_list_deckles, final_list_trim, final_list_width, product_info)
    calculate_knive_changes_and_trim(df, final_list_trim)

    df_width_roll = data[['WIDTH', 'NO.OF ROLL']].dropna()
    df_width_roll['NO.OF ROLL'] = np.ceil(df_width_roll['NO.OF ROLL'])
    grouped_df_width_roll = df_width_roll.groupby('WIDTH')['NO.OF ROLL'].sum().reset_index()
    must_make_values = grouped_df_width_roll['WIDTH'].tolist()
    must_make_number_repetitions = grouped_df_width_roll['NO.OF ROLL'].tolist()
    must_make_number_dict = dict(zip(must_make_values, must_make_number_repetitions))

    completed_dict = calculate_completed_dict(must_make_number_dict, residual_dict)
    print("check, check, check", completed_dict)

    return completed_dict, df


def common_optimisation_logic(data, get_deckle_function):
    optional_values = [450, 550, 625, 750, 950, 1080]
    optional_numbers = [15, 4, 12, 16, 3, 15]
    optional_number_dict = dict(zip(optional_values, optional_numbers))
    df_width_roll = data[['WIDTH', 'NO.OF ROLL']].dropna()
    df_width_roll['NO.OF ROLL'] = np.ceil(df_width_roll['NO.OF ROLL'])
    grouped_df_width_roll = df_width_roll.groupby('WIDTH')['NO.OF ROLL'].sum().reset_index()
    must_make_values = grouped_df_width_roll['WIDTH'].tolist()
    position = range(1, prms.max_arms + 1)
    possible_width = prms.max_width - prms.minimum_trim
    must_make_number_repetitions = grouped_df_width_roll['NO.OF ROLL'].tolist()
    must_make_number_dict = dict(zip(must_make_values, must_make_number_repetitions))
    residual_dict = must_make_number_dict.copy()

    final_list_deckles, residual_dict = get_deckle_function(must_make_values, residual_dict, position, possible_width,
                                                            prms.min_arms)

    completed_dict, plan_df = create_output(residual_dict, must_make_values, optional_values, optional_number_dict,
                                            position, possible_width, final_list_deckles, data)

    customer_df = customer_table(completed_dict, data)
    return plan_df, customer_df
