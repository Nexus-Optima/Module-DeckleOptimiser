from Database.s3_operations import save_results_to_file
from Output.plan_output import common_optimisation_logic
from Algorithm.knives_optimiser import get_optimised_knives_deckle
from Algorithm.wastage_optimiser import get_optimised_wastage_deckle


def get_optimised_knives(data):
    plan_df, customer_df = common_optimisation_logic(data, get_optimised_knives_deckle)
    save_results_to_file(plan_df, 'knives_optimisation', 'planning_output')
    save_results_to_file(customer_df, 'knives_optimisation', 'customer_output')


def get_optimised_wastage(data):
    plan_df, customer_df = common_optimisation_logic(data, get_optimised_wastage_deckle)
    save_results_to_file(plan_df, 'wastage_optimisation', 'planning_output')
    save_results_to_file(customer_df, 'wastage_optimisation', 'customer_output')


def optimise_deckle(data):
    get_optimised_knives(data)
    get_optimised_wastage(data)
