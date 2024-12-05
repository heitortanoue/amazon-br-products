import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def top_cities_by_customers():
    """
    Identifies the top 10 cities with the highest number of registered customers.

    Returns:
        pd.DataFrame: DataFrame containing cities and their customer counts.
    """
    db = get_database()
    pipeline = [
        {
            "$group": {
                "_id": "$customer_unique_id",
                "customer_city": { "$first": "$customer_city" }
            }
        },
        {
            "$group": {
                "_id": "$customer_city",
                "customer_count": { "$sum": 1 }
            }
        },
        { "$sort": { "customer_count": -1 } },
        { "$limit": 10 }
    ]
    result = list(db.customers.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={'_id': 'customer_city'}, inplace=True)
    return df
