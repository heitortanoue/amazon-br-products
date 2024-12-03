import streamlit as st
import plotly.express as px
import json

def visualize_data(data, selected_query_title):
    if selected_query_title == "Monthly sales trends":
        st.subheader("Monthly Sales Trends")

        # Line Chart
        st.markdown("### Line Chart: Total Sales Over Time")
        fig_line = px.line(
            data,
            x='date',
            y='total_sales',
            labels={'date': 'Month', 'total_sales': 'Total Sales (BRL)'},
            title="Monthly Sales Trend",
            markers=True,
            line_shape='linear',
            color_discrete_sequence=['indigo']
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Area Chart
        st.markdown("### Area Chart: Cumulative Sales Over Time")
        data_sorted = data.sort_values('date')
        data_sorted['cumulative_sales'] = data_sorted['total_sales'].cumsum()
        fig_area = px.area(
            data_sorted,
            x='date',
            y='cumulative_sales',
            labels={'date': 'Month', 'cumulative_sales': 'Cumulative Sales (BRL)'},
            title="Cumulative Monthly Sales",
            color_discrete_sequence=['lightseagreen']
        )
        st.plotly_chart(fig_area, use_container_width=True)

    elif selected_query_title == "Average order value by customer state":
        st.subheader("Average Order Value by Customer State")
        fig = px.bar(
            data,
            x='customer_state',
            y='average_order_value',
            labels={'average_order_value': 'Average Order Value (BRL)', 'customer_state': 'Customer State'},
            title="Average Order Value by Customer State",
            color='average_order_value',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

        with open('./dataset/brazil-states.geojson') as f:
            geojson = json.load(f)

        fig_map = px.choropleth(
            data,
            geojson=geojson,
            locations='customer_state',
            featureidkey="properties.sigla",
            color='average_order_value',
            color_continuous_scale='Viridis',
            projection="mercator",
            title="Average Order Value by Customer State",
        )
        fig_map.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig_map, use_container_width=True)

    elif selected_query_title == "Most popular products":
        st.subheader("Top 10 Most Popular Products")
        fig = px.bar(
            data,
            x='product_id',
            y='purchase_count',
            hover_data=['product_category', 'product_name_length'],
            labels={'purchase_count': 'Purchase Count', 'product_id': 'Product ID'},
            title="Most Popular Products",
            color='purchase_count',
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Treemap Visualization
        fig_treemap = px.treemap(
            data,
            path=['product_category', 'product_id'],
            values='purchase_count',
            color='purchase_count',
            color_continuous_scale='Purples',
            title="Treemap of Most Popular Products by Category"
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

    elif selected_query_title == "Average delivery time per seller":
        st.subheader("Top 10 Fast Average Delivery Time per Seller (Days)")
        fig = px.bar(
            data.head(10),
            x='seller_id',
            y='average_delivery_time_in_days',
            labels={'average_delivery_time_in_days': 'Average Delivery Time (Days)', 'seller_id': 'Seller ID'},
            title="Average Delivery Time per Seller",
            color='average_delivery_time_in_days',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)

        fig_scatter = px.histogram(
            data,
            x='average_delivery_time_in_days',
            nbins=100,
            labels={'average_delivery_time_in_days': 'Average Delivery Time (Days)'},
            title="Average Delivery Time Histogram",
            color_discrete_sequence=['crimson']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    elif selected_query_title == "Top rated products":
        st.subheader("Top 10 Products with Highest Average Review Scores")
        fig = px.bar(
            data,
            x='product_id',
            y='average_review_score',
            hover_data=['review_count', 'product_category'],
            labels={'average_review_score': 'Average Review Score', 'product_id': 'Product ID'},
            title="Top Rated Products",
            color='average_review_score',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Bubble Chart: Review Score vs. Review Count
        fig_bubble = px.scatter(
            data,
            x='average_review_score',
            y='review_count',
            size='review_count',
            color='average_review_score',
            hover_data=['product_id', 'product_category'],
            labels={'average_review_score': 'Average Review Score', 'review_count': 'Review Count'},
            title="Review Score vs. Review Count",
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    elif selected_query_title == "Most common payment types":
        st.subheader("Distribution of Payment Types")

        fig_donut = px.pie(
            data,
            names='payment_type',
            values='count',
            title="Most Common Payment Types",
            hover_data=['total_amount'],
            labels={'payment_type': 'Payment Type', 'count': 'Count'},
            hole=0.4
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        # Bar Chart for Payment Types
        fig_bar = px.bar(
            data,
            x='payment_type',
            y='count',
            labels={'count': 'Number of Payments', 'payment_type': 'Payment Type'},
            title="Number of Payments by Type",
            color='count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    elif selected_query_title == "Sales by product category":
        st.subheader("Top 10 Total Sales by Product Category")
        fig_sales = px.bar(
            data.head(10),
            x='product_category',
            y='total_sales',
            labels={'total_sales': 'Total Sales (BRL)', 'product_category': 'Product Category'},
            title="Total Sales by Product Category",
            color='total_sales',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_sales, use_container_width=True)

        st.subheader("Respective Number of Orders by Product Category")
        fig_orders = px.bar(
            data.head(10),
            x='product_category',
            y='total_orders',
            labels={'total_orders': 'Number of Orders', 'product_category': 'Product Category'},
            title="Number of Orders by Product Category",
            color='total_orders',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_orders, use_container_width=True)

    elif selected_query_title == "Cities with highest number of customers":
        st.subheader("Top 10 Cities with the Highest Number of Customers")

        # Horizontal Bar Chart
        fig_horizontal = px.bar(
            data,
            x='customer_count',
            y='customer_city',
            orientation='h',
            labels={'customer_count': 'Number of Customers', 'customer_city': 'Customer City'},
            title="Top 10 Cities by Number of Customers",
            color='customer_count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_horizontal, use_container_width=True)

    elif selected_query_title == "Average freight value by state":
        st.subheader("Average Freight Value by Customer State")
        fig = px.bar(
            data,
            x='customer_state',
            y='average_freight_value',
            labels={'average_freight_value': 'Average Freight Value (BRL)', 'customer_state': 'Customer State'},
            title="Average Freight Value by Customer State",
            color='average_freight_value',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_query_title == "Orders with delayed delivery":
        st.subheader("Orders with Delayed Delivery")

        st.write("### Distribution of Delivery Delays (Days)")
        fig = px.histogram(
            data,
            x='delay_in_days',
            nbins=100,
            labels={'delay_in_days': 'Delay in Days'},
            title="Distribution of Delivery Delays",
            color_discrete_sequence=['crimson']
        )
        st.plotly_chart(fig, use_container_width=True)
