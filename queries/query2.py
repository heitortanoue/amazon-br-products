import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def average_order_value_by_state():
    """
    Calculates the average total value of orders for each customer state.

    Returns:
        pd.DataFrame: DataFrame containing customer states and their average order values.
    """
    db = get_database()
    pipeline = [
        { "$unwind": "$order_items" },
        {
            "$group": {
                "_id": "$_id",
                "customer_id": { "$first": "$customer_id" },
                "total_order_value": {
                    "$sum": {
                        "$add": ["$order_items.price", "$order_items.freight_value"]
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_info"
            }
        },
        { "$unwind": "$customer_info" },
        {
            "$group": {
                "_id": "$customer_info.customer_state",
                "average_order_value": { "$avg": "$total_order_value" }
            }
        },
        { "$sort": { "average_order_value": -1 } }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={'_id': 'customer_state'}, inplace=True)
    return df
