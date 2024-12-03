# queries/query8.py
import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def monthly_sales_trends():
    """
    Visualizes sales trends on a monthly basis.

    Returns:
        pd.DataFrame: DataFrame containing months and their corresponding total sales.
    """
    db = get_database()
    pipeline = [
        { "$unwind": "$order_items" },
        {
            "$addFields": {
                "order_month": { "$month": "$order_purchase_timestamp" },
                "order_year": { "$year": "$order_purchase_timestamp" }
            }
        },
        {
            "$group": {
                "_id": { "year": "$order_year", "month": "$order_month" },
                "total_sales": { "$sum": "$order_items.price" }
            }
        },
        { "$sort": { "_id.year": 1, "_id.month": 1 } },
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "total_sales": { "$round": ["$total_sales", 2] }
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    # Create a datetime column for plotting
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))
    return df
