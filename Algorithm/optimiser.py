from Output.plan_output import common_optimisation_logic
from Algorithm.knives_optimiser import get_optimised_knives_deckle
from Algorithm.wastage_optimiser import get_optimised_wastage_deckle


def get_optimised_knives(data):
    plan_df, customer_df = common_optimisation_logic(data, get_optimised_knives_deckle)


def get_optimised_wastage(data):
    plan_df, customer_df = common_optimisation_logic(data, get_optimised_wastage_deckle)


def optimise_deckle(data):
    get_optimised_knives(data)
    get_optimised_wastage(data)
