# queries/query10.py
import pandas as pd
from utils.db_connection import get_database

def orders_with_delayed_delivery():
    """
    Finds all orders where the actual delivery date was later than the estimated delivery date,
    indicating a delayed delivery.

    Returns:
        pd.DataFrame: DataFrame containing details of delayed orders.
    """
    db = get_database()
    pipeline = [
        # Match orders where delivery dates exist
        {
            "$match": {
                "order_delivered_customer_date": { "$ne": None },
                "order_estimated_delivery_date": { "$ne": None }
            }
        },

        # Add a field to calculate if delivery was delayed
        {
            "$addFields": {
                "is_delayed": {
                    "$gt": ["$order_delivered_customer_date", "$order_estimated_delivery_date"]
                },
                "delay_in_ms": {
                    "$subtract": ["$order_delivered_customer_date", "$order_estimated_delivery_date"]
                }
            }
        },

        # Filter only delayed deliveries
        {
            "$match": {
                "is_delayed": True
            }
        },

        # Lookup to join with customers collection to get customer_state
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_info"
            }
        },

        # Unwind the customer_info array
        {
            "$unwind": "$customer_info"
        },

        # Project desired fields including customer_state
        {
            "$project": {
                "_id": 0,
                "order_id": "$_id",
                "customer_id": 1,
                "order_purchase_timestamp": 1,
                "order_delivered_customer_date": 1,
                "order_estimated_delivery_date": 1,
                "delay_in_days": {
                    "$divide": ["$delay_in_ms", 1000 * 60 * 60 * 24]
                }
            }
        },

        # Sort by delay_in_days descending
        {
            "$sort": { "delay_in_days": -1 }
        }
    ]

    result = list(db.orders.aggregate(pipeline))
    df = pd.DataFrame(result)
    return df