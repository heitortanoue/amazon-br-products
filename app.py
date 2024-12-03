import streamlit as st
import pandas as pd
from utils import visualizations
from queries import query1, query2, query3, query4, query5, query6, query7, query8, query9, query10

st.set_page_config(page_title="Olist E-commerce Data Analysis", layout="wide")

st.title("Olist E-commerce data analysis")

query_options = {
    "Monthly sales trends": query1.monthly_sales_trends,
    "Average order value by customer state": query2.average_order_value_by_state,
    "Most popular products": query3.most_popular_products,
    "Average delivery time per seller": query4.average_delivery_time_per_seller,
    "Top rated products": query5.top_rated_products,
    "Most common payment types": query6.most_common_payment_types,
    "Sales by product category": query7.sales_by_product_category,
    "Cities with highest number of customers": query8.top_cities_by_customers,
    "Average freight value by state": query9.average_freight_value_by_state,
    "Orders with delayed delivery": query10.orders_with_delayed_delivery
}

st.sidebar.title("Queries")
selected_query_title = st.sidebar.selectbox("Select a query to display:", list(query_options.keys()))
selected_query_function = query_options[selected_query_title]

st.sidebar.markdown("---")

st.sidebar.title("About 🇧🇷")
st.sidebar.markdown("This is a Brazilian ecommerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. We also released a geolocation dataset that relates Brazilian zip codes to lat/lng coordinates.")

st.sidebar.markdown("> Made by [Heitor Tanoue](https://github.com/heitortanoue)")

st.header(selected_query_title)

def load_data():
    return selected_query_function()

data = load_data()

# Display the data
st.dataframe(data)

visualizations.visualize_data(data, selected_query_title)
