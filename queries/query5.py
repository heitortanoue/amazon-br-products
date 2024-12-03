# queries/query5.py
import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def top_rated_products():
    """
    Retrieves the top 10 products with the highest average review scores,
    considering only products with at least 100 reviews.

    Returns:
        pd.DataFrame: DataFrame containing product details and review statistics.
    """
    db = get_database()
    pipeline = [
        # Unwind the order items to access individual products
        { "$unwind": "$order_items" },

        # Match orders that have a review score
        { "$match": { "review.review_score": { "$ne": None } } },

        # Group by product_id to calculate average review score and count
        {
            "$group": {
                "_id": "$order_items.product_id",
                "average_review_score": { "$avg": "$review.review_score" },
                "review_count": { "$sum": 1 }
            }
        },

        # Filter products with at least 100 reviews
        { "$match": { "review_count": { "$gte": 100 } } },

        # Sort by average review score descending
        { "$sort": { "average_review_score": -1, "review_count": -1 } },

        # Limit to top 10
        { "$limit": 10 },

        # Lookup product details from products collection
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "product_info"
            }
        },

        # Unwind the product_info array
        { "$unwind": "$product_info" },

        # Project the desired fields
        {
            "$project": {
                "_id": 0,
                "product_id": "$_id",
                "average_review_score": 1,
                "review_count": 1,
                "product_category": "$product_info.product_category_name_english",
                "product_name_length": "$product_info.product_name_lenght"
            }
        }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    return df
