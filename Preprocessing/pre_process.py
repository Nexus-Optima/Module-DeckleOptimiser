from Constants.parameters import OrderDetails

def split_dataframe(df):
    grouped = df.groupby([OrderDetails.product_type, OrderDetails.product_ID, OrderDetails.product_OD, OrderDetails.product_length])

    # Create a dictionary to hold the split DataFrames
    dfs = {name: group.reset_index(drop=True) for name, group in grouped}
    return dfs
