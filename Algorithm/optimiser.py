from Database.s3_operations import save_results_to_file
from Output.plan_output import common_optimisation_logic


def get_optimised_knives(client_metadata, data):
    plan_df, customer_df, metric_df = common_optimisation_logic(data, alpha=0)
    save_results_to_file(client_metadata, plan_df, 'knives_optimisation', 'planning_output')
    save_results_to_file(client_metadata, customer_df, 'knives_optimisation', 'customer_output')
    save_results_to_file(client_metadata, metric_df, 'knives_optimisation', 'metrics_output')


def get_optimised_wastage(client_metadata, data):
    plan_df, customer_df, metric_df = common_optimisation_logic(data, alpha=1)
    save_results_to_file(client_metadata, plan_df, 'wastage_optimisation', 'planning_output')
    save_results_to_file(client_metadata, customer_df, 'wastage_optimisation', 'customer_output')
    save_results_to_file(client_metadata, metric_df, 'wastage_optimisation', 'metrics_output')


def get_optimised_hybrid(client_metadata, data):
    plan_df, customer_df, metric_df = common_optimisation_logic(data, alpha=0.5)
    save_results_to_file(client_metadata, plan_df, 'hybrid_optimisation', 'planning_output')
    save_results_to_file(client_metadata, customer_df, 'hybrid_optimisation', 'customer_output')
    save_results_to_file(client_metadata, metric_df, 'hybrid_optimisation', 'metrics_output')


def optimise_deckle(client_metadata, data):
    get_optimised_knives(client_metadata, data)
    get_optimised_wastage(client_metadata, data)
    get_optimised_hybrid(client_metadata, data)
