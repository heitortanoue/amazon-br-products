import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def sales_by_product_category():
    """
    Calculates the total sales amount and the number of orders for each product category.

    Returns:
        pd.DataFrame: DataFrame containing sales statistics by product category.
    """
    db = get_database()
    pipeline = [
        {"$unwind": "$order_items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "order_items.product_id",
                "foreignField": "_id",
                "as": "product_info",
            }
        },
        {"$unwind": "$product_info"},
        {
            "$group": {
                "_id": "$product_info.product_category_name_english",
                "total_sales": {"$sum": "$order_items.price"},
                "total_orders": {"$sum": 1},
            }
        },
        {"$sort": {"total_sales": -1}},
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={"_id": "product_category"}, inplace=True)
    return df
