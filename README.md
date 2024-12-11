# Olist E-commerce Data Analysis Dashboard

![Olist Dashboard Banner](https://d3hw41hpah8tvx.cloudfront.net/images/post_blog_produtos_olist_g_legacy_2018_11_afb6860a22.png)

## Overview

The **Olist E-commerce Data Analysis Dashboard** is a Streamlit application designed to analyze and visualize various aspects of the Olist e-commerce dataset. This dataset contains information about 100k orders made between 2016 and 2018 across multiple marketplaces in Brazil. The dashboard provides insights into product performance, payment methods, delivery efficiency, sales trends, and more, enabling data-driven decision-making for e-commerce businesses.

## Data source

The data was taken from [this source](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and modelled accordingly to a MongoDB database. The data was then queried using PyMongo and visualized using Streamlit.

To leverage MongoDB's strengths in handling non-relational data, the dataset has been transformed into a **document-oriented model**. This involves organizing the data into collections and documents, employing embedded documents for closely related information like order items and payments within the orders collection, and using references where appropriate to maintain data integrity. This modeling approach enhances query efficiency, scalability, and flexibility.

## Queries
- Monthly sales trends;
- Average order value by customer state;
- Most popular products;
- Average delivery time per seller;
- Top rated products;
- Most common payment types;
- Sales by product category;
- Cities with highest number of customers;
- Average freight value by state;
- Orders with delayed delivery;