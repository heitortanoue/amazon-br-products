# queries/query9.py
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
        # Unwind the order items to access individual freight values
        { "$unwind": "$order_items" },

        # Lookup customer details from customers collection
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_info"
            }
        },

        # Unwind the customer_info array
        { "$unwind": "$customer_info" },

        # Group by customer state to calculate average freight value
        {
            "$group": {
                "_id": "$customer_info.customer_state",
                "average_freight_value": { "$avg": "$order_items.freight_value" },
                "total_orders": { "$sum": 1 }
            }
        },

        # Sort by average freight value descending
        { "$sort": { "average_freight_value": -1 } }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={'_id': 'customer_state'}, inplace=True)
    return df
