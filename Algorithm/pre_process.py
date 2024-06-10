from pulp import *
from collections import defaultdict
import pandas as pd
import numpy as np
from collections import Counter
import Constants.parameters as prms

def split_dataframe(df):
    grouped = df.groupby(['TYPE','ID','OD','SAP LENGTH'])

    # Create a dictionary to hold the split DataFrames
    dfs = {name: group.reset_index(drop=True) for name, group in grouped}

    for name, df_group in dfs.items():
        print(f"DataFrame for Category combination {name}:")
        print(df_group)
    return dfs