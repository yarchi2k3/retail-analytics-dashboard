import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Retail Analytics Dashboard")
st.markdown(
    """
    Interactive dashboard for exploring supermarket sales performance
    across branches, customer segments, and product categories.
    """
)

df = pd.read_csv("data/raw/supermarket_sales.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Weekday"] = df["Date"].dt.day_name()
df["Time"] = pd.to_datetime(
    df["Time"],
    format="%H:%M"
)
df["Hour"] = df["Time"].dt.hour

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday", 
]

df["Weekday"] = pd.Categorical(
    df["Weekday"],
    categories=weekday_order,
    ordered=True,
)

st.sidebar.header("Filters")

selected_branch = st.sidebar.selectbox(
    "Select Branch",
    ["All"] + sorted(df["Branch"].unique())
)


selected_customer_type = st.sidebar.selectbox(
    "Customer Type",
    ["All"] + sorted(df["Customer type"].unique())
)

st.sidebar.markdown("---")

filtered_df = df.copy()

if selected_branch != "All":
    filtered_df = filtered_df[
        filtered_df["Branch"] == selected_branch
    ]

if selected_customer_type != "All":
    filtered_df = filtered_df[
        filtered_df["Customer type"] == selected_customer_type
    ] 

total_revenue = filtered_df["Total"].sum()
total_transactions = filtered_df["Invoice ID"].count()
avg_basket = filtered_df["Total"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col2:
    st.metric("Transactions", f"{total_transactions:,}")

with col3:
    st.metric("Avg Basket Value", f"${avg_basket:,.2f}")  

col1, col2 = st.columns([3, 2])

weekday_revenue = filtered_df.groupby("Weekday")["Total"].sum()    

with col1:
    st.subheader("Revenue Trends by Weekday")
    st.bar_chart(weekday_revenue)

hourly_transactions = filtered_df.groupby("Hour")["Invoice ID"].count()

with col2:
    st.subheader("Customer Traffic by Hour")
    st.line_chart(hourly_transactions)

product_revenue = filtered_df.groupby("Product line")["Total"].sum().sort_values(ascending=True)

st.subheader("Revenue by Product Line")
fig = px.bar(
    product_revenue,
    x=product_revenue.values,
    y=product_revenue.index,
    orientation="h",
    labels={
        "x": "Revenue",
        "y": "Product Line"
    },
    template="plotly_dark"
)

fig.update_traces(marker_color="#83c9ff")

st.plotly_chart(
    fig,
    width="stretch"
)

# st.write("Dataset Preview")
# st.dataframe(df.head())

st.markdown("---")
st.caption(
    "Built with Python, Pandas, Streamlit and Matplotlib"
)