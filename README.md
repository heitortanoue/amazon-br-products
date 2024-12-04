# Olist E-commerce Data Analysis Dashboard

![Olist Dashboard Banner](https://d3hw41hpah8tvx.cloudfront.net/images/post_blog_produtos_olist_g_legacy_2018_11_afb6860a22.png)

## Overview

The **Olist E-commerce Data Analysis Dashboard** is a Streamlit application designed to analyze and visualize various aspects of the Olist e-commerce dataset. This dataset encompasses information about 100k orders made between 2016 and 2018 across multiple marketplaces in Brazil. The dashboard provides insights into product performance, payment methods, delivery efficiency, sales trends, and more, enabling data-driven decision-making for e-commerce businesses.

## Data source

The data was taken from [this source](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and modelled accordingly to a MongoDB database. The data was then queried using PyMongo and visualized using Streamlit.

To leverage MongoDB's strengths in handling non-relational data, the dataset has been transformed into a **document-oriented model**. This involves organizing the data into collections and documents, employing embedded documents for closely related information like order items and payments within the orders collection, and using references where appropriate to maintain data integrity. This modeling approach enhances query efficiency, scalability, and flexibility.



## Features

- **Top Products Analysis:**
  - **Sales Volume:** Identify the top 10 products by units sold.
  - **Revenue:** Determine the top 10 products generating the highest revenue.
  - **Sales Distribution:** Analyze sales distribution across different product categories.

- **Payment Methods Insights:**
  - **Most Common Payments:** Discover the most frequently used payment types.

- **Delivery Performance:**
  - **Average Delivery Time:** Evaluate delivery efficiency by state.
  - **Freight Value Analysis:** Assess average freight costs across states.

- **Order Status Overview:**
  - **Status Distribution:** Understand the distribution of various order statuses.

- **Sales Trends:**
  - **Monthly Sales Trends:** Visualize sales performance over time.

- **Geographical Insights:**
  - **Order Distribution:** Map the geographical distribution of orders.

- **Product Returns Analysis:**
  - **Return Rates:** Identify products with the highest return rates.
