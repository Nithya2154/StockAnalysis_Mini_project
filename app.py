import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# ============================================
# PAGE CONFIG & STYLING
# ============================================
st.set_page_config(
    page_title="📈 Stock Market Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .header-title {
        color: #1f3a93;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-header {
        color: #2d5aa0;
        font-size: 1.5em;
        font-weight: bold;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================


@st.cache_data
def load_data():
    """Load all CSV files"""
    try:
        data = {
            'top5_losers': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/top5_losers_monthwise.csv'),
            'before_ques': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/before_ques.csv'),
            'bottom_10_red': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/bottom10redstocks.csv'),
            'green_vs_red': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/green_vs_red_stocks.csv'),
            'question1': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/question1.csv'),
            'question2': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/question2.csv'),
            'question3': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/question3.csv'),
            'question4': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/question4.csv'),
            'stock_correlation': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/stock_correlation_matrix.csv'),
            'top_10_green': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/Top_10_Green_Stocks.csv'),
            'top5_gainers': pd.read_csv('C:/Nithyanantham/Mini_Projects/results/top5_gainers_monthwise.csv'),
        }
        return data
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        return None

# ============================================
# HELPER FUNCTIONS
# ============================================


def create_metric_card(label, value, color="blue"):
    """Create metric card"""
    return f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px;
    border-radius: 10px; text-align: center; margin: 10px;">
        <h4 style="margin: 0; font-size: 0.9em; opacity: 0.9;">{label}</h4>
        <h2 style="margin: 10px 0 0 0;">{value}</h2>
    </div>
    """

# ============================================
# MAIN APP
# ============================================


def main():
    # Load data
    data = load_data()

    if data is None:
        st.error("Failed to load data. Please check the file paths.")
        return

    # Sidebar Navigation
    st.sidebar.markdown("# 📊 Navigation")
    page = st.sidebar.radio(
        "Select a Page:",
        [
            "🏠 Dashboard Overview",
            "📈 Top Gainers & Losers",
            "🎯 Stock Performance Analysis",
            "💹 Monthly Trends",
            "📊 Correlation Analysis",
            "💰 Sector Analysis",
            "📉 Risk Analysis"
        ]
    )

    # ========== PAGE 1: DASHBOARD OVERVIEW ==========
    if page == "🏠 Dashboard Overview":
        st.markdown(
            '<p class="header-title">📊 Stock Market Analysis Dashboard</p>', unsafe_allow_html=True)
        st.markdown(
            "Welcome to the comprehensive stock market analysis platform!")
        st.divider()

        # Key Metrics
        st.markdown('<p class="section-header">Key Metrics</p>',
                    unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        green_count = data['green_vs_red'][data['green_vs_red']
                                           ['Stock_Status'] == 'Green']['Count'].values[0]
        red_count = data['green_vs_red'][data['green_vs_red']
                                         ['Stock_Status'] == 'Red']['Count'].values[0]
        total_stocks = green_count + red_count

        with col1:
            st.metric("🟢 Green Stocks", green_count,
                      f"{(green_count/total_stocks*100):.1f}%")
        with col2:
            st.metric("🔴 Red Stocks", red_count,
                      f"{(red_count/total_stocks*100):.1f}%")
        with col3:
            st.metric("📊 Total Stocks", total_stocks)
        with col4:
            st.metric("📈 Analysis Period", "2023-2024")

        st.divider()

        # Green vs Red visualization
        st.markdown(
            '<p class="section-header">Stock Status Distribution</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])

        with col1:
            fig_pie = go.Figure(data=[go.Pie(
                labels=data['green_vs_red']['Stock_Status'],
                values=data['green_vs_red']['Count'],
                hole=0.3,
                marker=dict(colors=['#2ecc71', '#e74c3c'])
            )])
            fig_pie.update_layout(title="Green vs Red Stocks", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(data['green_vs_red'],
                             x='Stock_Status',
                             y='Percentage',
                             color='Stock_Status',
                             color_discrete_map={
                                 'Green': '#2ecc71', 'Red': '#e74c3c'},
                             title='Percentage Distribution')
            fig_bar.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # Summary Statistics
        st.markdown('<p class="section-header">Summary Statistics</p>',
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Top 10 Green Stocks (Best Performers)**")
            st.dataframe(data['top_10_green'].head(
                10), use_container_width=True, hide_index=True)

        with col2:
            st.write("**Bottom 10 Red Stocks (Worst Performers)**")
            st.dataframe(data['bottom_10_red'].head(
                10), use_container_width=True, hide_index=True)

    # ========== PAGE 2: TOP GAINERS & LOSERS ==========
    elif page == "📈 Top Gainers & Losers":
        st.markdown(
            '<p class="header-title">📈 Top Gainers & Losers Analysis</p>', unsafe_allow_html=True)
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<p class="section-header">🟢 Top 10 Green Stocks</p>', unsafe_allow_html=True)
            top_10_green = data['top_10_green'].head(10)
            fig_top10 = px.bar(top_10_green,
                               x='yearly_returns' if 'yearly_returns' in top_10_green.columns else top_10_green.columns[
                                   1],
                               y='Ticker' if 'Ticker' in top_10_green.columns else top_10_green.columns[
                                   0],
                               orientation='h',
                               color_discrete_sequence=['#2ecc71'],
                               title='Top 10 Green Stocks')
            st.plotly_chart(fig_top10, use_container_width=True)
            st.dataframe(top_10_green, use_container_width=True,
                         hide_index=True)

        with col2:
            st.markdown(
                '<p class="section-header">🔴 Bottom 10 Red Stocks</p>', unsafe_allow_html=True)
            bottom_10_red = data['bottom_10_red'].head(10)
            fig_bottom10 = px.bar(bottom_10_red,
                                  x='yearly_returns' if 'yearly_returns' in bottom_10_red.columns else bottom_10_red.columns[
                                      2],
                                  y='Ticker' if 'Ticker' in bottom_10_red.columns else bottom_10_red.columns[
                                      0],
                                  orientation='h',
                                  color_discrete_sequence=['#e74c3c'],
                                  title='Bottom 10 Red Stocks')
            st.plotly_chart(fig_bottom10, use_container_width=True)
            st.dataframe(bottom_10_red, use_container_width=True,
                         hide_index=True)

        st.divider()

        # Performance metrics
        if 'before_ques' in data:
            st.markdown(
                '<p class="section-header">📊 Overall Performance Metrics</p>', unsafe_allow_html=True)
            before_ques = data['before_ques']

            col1, col2, col3 = st.columns(3)
            with col1:
                avg_green = before_ques[before_ques['Stock_Status']
                                        == 'Green']['yearly_returns'].mean()
                st.metric("Avg Green Return", f"{avg_green:.2f}%")

            with col2:
                avg_red = before_ques[before_ques['Stock_Status']
                                      == 'Red']['yearly_returns'].mean()
                st.metric("Avg Red Return", f"{avg_red:.2f}%")

            with col3:
                best_performer = before_ques.loc[before_ques['yearly_returns'].idxmax(
                )]
                st.metric(
                    "Best Performer", best_performer['Ticker'], f"{best_performer['yearly_returns']:.2f}%")

    # ========== PAGE 3: STOCK PERFORMANCE ANALYSIS ==========
    elif page == "🎯 Stock Performance Analysis":
        st.markdown(
            '<p class="header-title">🎯 Stock Performance Analysis</p>', unsafe_allow_html=True)
        st.divider()

        st.markdown(
            '<p class="section-header">Cumulative Returns by Stock</p>', unsafe_allow_html=True)

        if 'question1' in data and not data['question1'].empty:
            question1 = data['question1'].head(20)
            fig_cumulative = px.bar(question1,
                                    x='Cumulative_Return',
                                    y='Ticker',
                                    orientation='h',
                                    color='Cumulative_Return',
                                    color_continuous_scale='RdYlGn',
                                    title='Top 20 Stocks by Cumulative Return')
            st.plotly_chart(fig_cumulative, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Top Performers**")
                st.dataframe(question1.head(
                    10), use_container_width=True, hide_index=True)
            with col2:
                st.write("**Data Summary**")
                st.write(question1.describe())

        # Stock price comparison
        if 'before_ques' in data:
            st.markdown(
                '<p class="section-header">Price Movement Analysis</p>', unsafe_allow_html=True)
            before_ques = data['before_ques']

            fig_scatter = px.scatter(before_ques,
                                     x='first_close',
                                     y='last_close',
                                     color='Stock_Status',
                                     hover_data=['Ticker', 'yearly_returns'],
                                     color_discrete_map={
                                         'Green': '#2ecc71', 'Red': '#e74c3c'},
                                     title='Stock Price: Opening vs Closing')
            fig_scatter.add_shape(type="line", x0=before_ques['first_close'].min(),
                                  y0=before_ques['first_close'].min(),
                                  x1=before_ques['first_close'].max(),
                                  y1=before_ques['first_close'].max(),
                                  line=dict(dash="dash", color="gray"))
            st.plotly_chart(fig_scatter, use_container_width=True)

    # ========== PAGE 4: MONTHLY TRENDS ==========
    elif page == "💹 Monthly Trends":
        st.markdown(
            '<p class="header-title">💹 Monthly Trends Analysis</p>', unsafe_allow_html=True)
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                '<p class="section-header">Top 5 Gainers (Monthly)</p>', unsafe_allow_html=True)
            top5_gainers = data['top5_gainers']
            fig_gainers = px.line(top5_gainers,
                                  x='month',
                                  y='monthly_return',
                                  color='Ticker',
                                  title='Top Gainers Monthly Returns',
                                  markers=True)
            st.plotly_chart(fig_gainers, use_container_width=True)
            st.dataframe(top5_gainers.head(
                20), use_container_width=True, hide_index=True)

        with col2:
            st.markdown(
                '<p class="section-header">Top 5 Losers (Monthly)</p>', unsafe_allow_html=True)
            top5_losers = data['top5_losers']
            fig_losers = px.line(top5_losers,
                                 x='month',
                                 y='monthly_return',
                                 color='Ticker',
                                 title='Top Losers Monthly Returns',
                                 markers=True)
            st.plotly_chart(fig_losers, use_container_width=True)
            st.dataframe(top5_losers.head(
                20), use_container_width=True, hide_index=True)

    # ========== PAGE 5: CORRELATION ANALYSIS ==========
    elif page == "📊 Correlation Analysis":
        st.markdown(
            '<p class="header-title">📊 Stock Correlation Matrix</p>', unsafe_allow_html=True)
        st.divider()

        if 'stock_correlation' in data:
            correlation_matrix = data['stock_correlation']

            # Create heatmap
            st.markdown(
                '<p class="section-header">Correlation Heatmap</p>', unsafe_allow_html=True)

            # Set first column as index if not already
            if correlation_matrix.columns[0] not in ['Ticker', 'Symbol']:
                correlation_matrix_numeric = correlation_matrix.iloc[:, 1:].astype(
                    float)
                ticker_names = correlation_matrix.iloc[:, 0].values
                correlation_matrix_numeric.index = ticker_names
            else:
                correlation_matrix_numeric = correlation_matrix.set_index(
                    correlation_matrix.columns[0]).astype(float)

            # Create Plotly heatmap
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=correlation_matrix_numeric.values,
                x=correlation_matrix_numeric.columns,
                y=correlation_matrix_numeric.index,
                colorscale='RdBu',
                zmid=0
            ))
            fig_heatmap.update_layout(
                title='Stock Correlation Matrix', height=600)
            st.plotly_chart(fig_heatmap, use_container_width=True)

            st.write("**Correlation Matrix Data**")
            st.dataframe(correlation_matrix_numeric, use_container_width=True)

    # ========== PAGE 6: SECTOR ANALYSIS ==========
    elif page == "💰 Sector Analysis":
        st.markdown(
            '<p class="header-title">💰 Sector Performance Analysis</p>', unsafe_allow_html=True)
        st.divider()

        if 'question3' in data and not data['question3'].empty:
            question3 = data['question3']

            st.markdown(
                '<p class="section-header">Daily Returns by Sector</p>', unsafe_allow_html=True)

            fig_sector = px.bar(question3,
                                x='sector',
                                y='Daily_Return',
                                color='Daily_Return',
                                color_continuous_scale='Viridis',
                                title='Daily Returns by Sector')
            st.plotly_chart(fig_sector, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Sector Performance Table**")
                st.dataframe(question3, use_container_width=True,
                             hide_index=True)

            with col2:
                st.write("**Statistics**")
                st.write(question3.describe())

    # ========== PAGE 7: RISK ANALYSIS ==========
    elif page == "📉 Risk Analysis":
        st.markdown('<p class="header-title">📉 Risk Analysis</p>',
                    unsafe_allow_html=True)
        st.divider()

        if 'question2' in data and not data['question2'].empty:
            question2 = data['question2'].head(50).copy()

            st.markdown(
                '<p class="section-header">Stock Volatility Analysis</p>',
                unsafe_allow_html=True
            )

            # -------------------------------
            # 🔧 Data Cleaning (IMPORTANT)
            # -------------------------------
            import pandas as pd

            # Convert columns to numeric where possible
            for col in question2.columns:
                question2[col] = pd.to_numeric(question2[col], errors='coerce')

            # Drop rows where X or Y is missing
            if len(question2.columns) >= 2:
                question2 = question2.dropna(
                    subset=[question2.columns[0], question2.columns[1]]
                )

            # -------------------------------
            # 📊 Scatter Plot
            # -------------------------------
            if len(question2.columns) >= 2:

                # Validate size column
                size_col = None
                if len(question2.columns) > 2:
                    col3 = question2.columns[2]
                    if pd.api.types.is_numeric_dtype(question2[col3]):
                        size_col = col3

                fig_risk = px.scatter(
                    question2,
                    x=question2.columns[0],
                    y=question2.columns[1],
                    size=size_col,  # Only used if valid
                    hover_data=question2.columns[:4],
                    title='Risk vs Return Analysis',
                    labels={
                        question2.columns[0]: 'Risk',
                        question2.columns[1]: 'Return'
                    }
                )

                st.plotly_chart(fig_risk, use_container_width=True)

            # -------------------------------
            # 📋 Data Table
            # -------------------------------
            st.write("**Risk Analysis Data**")
            st.dataframe(
                question2.head(30),
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------
            # 📈 Summary Metrics
            # -------------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Records", len(question2))

            with col2:
                if len(question2.columns) > 1:
                    avg_val = question2.iloc[:, 1].mean()
                    st.metric("Avg Value", f"{avg_val:.4f}" if pd.notna(
                        avg_val) else "N/A")

            with col3:
                if len(question2.columns) > 1:
                    std_val = question2.iloc[:, 1].std()
                    st.metric("Std Dev", f"{std_val:.4f}" if pd.notna(
                        std_val) else "N/A")
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9em; margin-top: 50px;">
        <p>📊 Stock Market Analysis Dashboard | Data Period: 2023-2024</p>
        <p>Built with Streamlit | Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
