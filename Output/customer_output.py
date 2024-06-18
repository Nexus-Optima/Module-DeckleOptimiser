import pandas as pd
import numpy as np


def customer_table(final_dict, df):
    customer_df = pd.DataFrame()
    customer_df[['ITEM', 'SO', 'CUSTOMER', 'CONSIGN', 'WIDTH', 'ID', 'TARGET ROLL']] = df[
        ['ITEM NO', 'SO', 'CUSTOMER', 'CONSIGN', 'WIDTH', 'ID', 'NO.OF ROLL']]
    customer_df['ACTUAL ROLL'] = None
    customer_df['TARGET ROLL'] = np.ceil(customer_df['TARGET ROLL'])
    customer_df['QTY'] = df['QUANTITY'].round(0).astype(int)
    for i in range(len(customer_df)):
        if customer_df['WIDTH'].iloc[i] in final_dict.keys():
            if final_dict.get(customer_df['WIDTH'].iloc[i]) >= customer_df['TARGET ROLL'].iloc[i]:
                customer_df['ACTUAL ROLL'].iloc[i] = customer_df['TARGET ROLL'].iloc[i]
                final_dict[customer_df['WIDTH'].iloc[i]] = final_dict[customer_df['WIDTH'].iloc[i]] - \
                                                           customer_df['TARGET ROLL'].iloc[i]
            else:
                customer_df['ACTUAL ROLL'].iloc[i] = final_dict.get(customer_df['WIDTH'].iloc[i])
                final_dict[customer_df['WIDTH'].iloc[i]] = 0
        else:
            customer_df['ACTUAL ROLL'].iloc[i] = 0
    customer_df['PROD QTY'] = customer_df['ACTUAL ROLL'] * customer_df['WIDTH'] * df['MIC'] * df['SAP LENGTH'] * df[
        'DENSITY'] / 1000000
    customer_df['PROD QTY'] = customer_df['PROD QTY'].astype(float).round(2)
    customer_df['PENDING'] = customer_df['QTY'] - customer_df['PROD QTY']
    return customer_df
