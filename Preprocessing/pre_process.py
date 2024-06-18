def split_dataframe(df):
    grouped = df.groupby(['TYPE', 'ID', 'OD', 'SAP LENGTH'])

    # Create a dictionary to hold the split DataFrames
    dfs = {name: group.reset_index(drop=True) for name, group in grouped}
    return dfs
