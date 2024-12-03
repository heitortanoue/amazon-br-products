# queries/query6.py
import pandas as pd
from utils.db_connection import get_database
import streamlit as st

@st.cache_data
def most_common_payment_types():
    """
    Determines the distribution of payment types used by customers across all orders,
    including the count and total payment value for each type.

    Returns:
        pd.DataFrame: DataFrame containing payment type statistics.
    """
    db = get_database()
    pipeline = [
        # Unwind the payment array to access individual payment records
        { "$unwind": "$payment" },

        # Group by payment type to calculate count and total payment value
        {
            "$group": {
                "_id": "$payment.payment_type",
                "count": { "$sum": 1 },
                "total_amount": { "$sum": "$payment.payment_value" }
            }
        },

        # Sort by count descending
        { "$sort": { "count": -1 } }
    ]
    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    df.rename(columns={'_id': 'payment_type'}, inplace=True)
    return df
