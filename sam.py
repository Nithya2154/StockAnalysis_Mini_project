import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Stock Analytics Dashboard", layout="wide")

st.title("📊 Stock Market Analytics Dashboard")
st.markdown("---")

# =========================
# Row 1: Volatility + Sector Return
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Most Volatile Stocks")

    q1 = pd.read_csv(
        r"C:\Nithyanantham\Mini_Projects\results\question1.csv"
    )

    q1 = q1.set_index("Ticker")

    st.bar_chart(q1["Cumulative_Return"])


with col2:
    st.subheader("Average Yearly Return by Sector")

    q3 = pd.read_csv(
        r"C:\Nithyanantham\Mini_Projects\results\question3.csv"
    )

    sector_avg = (
        q3.groupby("sector", as_index=False)["Daily_Return"]
        .mean()
        .sort_values("Daily_Return", ascending=False)
    )

    st.bar_chart(sector_avg, x="sector", y="Daily_Return")

st.markdown("---")

# =========================
# Row 2: Cumulative Returns Line Chart
# =========================
st.subheader("Cumulative Return for Top 5 Performing Stocks")

q2 = pd.read_csv(
    r"C:\Nithyanantham\Mini_Projects\results\question2.csv"
)

q2["date"] = pd.to_datetime(q2["date"])

pivot_df = q2.pivot(
    index="date",
    columns="Ticker",
    values="cumulative_return"
)

st.line_chart(pivot_df)

st.markdown("---")

# =========================
# Row 3: Correlation Heatmap
# =========================
st.subheader("Stock Price Correlation Heatmap")

q4 = pd.read_csv(
    r"C:\Nithyanantham\Mini_Projects\results\stock_correlation_matrix.csv"
)

q4 = q4.set_index(q4.columns[0])
q4 = q4.apply(pd.to_numeric, errors="coerce")
q4 = q4.dropna(axis=0, how="all").dropna(axis=1, how="all")

fig, ax = plt.subplots(figsize=(12, 9))

sns.heatmap(
    q4,
    annot=False,
    cmap="viridis",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig)

st.markdown("---")

# =========================
# Row 4: Monthly Gainers & Losers
# =========================
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top 5 Monthly Gainers")

    gainers = pd.read_csv(
        r"C:\Nithyanantham\Mini_Projects\results\top5_gainers_monthwise.csv"
    )

    gainers = gainers.sort_values(["month", "monthly_return"])

    g = sns.FacetGrid(
        gainers,
        col="month",
        col_wrap=4,
        height=3,
        sharex=False,
        sharey=True
    )

    g.map_dataframe(
        sns.barplot,
        x="Ticker",
        y="monthly_return",
        color="green"
    )

    for ax in g.axes.flatten():
        ax.tick_params(axis='x', rotation=90)

    g.set_titles("{col_name}")
    g.set_axis_labels("Ticker", "Return")
    g.fig.subplots_adjust(hspace=0.8, top=0.95)
    st.pyplot(g.fig)


with col4:
    st.subheader("Top 5 Monthly Losers")

    losers = pd.read_csv(
        r"C:\Nithyanantham\Mini_Projects\results\top5_losers_monthwise.csv"
    )

    losers = losers.sort_values(["month", "monthly_return"])

    g2 = sns.FacetGrid(
        losers,
        col="month",
        col_wrap=4,
        height=3,
        sharex=False,
        sharey=True
    )

    g2.map_dataframe(
        sns.barplot,
        x="Ticker",
        y="monthly_return",
        color="red"
    )

    for ax in g2.axes.flatten():
        ax.tick_params(axis='x', rotation=90)

    g2.set_titles("{col_name}")
    g2.set_axis_labels("Ticker", "Return")
    g2.fig.subplots_adjust(hspace=0.8, top=0.95)
    st.pyplot(g2.fig)

st.markdown("---")
st.success("Dashboard loaded successfully ✅")

