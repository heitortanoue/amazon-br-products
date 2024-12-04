import streamlit as st
import plotly.express as px
import json

def visualize_data(data, selected_query_title):
    if selected_query_title == "Monthly sales trends":
        fig_line = px.line(
            data,
            x="date",
            y="total_sales",
            labels={"date": "Month", "total_sales": "Total sales (BRL)"},
            title="Monthly sales trend",
            markers=True,
            line_shape="linear",
            color_discrete_sequence=["indigo"],
        )
        st.plotly_chart(fig_line, use_container_width=True)

        data["cumulative_sales"] = data["total_sales"].cumsum()
        fig_area = px.area(
            data,
            x="date",
            y="cumulative_sales",
            labels={"date": "Month", "cumulative_sales": "Cumulative sales (BRL)"},
            title="Cumulative monthly sales",
            color_discrete_sequence=["lightseagreen"],
        )
        st.plotly_chart(fig_area, use_container_width=True)

    elif selected_query_title == "Average order value by customer state":
        fig = px.bar(
            data,
            x="customer_state",
            y="average_order_value",
            labels={
                "average_order_value": "Average order value (BRL)",
                "customer_state": "Customer state",
            },
            title="Average order value by customer state",
            color="average_order_value",
            color_continuous_scale="Greens",
        )
        st.plotly_chart(fig, use_container_width=True)

        with open("./dataset/brazil-states.geojson") as f:
            geojson = json.load(f)

        fig_map = px.choropleth(
            data,
            geojson=geojson,
            locations="customer_state",
            featureidkey="properties.sigla",
            color="average_order_value",
            color_continuous_scale="Viridis",
            projection="mercator",
            title="Average order value by customer state",
        )
        fig_map.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig_map, use_container_width=True)

    elif selected_query_title == "Most popular products":
        st.markdown("Results limited to the top 10 products.")

        fig = px.bar(
            data,
            x="product_id",
            y="purchase_count",
            hover_data=["product_category", "product_name_length"],
            labels={"purchase_count": "Purchase count", "product_id": "Product ID"},
            title="Most popular products",
            color="purchase_count",
            color_continuous_scale="Purples",
        )
        st.plotly_chart(fig, use_container_width=True)

        fig_treemap = px.treemap(
            data,
            path=["product_category", "product_id"],
            values="purchase_count",
            color="purchase_count",
            color_continuous_scale="Purples",
            title="Treemap of most popular products by category",
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

    elif selected_query_title == "Average delivery time per seller":
        st.markdown("For better data quality, only sellers with 10 or more deliveries are considered.")

        fig = px.bar(
            data.head(10),
            x="seller_id",
            y="average_delivery_time_in_days",
            labels={
                "average_delivery_time_in_days": "Average delivery time (days)",
                "seller_id": "Seller ID",
            },
            title="Average delivery time per seller",
            color="average_delivery_time_in_days",
            color_continuous_scale="Oranges",
        )
        st.plotly_chart(fig, use_container_width=True)

        fig_scatter = px.histogram(
            data,
            x="average_delivery_time_in_days",
            nbins=100,
            labels={"average_delivery_time_in_days": "Average delivery time (days)"},
            title="Average delivery time histogram",
            color_discrete_sequence=["crimson"],
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    elif selected_query_title == "Top rated products":
        st.markdown("Results limited to the top 10 products with at least 100 reviews.")

        fig = px.bar(
            data,
            x="product_id",
            y="average_review_score",
            hover_data=["review_count", "product_category"],
            labels={
                "average_review_score": "Average review score",
                "product_id": "Product ID",
            },
            title="Top rated products",
            color="average_review_score",
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig, use_container_width=True)

        fig_bubble = px.scatter(
            data,
            x="average_review_score",
            y="review_count",
            size="review_count",
            color="average_review_score",
            hover_data=["product_id", "product_category"],
            labels={
                "average_review_score": "Average review score",
                "review_count": "Review count",
            },
            title="Review score vs. review count",
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    elif selected_query_title == "Most common payment types":

        fig_donut = px.pie(
            data,
            names="payment_type",
            values="count",
            title="Most common payment types",
            hover_data=["total_amount"],
            labels={"payment_type": "Payment type", "count": "Count"},
            hole=0.4,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        fig_bar = px.bar(
            data,
            x="payment_type",
            y="count",
            labels={"count": "Number of payments", "payment_type": "Payment type"},
            title="Number of payments by type",
            color="count",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    elif selected_query_title == "Sales by product category":
        fig_sales = px.bar(
            data.head(10),
            x="product_category",
            y="total_sales",
            labels={
                "total_sales": "Total sales (BRL)",
                "product_category": "Product category",
            },
            title="Total sales by product category",
            color="total_sales",
            color_continuous_scale="Greens",
        )
        st.plotly_chart(fig_sales, use_container_width=True)

        fig_orders = px.bar(
            data.head(10),
            x="product_category",
            y="total_orders",
            labels={
                "total_orders": "Number of orders",
                "product_category": "Product category",
            },
            title="Number of orders by product category",
            color="total_orders",
            color_continuous_scale="Greens",
        )
        st.plotly_chart(fig_orders, use_container_width=True)

    elif selected_query_title == "Cities with highest number of customers":
        st.markdown("Results limited to the top 10 cities.")

        fig_horizontal = px.bar(
            data,
            x="customer_count",
            y="customer_city",
            orientation="h",
            labels={
                "customer_count": "Number of customers",
                "customer_city": "Customer city",
            },
            title="Top 10 cities by number of customers",
            color="customer_count",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_horizontal, use_container_width=True)

    elif selected_query_title == "Average freight value by state":
        fig = px.bar(
            data,
            x="customer_state",
            y="average_freight_value",
            labels={
                "average_freight_value": "Average freight value (BRL)",
                "customer_state": "Customer state",
            },
            title="Average freight value by customer state",
            color="average_freight_value",
            color_continuous_scale="Oranges",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_query_title == "Orders with delayed delivery":

        fig = px.histogram(
            data,
            x="delay_in_days",
            nbins=100,
            labels={"delay_in_days": "Delay in Days"},
            title="Distribution of delivery delays",
            color_discrete_sequence=["crimson"],
        )
        st.plotly_chart(fig, use_container_width=True)
