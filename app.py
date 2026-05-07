import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ================================================
# PAGE CONFIG
# ================================================
st.set_page_config(
    page_title="Kenya CPI & Inflation Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================================================
# LOAD DATA
# ================================================
@st.cache_data
def load_data():
    base = "https://raw.githubusercontent.com/FelixBeruTheAnalyst/kenya-cpi-inflation-analysis/main/"
    df_div = pd.read_csv(base + "kenya_cpi_divisions.csv")
    df_com = pd.read_csv(base + "kenya_cpi_commodities.csv")
    df_core = pd.read_csv(base + "kenya_cpi_core_noncore.csv")
    return df_div, df_com, df_core

df_divisions, df_commodities, df_core = load_data()

# Calculate weighted contributions
overall_inflation = 4.4
df_divisions['Weighted_Contribution'] = (
    df_divisions['Weight'] / 100 * df_divisions['Annual_Change']
).round(3)

# ================================================
# COLOR FUNCTIONS
# ================================================
def div_color(inflation):
    if inflation > 6: return '#e74c3c'
    elif inflation > overall_inflation: return '#f39c12'
    elif inflation > 2: return '#3498db'
    else: return '#2ecc71'

def com_color(change):
    if change > 15: return '#e74c3c'
    elif change > 5: return '#f39c12'
    elif change >= 0: return '#3498db'
    else: return '#2ecc71'

# ================================================
# SIDEBAR
# ================================================
st.sidebar.title("📊 Kenya CPI Dashboard")
st.sidebar.markdown("**March 2025 – March 2026**")
st.sidebar.markdown("*Source: KNBS*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview",
     "📊 Inflation by Division",
     "🛒 Commodity Prices",
     "📈 Core vs Non-Core",
     "⚖️ Weighted Impact"]
)

st.sidebar.divider()
st.sidebar.metric("Overall Inflation", "4.4%")
st.sidebar.metric("Core Inflation", "2.1%")
st.sidebar.metric("Non-Core Inflation", "10.8%")
st.sidebar.divider()
st.sidebar.caption(
    "Built by Felix Beru Tsinzole\n"
    "Financial & Data Analyst\n"
    "Nairobi, Kenya"
)

