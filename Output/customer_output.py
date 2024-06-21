import pandas as pd
import numpy as np
from Constants.parameters import OrderDetails, CustomerTable, Optional

def customer_table(final_dict, df):
    customer_df = pd.DataFrame()
    customer_df[[CustomerTable.product_item, CustomerTable.sales_order, CustomerTable.customer_name, CustomerTable.consignee_name, CustomerTable.width, CustomerTable.product_ID, CustomerTable.target_rolls, Optional.column_name]] = df[
        [OrderDetails.item, OrderDetails.sales_order, OrderDetails.customer_name, OrderDetails.consignee_name, OrderDetails.width, OrderDetails.product_ID, OrderDetails.number_of_rolls, Optional.column_name]]
    customer_df[CustomerTable.actual_rolls] = None
    customer_df[CustomerTable.target_rolls] = np.ceil(customer_df[CustomerTable.target_rolls])
    customer_df[CustomerTable.target_quantity] = df[OrderDetails.product_qty].round(0).astype(int)
    for i in range(len(customer_df)):
        if customer_df[Optional.column_name].iloc[i] == Optional.must_make:
            if customer_df[CustomerTable.width].iloc[i] in final_dict.keys():
                customer_df[CustomerTable.actual_rolls].iloc[i] = min(final_dict.get(customer_df[CustomerTable.width].iloc[i]), customer_df[CustomerTable.target_rolls].iloc[i])
                final_dict[customer_df[CustomerTable.width].iloc[i]] -= customer_df[CustomerTable.actual_rolls].iloc[i]
            else:
                customer_df[CustomerTable.actual_rolls].iloc[i] = 0
        else:
            continue
    for i in range(len(customer_df)):
        if customer_df[Optional.column_name].iloc[i] == Optional.optional:
            if customer_df[CustomerTable.width].iloc[i] in final_dict.keys():
                customer_df[CustomerTable.actual_rolls].iloc[i] = min(
                    final_dict.get(customer_df[CustomerTable.width].iloc[i]),
                    customer_df[CustomerTable.target_rolls].iloc[i])
                final_dict[customer_df[CustomerTable.width].iloc[i]] -= customer_df[CustomerTable.actual_rolls].iloc[i]
            else:
                customer_df[CustomerTable.actual_rolls].iloc[i] = 0
        else:
            continue

    customer_df[CustomerTable.production_quantity] = customer_df[CustomerTable.actual_rolls] * customer_df[CustomerTable.width] * df[OrderDetails.product_thickness] * df[OrderDetails.product_length] * 0.91/ 1000000
    customer_df[CustomerTable.production_quantity] = customer_df[CustomerTable.production_quantity].astype(float).round(2)
    customer_df[CustomerTable.pending_quantity] = customer_df[CustomerTable.target_quantity] - customer_df[CustomerTable.production_quantity]
    return customer_df
