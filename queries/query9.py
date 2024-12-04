import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def average_freight_value_by_state():
    """
    Computes the average freight (shipping) value charged to customers in each state.

    Returns:
        pd.DataFrame: DataFrame containing states and their average freight values.
    """
    db = get_database()
    pipeline = [
        { "$unwind": "$order_items" },
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
                "average_freight_value": { "$avg": "$order_items.freight_value" },
                "total_orders": { "$sum": 1 }
            }
        },
        { "$sort": { "average_freight_value": -1 } }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={'_id': 'customer_state'}, inplace=True)
    return df