# ================================================
# PAGE 1 — OVERVIEW
# ================================================
if page == "🏠 Overview":
    st.title("🇰🇪 Kenya CPI & Inflation Dashboard")
    st.markdown("**Consumer Price Index Analysis | March 2025 – March 2026**")
    st.markdown("*Source: Kenya National Bureau of Statistics (KNBS) | Analyst: Felix Beru Tsinzole*")
    st.divider()

    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Overall Inflation", "4.4%",
                  delta="0.5% vs last month")
    with col2:
        st.metric("Core Inflation", "2.1%",
                  delta="-0.1% vs last month")
    with col3:
        st.metric("Non-Core Inflation", "10.8%",
                  delta="0.7% vs last month",
                  delta_color="inverse")
    with col4:
        st.metric("Food Inflation", "7.7%",
                  delta="Highest division",
                  delta_color="inverse")
    with col5:
        st.metric("Core/Non-Core Gap", "8.7 pp",
                  delta="Food & energy driven",
                  delta_color="inverse")

    st.divider()

    # Headline finding
    st.subheader("🔍 Headline Finding")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.error("""
        **Food prices are responsible for 62.6% of Kenya's total inflation.**

        Food and Non-Alcoholic Beverages contributes **2.53 percentage points**
        to Kenya's overall 4.4% inflation rate — despite being just one of
        13 expenditure divisions.

        Cabbages (+33.8%), Tomatoes (+23.2%) and Potatoes (+18.8%) are
        the sharpest commodity price increases over the past year.
        """)

    with col_b:
        st.info("""
        **The good news:**

        Core inflation — which excludes food and energy — is
        stable at just **2.1%**.

        Kenya does not have a structural inflation problem.
        The crisis is driven entirely by food and energy
        price shocks — which can ease faster than
        structural inflation.
        """)

    st.divider()

    # Quick overview charts side by side
    st.subheader("📊 Quick Overview")
    col1, col2 = st.columns(2)

    with col1:
        # Division bar chart mini
        df_sorted = df_divisions.sort_values('Annual_Change', ascending=True)
        colors = [div_color(x) for x in df_sorted['Annual_Change']]

        fig1 = go.Figure(go.Bar(
            x=df_sorted['Annual_Change'],
            y=df_sorted['Division'],
            orientation='h',
            marker_color=colors,
            hovertemplate='<b>%{y}</b><br>Annual Inflation: %{x:.1f}%<extra></extra>'
        ))
        fig1.add_vline(x=overall_inflation, line_dash='dash',
                       line_color='navy',
                       annotation_text=f'Overall: {overall_inflation}%',
                       annotation_font_color='navy')
        fig1.update_layout(
            title='Inflation by Division',
            height=400,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(range=[0, 10]),
            yaxis=dict(tickfont=dict(size=9))
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Core vs non-core line mini
        x = list(range(len(df_core)))
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_core['Period'],
            y=df_core['Core_Inflation'],
            mode='lines+markers',
            name='Core Inflation',
            line=dict(color='#3498db', width=2.5),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>Core: %{y:.1f}%<extra></extra>'
        ))
        fig2.add_trace(go.Scatter(
            x=df_core['Period'],
            y=df_core['NonCore_Inflation'],
            mode='lines+markers',
            name='Non-Core Inflation',
            line=dict(color='#e74c3c', width=2.5),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>Non-Core: %{y:.1f}%<extra></extra>'
        ))
        fig2.update_layout(
            title='Core vs Non-Core Trend',
            height=400,
            plot_bgcolor='#f8f9fa',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis=dict(tickangle=45, tickfont=dict(size=9))
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.caption("Kenya National Bureau of Statistics (KNBS) | CPI Report March 2026 | Analysis by Felix Beru Tsinzole")

# ================================================
# PAGE 2 — INFLATION BY DIVISION
# ================================================
elif page == "📊 Inflation by Division":
    st.title("📊 Inflation by COICOP Division")
    st.markdown("**13 expenditure divisions ranked by annual inflation rate**")
    st.divider()

    # Metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        above = len(df_divisions[df_divisions['Annual_Change'] > overall_inflation])
        st.metric("Divisions Above Average", f"{above} of 13")
    with col2:
        st.metric("Highest Division", "Food — 7.7%")
    with col3:
        st.metric("Lowest Division", "Info & Comms — 0.5%")

    st.divider()

    # Filter
    view = st.radio("View", ["Annual Change", "Monthly Change", "Both"],
                    horizontal=True)

    df_sorted = df_divisions.sort_values('Annual_Change', ascending=True)
    colors = [div_color(x) for x in df_sorted['Annual_Change']]

    if view == "Annual Change":
        fig = go.Figure(go.Bar(
            x=df_sorted['Annual_Change'],
            y=df_sorted['Division'],
            orientation='h',
            marker_color=colors,
            text=df_sorted['Annual_Change'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>'
                          'Annual Inflation: %{x:.1f}%<br>'
                          '<extra></extra>'
        ))
        fig.add_vline(x=overall_inflation, line_dash='dash',
                      line_color='navy',
                      annotation_text=f'◄ Overall: {overall_inflation}%',
                      annotation_font_color='navy',
                      annotation_font_size=11)
        fig.update_layout(
            title='Annual Inflation Rate by Division — March 2026 vs March 2025',
            height=550,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(range=[0, 11], title='Annual Inflation Rate (%)'),
            yaxis=dict(tickfont=dict(size=10))
        )

    elif view == "Monthly Change":
        df_monthly = df_divisions.sort_values('Monthly_Change', ascending=True)
        colors_m = ['#e74c3c' if x > 0.5 else '#f39c12'
                    if x > 0.2 else '#3498db'
                    if x > 0 else '#2ecc71'
                    for x in df_monthly['Monthly_Change']]
        fig = go.Figure(go.Bar(
            x=df_monthly['Monthly_Change'],
            y=df_monthly['Division'],
            orientation='h',
            marker_color=colors_m,
            text=df_monthly['Monthly_Change'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>'
                          'Monthly Change: %{x:.1f}%<br>'
                          '<extra></extra>'
        ))
        fig.update_layout(
            title='Monthly Inflation Rate — March 2026 vs February 2026',
            height=550,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(title='Monthly Change (%)'),
            yaxis=dict(tickfont=dict(size=10))
        )

    else:
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=('Annual Change (%)',
                                            'Monthly Change (%)'))
        fig.add_trace(go.Bar(
            x=df_sorted['Annual_Change'],
            y=df_sorted['Division'],
            orientation='h',
            marker_color=colors,
            name='Annual',
            hovertemplate='<b>%{y}</b><br>Annual: %{x:.1f}%<extra></extra>'
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=df_divisions.sort_values('Monthly_Change')['Monthly_Change'],
            y=df_divisions.sort_values('Monthly_Change')['Division'],
            orientation='h',
            marker_color='#9b59b6',
            name='Monthly',
            hovertemplate='<b>%{y}</b><br>Monthly: %{x:.1f}%<extra></extra>'
        ), row=1, col=2)
        fig.update_layout(height=550, plot_bgcolor='#f8f9fa',
                          showlegend=False)
        fig.update_yaxes(tickfont=dict(size=9))

    st.plotly_chart(fig, use_container_width=True)

    # Division weight table
    st.subheader("📋 Division Details")
    st.dataframe(
        df_divisions[['Division', 'Weight', 'Monthly_Change',
                      'Annual_Change', 'Weighted_Contribution']]
        .sort_values('Annual_Change', ascending=False)
        .rename(columns={
            'Monthly_Change': 'Monthly Change (%)',
            'Annual_Change': 'Annual Change (%)',
            'Weighted_Contribution': 'Weighted Contribution (pp)'
        })
        .set_index('Division'),
        use_container_width=True
    )

# ================================================
# PAGE 3 — COMMODITY PRICES
# ================================================
elif page == "🛒 Commodity Prices":
    st.title("🛒 Commodity Price Movement")
    st.markdown("**17 key commodities — annual and monthly price changes**")
    st.divider()

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        top = df_commodities.loc[df_commodities['Annual_Change'].idxmax()]
        st.metric("Biggest Annual Increase",
                  f"{top['Commodity']}",
                  delta=f"+{top['Annual_Change']:.1f}%",
                  delta_color="inverse")
    with col2:
        bottom = df_commodities.loc[df_commodities['Annual_Change'].idxmin()]
        st.metric("Biggest Annual Decrease",
                  f"{bottom['Commodity']}",
                  delta=f"{bottom['Annual_Change']:.1f}%")
    with col3:
        rising = len(df_commodities[df_commodities['Annual_Change'] > 0])
        st.metric("Commodities Rising", f"{rising} of {len(df_commodities)}")

    st.divider()

    # Chart selector
    chart_type = st.selectbox(
        "Select View",
        ["Annual Price Change (%)",
         "Monthly Price Change (%)",
         "Price Comparison — March 2025 vs March 2026"]
    )

    if chart_type == "Annual Price Change (%)":
        df_sorted = df_commodities.sort_values('Annual_Change', ascending=True)
        colors = [com_color(x) for x in df_sorted['Annual_Change']]

        fig = go.Figure(go.Bar(
            x=df_sorted['Annual_Change'],
            y=df_sorted['Commodity'],
            orientation='h',
            marker_color=colors,
            text=df_sorted['Annual_Change'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>'
                          'Annual Change: %{x:.1f}%<br>'
                          '<extra></extra>'
        ))
        fig.add_vline(x=0, line_color='navy', line_width=1.5,
                      line_dash='dash')
        fig.update_layout(
            title='Annual Price Change by Commodity — March 2026 vs March 2025',
            height=550,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(title='Annual Price Change (%)'),
            yaxis=dict(tickfont=dict(size=10))
        )

    elif chart_type == "Monthly Price Change (%)":
        df_sorted = df_commodities.sort_values('Monthly_Change', ascending=True)
        colors_m = ['#e74c3c' if x > 5 else '#f39c12'
                    if x > 0 else '#2ecc71'
                    for x in df_sorted['Monthly_Change']]
        fig = go.Figure(go.Bar(
            x=df_sorted['Monthly_Change'],
            y=df_sorted['Commodity'],
            orientation='h',
            marker_color=colors_m,
            text=df_sorted['Monthly_Change'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>'
                          'Monthly Change: %{x:.1f}%<br>'
                          '<extra></extra>'
        ))
        fig.add_vline(x=0, line_color='navy', line_width=1.5,
                      line_dash='dash')
        fig.update_layout(
            title='Monthly Price Change — March 2026 vs February 2026',
            height=550,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(title='Monthly Change (%)'),
            yaxis=dict(tickfont=dict(size=10))
        )

    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_commodities['Price_March2025'],
            y=df_commodities['Commodity'],
            orientation='h',
            name='March 2025',
            marker_color='#95a5a6',
            hovertemplate='<b>%{y}</b><br>March 2025: KES %{x:.2f}<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            x=df_commodities['Price_March2026'],
            y=df_commodities['Commodity'],
            orientation='h',
            name='March 2026',
            marker_color='#e74c3c',
            hovertemplate='<b>%{y}</b><br>March 2026: KES %{x:.2f}<extra></extra>'
        ))
        fig.update_layout(
            title='Commodity Prices — March 2025 vs March 2026 (KES)',
            barmode='group',
            height=550,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(title='Average Retail Price (KES)'),
            yaxis=dict(tickfont=dict(size=10)),
            legend=dict(orientation='h', yanchor='bottom', y=1.02)
        )

    st.plotly_chart(fig, use_container_width=True)

    # Full price table
    st.subheader("📋 Full Commodity Price Table")
    st.dataframe(
        df_commodities[['Commodity', 'Unit', 'Price_March2025',
                        'Price_Feb2026', 'Price_March2026',
                        'Monthly_Change', 'Annual_Change']]
        .rename(columns={
            'Price_March2025': 'Mar 2025 (KES)',
            'Price_Feb2026': 'Feb 2026 (KES)',
            'Price_March2026': 'Mar 2026 (KES)',
            'Monthly_Change': 'Monthly (%)',
            'Annual_Change': 'Annual (%)'
        })
        .set_index('Commodity'),
        use_container_width=True
    )

# ================================================
# PAGE 4 — CORE VS NON-CORE
# ================================================
elif page == "📈 Core vs Non-Core":
    st.title("📈 Core vs Non-Core Inflation Trend")
    st.markdown("**Monthly trend — March 2025 to March 2026**")
    st.divider()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Core Inflation (Mar 26)",
                  f"{df_core['Core_Inflation'].iloc[-1]}%")
    with col2:
        st.metric("Non-Core Inflation (Mar 26)",
                  f"{df_core['NonCore_Inflation'].iloc[-1]}%",
                  delta_color="inverse")
    with col3:
        gap = df_core['NonCore_Inflation'].iloc[-1] - df_core['Core_Inflation'].iloc[-1]
        st.metric("Divergence Gap", f"{gap:.1f} pp")
    with col4:
        peak = df_core['NonCore_Inflation'].max()
        peak_month = df_core.loc[df_core['NonCore_Inflation'].idxmax(), 'Period']
        st.metric("Peak Non-Core", f"{peak}%",
                  delta=f"in {peak_month}",
                  delta_color="inverse")

    st.divider()

    # View selector
    view = st.radio("Select View",
                    ["Inflation Rate Trend", "Index Level Trend", "Both"],
                    horizontal=True)

    if view == "Inflation Rate Trend" or view == "Both":
        fig_rate = go.Figure()
        fig_rate.add_trace(go.Scatter(
            x=df_core['Period'],
            y=df_core['Core_Inflation'],
            mode='lines+markers',
            name='Core Inflation',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Core: %{y:.1f}%<extra></extra>'
        ))
        fig_rate.add_trace(go.Scatter(
            x=df_core['Period'],
            y=df_core['NonCore_Inflation'],
            mode='lines+markers',
            name='Non-Core Inflation',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Non-Core: %{y:.1f}%<extra></extra>'
        ))
        fig_rate.add_trace(go.Scatter(
            x=list(df_core['Period']) + list(df_core['Period'])[::-1],
            y=list(df_core['NonCore_Inflation']) + list(df_core['Core_Inflation'])[::-1],
            fill='toself',
            fillcolor='rgba(231, 76, 60, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Divergence Gap',
            hoverinfo='skip'
        ))
        fig_rate.update_layout(
            title='Core vs Non-Core Inflation Rate — March 2025 to March 2026',
            height=450,
            plot_bgcolor='#f8f9fa',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis=dict(tickangle=45, tickfont=dict(size=10)),
            yaxis=dict(title='Inflation Rate (%)', tickfont=dict(size=10))
        )
        st.plotly_chart(fig_rate, use_container_width=True)

    if view == "Index Level Trend" or view == "Both":
        fig_idx = go.Figure()
        fig_idx.add_trace(go.Scatter(
            x=df_core['Period'],
            y=df_core['Core_Index'],
            mode='lines+markers',
            name='Core Index',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Core Index: %{y:.2f}<extra></extra>'
        ))
        fig_idx.add_trace(go.Scatter(
            x=df_core['Period'],
            y=df_core['NonCore_Index'],
            mode='lines+markers',
            name='Non-Core Index',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Non-Core Index: %{y:.2f}<extra></extra>'
        ))
        fig_idx.update_layout(
            title='Core vs Non-Core Index Level — March 2025 to March 2026',
            height=450,
            plot_bgcolor='#f8f9fa',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            xaxis=dict(tickangle=45, tickfont=dict(size=10)),
            yaxis=dict(title='Index Level', tickfont=dict(size=10))
        )
        st.plotly_chart(fig_idx, use_container_width=True)

    # Insight box
    st.divider()
    st.subheader("💡 What This Means")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("""
        **Core inflation is stable (2.0% – 3.1%)**

        Kenya's underlying cost of services, wages and rents
        is not spiralling. This is the inflation central banks
        watch most closely — and it is well controlled.
        """)
    with col_b:
        st.error("""
        **Non-core inflation peaked at 11.2% in December 2025**

        Food and energy price shocks are driving Kenya's
        inflation crisis. The 8.7 pp divergence gap between
        core and non-core is unusually wide — signalling
        supply-side pressures rather than broad overheating.
        """)

# ================================================
# PAGE 5 — WEIGHTED IMPACT
# ================================================
elif page == "⚖️ Weighted Impact":
    st.title("⚖️ Weighted Inflation Contribution Analysis")
    st.markdown("**How much does each division contribute to Kenya's 4.4% overall inflation?**")
    st.divider()

    total_contribution = df_divisions['Weighted_Contribution'].sum()

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        food_contrib = df_divisions[
            df_divisions['Division'].str.contains('Food')
        ]['Weighted_Contribution'].values[0]
        st.metric("Food Contribution",
                  f"{food_contrib:.3f} pp",
                  delta=f"{food_contrib/total_contribution*100:.1f}% of total",
                  delta_color="inverse")
    with col2:
        st.metric("Total Weighted Contribution",
                  f"{total_contribution:.2f} pp",
                  delta="vs 4.4% reported")
    with col3:
        top_div = df_divisions.loc[df_divisions['Weighted_Contribution'].idxmax(), 'Division']
        st.metric("Biggest Contributor", top_div.split()[0])

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        df_weighted = df_divisions.sort_values('Weighted_Contribution', ascending=True)

        def contrib_color(c):
            if c > 1.0: return '#e74c3c'
            elif c > 0.5: return '#f39c12'
            elif c > 0.2: return '#3498db'
            else: return '#2ecc71'

        colors_w = [contrib_color(x) for x in df_weighted['Weighted_Contribution']]

        fig_w = go.Figure(go.Bar(
            x=df_weighted['Weighted_Contribution'],
            y=df_weighted['Division'],
            orientation='h',
            marker_color=colors_w,
            text=df_weighted['Weighted_Contribution'].apply(lambda x: f'{x:.3f} pp'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>'
                          'Contribution: %{x:.3f} pp<br>'
                          '<extra></extra>'
        ))
        fig_w.update_layout(
            title='Weighted Contribution to Overall Inflation (percentage points)',
            height=500,
            plot_bgcolor='#f8f9fa',
            xaxis=dict(title='Contribution (pp)', tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10))
        )
        st.plotly_chart(fig_w, use_container_width=True)

    with col2:
        # Pie chart
        top5 = df_divisions.nlargest(5, 'Weighted_Contribution')
        others = total_contribution - top5['Weighted_Contribution'].sum()
        pie_labels = list(top5['Division'].str.split().str[0]) + ['Others']
        pie_values = list(top5['Weighted_Contribution']) + [others]
        pie_colors = ['#e74c3c', '#f39c12', '#3498db',
                      '#9b59b6', '#1abc9c', '#95a5a6']

        fig_pie = go.Figure(go.Pie(
            labels=pie_labels,
            values=pie_values,
            marker=dict(colors=pie_colors,
                       line=dict(color='white', width=2)),
            hovertemplate='<b>%{label}</b><br>'
                          'Contribution: %{value:.3f} pp<br>'
                          'Share: %{percent}<extra></extra>',
            textfont=dict(size=11)
        ))
        fig_pie.update_layout(
            title='Share of Total\nInflation',
            height=500,
            legend=dict(font=dict(size=9))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Full table
    st.subheader("📋 Full Weighted Contribution Table")
    st.dataframe(
        df_divisions[['Division', 'Weight', 'Annual_Change', 'Weighted_Contribution']]
        .sort_values('Weighted_Contribution', ascending=False)
        .rename(columns={
            'Weight': 'Weight (%)',
            'Annual_Change': 'Annual Inflation (%)',
            'Weighted_Contribution': 'Weighted Contribution (pp)'
        })
        .set_index('Division'),
        use_container_width=True
    )

    st.divider()
    st.subheader("💡 Business Implications")
    st.warning("""
    **For businesses serving rural Kenyan households:**

    - 🔴 **Collections risk** — rising food costs reduce household disposable income
    - 🟢 **Value proposition strengthens** — as energy costs rise, affordable alternatives become attractive
    - ⚠️ **Pricing sensitivity** — rural consumers are more price sensitive than ever
    - 📊 **Forecast** — if food inflation eases by 3%, overall inflation drops by ~1 percentage point
    """)

st.divider()
st.caption(
    "Source: Kenya National Bureau of Statistics (KNBS) | "
    "CPI Report March 2026 | "
    "Built by Felix Beru Tsinzole | "
    "Financial & Data Analyst | Nairobi, Kenya"
)