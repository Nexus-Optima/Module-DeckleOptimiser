class Parameters:
    min_arms = 4
    max_arms = 16
    max_width = 8700
    minimum_trim = 250

class Optional:
    column_name = 'Option'
    must_make = 'MustMake'
    optional = 'Optional'

class OrderDetails:
    width = 'Width'
    number_of_rolls = 'Rolls'
    product_type = 'Material'
    product_ID = 'ID'
    product_OD = 'OD'
    product_length = 'Lenght'
    item = 'Item No.'
    sales_order = 'Sales Orde'
    customer_name = 'Buyer Name'
    consignee_name = 'Consignee Name'
    product_qty = 'Pend. Prod'
    so_qty = 'SO.Qty'
    current_stock = 'Stock'
    product_thickness = 'Micron'
    product_density = 'DENSITY'

class CustomerTable:
    product_item = 'ITEM'
    sales_order = 'SO'
    customer_name = 'CUSTOMER'
    consignee_name = 'CONSIGN'
    width = 'WIDTH'
    product_ID = 'ID'
    target_rolls = 'TARGET ROLL'
    actual_rolls = 'ACTUAL ROLL'
    target_quantity = 'QTY'
    production_quantity = 'PROD QTY'
    pending_quantity = 'PENDING'

class Storage:
    s3_bucket = "b3llcurve-trim-optimisation"
