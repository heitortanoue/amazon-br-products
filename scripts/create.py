import pandas as pd
import pymongo
import json
import pickle
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

mongo_connection_string = os.getenv('MONGODB_CONNECTION_STRING')

# Connect to MongoDB
client = pymongo.MongoClient(mongo_connection_string, timeoutMS=10*60*1000)
db = client['olistDB']
print("Connected to MongoDB.")

# Load CSV data into DataFrames
customers_df = pd.read_csv('./dataset/olist_customers_dataset.csv')
geolocations_df = pd.read_csv('./dataset/olist_geolocation_dataset.csv')
order_items_df = pd.read_csv('./dataset/olist_order_items_dataset.csv')
order_payments_df = pd.read_csv('./dataset/olist_order_payments_dataset.csv')
order_reviews_df = pd.read_csv('./dataset/olist_order_reviews_dataset.csv')
orders_df = pd.read_csv('./dataset/olist_orders_dataset.csv')
products_df = pd.read_csv('./dataset/olist_products_dataset.csv')
sellers_df = pd.read_csv('./dataset/olist_sellers_dataset.csv')
product_category_translation_df = pd.read_csv('./dataset/product_category_name_translation.csv')
print("Data loaded into DataFrames.")

# ------------------ Customers Collection ------------------

# Rename 'customer_id' to '_id' for MongoDB
customers_df.rename(columns={'customer_id': '_id'}, inplace=True)

# Convert DataFrame to dictionary format
customers_data = customers_df.to_dict(orient='records')

# Insert data into MongoDB
db.customers.insert_many(customers_data)

print("Customers collection inserted.")

# ------------------ Geolocations Collection ------------------

# Convert DataFrame to dictionary format
geolocations_data = geolocations_df.to_dict(orient='records')

# Insert data into MongoDB
db.geolocations.insert_many(geolocations_data)

print("Geolocations collection inserted.")

# ------------------ Sellers Collection ------------------

# Rename 'seller_id' to '_id' for MongoDB
sellers_df.rename(columns={'seller_id': '_id'}, inplace=True)

# Convert DataFrame to dictionary format
sellers_data = sellers_df.to_dict(orient='records')

# Insert data into MongoDB
db.sellers.insert_many(sellers_data)

print("Sellers collection inserted.")

# ------------------ Products Collection ------------------

# Merge product category translations
products_df = pd.merge(products_df, product_category_translation_df, on='product_category_name', how='left')

# Replace NaN in 'product_category_name_english' with 'Unknown'
products_df['product_category_name_english'].fillna('Unknown', inplace=True)

# Rename 'product_id' to '_id' for MongoDB
products_df.rename(columns={'product_id': '_id'}, inplace=True)

# Convert DataFrame to dictionary format
products_data = products_df.to_dict(orient='records')

# Insert data into MongoDB
db.products.insert_many(products_data)

print("Products collection inserted.")

# ------------------ Orders Collection ------------------

# Convert date columns to datetime
date_columns = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

for col in date_columns:
    orders_df[col] = pd.to_datetime(orders_df[col], errors='coerce')

# Prepare order items data
order_items_df['shipping_limit_date'] = pd.to_datetime(order_items_df['shipping_limit_date'], errors='coerce')
order_items_df.dropna(subset=['order_id'], inplace=True)
order_items_grouped = order_items_df.groupby('order_id').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Prepare order payments data
order_payments_df.dropna(subset=['order_id'], inplace=True)
order_payments_grouped = order_payments_df.groupby('order_id').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Prepare order reviews data
review_date_columns = ['review_creation_date', 'review_answer_timestamp']
for col in review_date_columns:
    order_reviews_df[col] = pd.to_datetime(order_reviews_df[col], errors='coerce')

order_reviews_df.dropna(subset=['order_id'], inplace=True)
order_reviews_grouped = order_reviews_df.groupby('order_id').apply(lambda x: x.to_dict(orient='records')).to_dict()

# ------------------ Caching Mechanism ------------------

# Load processed order IDs from cache if exists
cache_file = 'processed_orders.pkl'
if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        processed_order_ids = pickle.load(f)
else:
    processed_order_ids = set()

# ------------------ Process and Insert Orders ------------------

batch_size = 1000
orders_data_batch = []
batch_count = 0

try:
    total_orders = len(orders_df)
    for index, order in orders_df.iterrows():
        order_dict = order.to_dict()
        order_id = order_dict['order_id']

        # Skip if order has been processed already
        if order_id in processed_order_ids:
            continue

        # Remove any NaN values
        order_dict = {k: v if pd.notnull(v) else None for k, v in order_dict.items()}

        # Convert date columns to Python datetime objects
        for col in date_columns:
            if order_dict[col]:
                order_dict[col] = order_dict[col].to_pydatetime()
            else:
                order_dict[col] = None

        # Get order items and embed them
        order_items = order_items_grouped.get(order_id, [])
        for item in order_items:
            item.pop('order_id', None)
        order_dict['order_items'] = order_items

        # Get payment information and embed it
        order_payments = order_payments_grouped.get(order_id, [])
        for payment in order_payments:
            payment.pop('order_id', None)
        order_dict['payment'] = order_payments

        # Get review information and embed it
        order_reviews = order_reviews_grouped.get(order_id, [])
        for review in order_reviews:
            review.pop('order_id', None)
        order_dict['review'] = order_reviews[0] if order_reviews else {}

        # Set '_id' field and remove 'order_id'
        order_dict['_id'] = order_dict['order_id']
        order_dict.pop('order_id', None)

        orders_data_batch.append(order_dict)
        processed_order_ids.add(order_id)

        # Insert batch when it reaches the batch_size
        if len(orders_data_batch) >= batch_size:
            db.orders.insert_many(orders_data_batch)
            orders_data_batch = []
            batch_count += 1
            print(f"Inserted batch {batch_count * batch_size} orders.")

            # Save progress to cache file
            with open(cache_file, 'wb') as f:
                pickle.dump(processed_order_ids, f)

    # Insert any remaining orders in the last batch
    if orders_data_batch:
        db.orders.insert_many(orders_data_batch)
        print(f"Inserted final batch of {len(orders_data_batch)} orders.")

    # Save progress to cache file
    with open(cache_file, 'wb') as f:
        pickle.dump(processed_order_ids, f)

    print("Orders collection inserted.")

except Exception as e:
    print(f"An error occurred: {e}")
    # Save progress to cache file before exiting
    with open(cache_file, 'wb') as f:
        pickle.dump(processed_order_ids, f)
    print("Progress saved to cache file.")
    raise  # Re-raise exception to see the traceback

# ------------------ Script Complete ------------------
print("Data import to MongoDB completed successfully.")
