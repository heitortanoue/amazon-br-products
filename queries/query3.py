import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def most_popular_products():
    """
    Identifies the most frequently purchased products.

    Returns:
        pd.DataFrame: DataFrame containing product details and purchase counts.
    """
    db = get_database()
    pipeline = [
        { "$unwind": "$order_items" },
        {
            "$group": {
                "_id": "$order_items.product_id",
                "purchase_count": { "$sum": 1 }
            }
        },
        { "$sort": { "purchase_count": -1 } },
        { "$limit": 10 },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "product_info"
            }
        },
        { "$unwind": "$product_info" },
        {
            "$project": {
                "_id": 0,
                "product_id": "$_id",
                "purchase_count": 1,
                "product_category": "$product_info.product_category_name_english",
                "product_name_length": "$product_info.product_name_lenght"
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    return df
