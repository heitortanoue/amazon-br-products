import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def average_delivery_time_per_seller():
    """
    Computes the average delivery time from order approval to customer delivery for each seller.

    Returns:
        pd.DataFrame: DataFrame containing seller IDs and their average delivery times in days.
    """
    db = get_database()
    pipeline = [
        {
            "$match": {
                "order_approved_at": { "$ne": None },
                "order_delivered_customer_date": { "$ne": None }
            }
        },
        { "$unwind": "$order_items" },
        {
            "$project": {
                "seller_id": "$order_items.seller_id",
                "delivery_time_in_ms": {
                    "$subtract": ["$order_delivered_customer_date", "$order_approved_at"]
                }
            }
        },
        {
            "$group": {
                "_id": "$seller_id",
                "delivery_count": { "$sum": 1 },
                "average_delivery_time_in_ms": { "$avg": "$delivery_time_in_ms" }
            }
        },
        {
            "$match": { "delivery_count": { "$gte": 10 } }
        },
        {
            "$project": {
                "average_delivery_time_in_days": {
                    "$divide": ["$average_delivery_time_in_ms", 1000 * 60 * 60 * 24]
                },
                "delivery_count": 1
            }
        },
        {
            "$sort": { "average_delivery_time_in_days": 1 }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={"_id": "seller_id"}, inplace=True)
    return df
