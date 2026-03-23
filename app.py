import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Unlearn", page_icon="🔴", layout="wide")

# --- Load Data ---
df_all = pd.read_csv("data/unlearn_all_years.csv")
df_2023 = df_all[(df_all["Year"] == 2023) & (df_all["State_UT"] != "ALL INDIA")]
df_india = df_all[df_all["State_UT"] == "ALL INDIA"]

# --- Crime labels ---
crime_cols_I = {
    "Rape": "Rape_I",
    "Attempt to Commit Rape": "Attempt_to_Commit_Rape_I",
    "Dowry Deaths": "Dowry_Deaths_I",
    "Assault on Women": "Assault_on_Women_Modesty_I",
    "Sexual Harassment": "Sexual_Harassment_I",
    "Stalking": "Stalking_I",
    "Voyeurism": "Voyeurism_I",
    "Disrobe (Sec.354B)": "Disrobe_Sec354B_I",
    "Kidnapping & Abduction": "Kidnapping_Abduction_Women_I",
    "Human Trafficking": "Human_Trafficking_I",
    "Cruelty by Husband/Relatives": "Cruelty_by_Husband_Relatives_I",
    "Insult to Modesty": "Insult_to_Modesty_Sec509_I",
}

# --- Hero Section ---
st.title("🔴 Unlearn")
st.subheader("Crime against women in India — 2019 to 2023")
st.markdown(
    "Every number below is a person. "
    "This is not a statistic problem. It is a people problem."
)
st.markdown("---")

# --- Hero Metrics (2023 vs 2019) ---
india_2023 = df_india[df_india["Year"] == 2023].iloc[0]
india_2019 = df_india[df_india["Year"] == 2019].iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Rape Cases (2023)",
    f"{int(india_2023['Rape_I']):,}",
    delta=f"{int(india_2023['Rape_I']) - int(india_2019['Rape_I']):+,} vs 2019",
    delta_color="inverse"
)
col2.metric(
    "Cruelty by Husband (2023)",
    f"{int(india_2023['Cruelty_by_Husband_Relatives_I']):,}",
    delta=f"{int(india_2023['Cruelty_by_Husband_Relatives_I']) - int(india_2019['Cruelty_by_Husband_Relatives_I']):+,} vs 2019",
    delta_color="inverse"
)
col3.metric(
    "Stalking Cases (2023)",
    f"{int(india_2023['Stalking_I']):,}",
    delta=f"{int(india_2023['Stalking_I']) - int(india_2019['Stalking_I']):+,} vs 2019",
    delta_color="inverse"
)
col4.metric(
    "Kidnapping & Abduction (2023)",
    f"{int(india_2023['Kidnapping_Abduction_Women_I']):,}",
    delta=f"{int(india_2023['Kidnapping_Abduction_Women_I']) - int(india_2019['Kidnapping_Abduction_Women_I']):+,} vs 2019",
    delta_color="inverse"
)

st.markdown("---")

# --- Chart 1: Trends Over Years ---
st.subheader("📈 How are crimes trending over the years? (All India)")

selected_crimes_trend = st.multiselect(
    "Select crimes to compare:",
    list(crime_cols_I.keys()),
    default=["Rape", "Cruelty by Husband/Relatives", "Stalking", "Kidnapping & Abduction"]
)

if selected_crimes_trend:
    trend_data = []
    for crime in selected_crimes_trend:
        col = crime_cols_I[crime]
        for _, row in df_india.iterrows():
            trend_data.append({
                "Year": int(row["Year"]),
                "Cases": row[col],
                "Crime": crime
            })
    trend_df = pd.DataFrame(trend_data)
    fig_trend = px.line(
        trend_df, x="Year", y="Cases", color="Crime", markers=True,
        title="Crime Trends Over Years — All India"
    )
    fig_trend.update_layout(xaxis=dict(tickvals=[2019, 2021, 2022, 2023]))
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption("Note: 2020 data not available in this dataset.")
else:
    st.info("Select at least one crime to see the trend.")

st.markdown("---")

# --- Chart 2: Crime Category Totals (2023) ---
st.subheader("📊 What crimes are most common? (All India, 2023)")

chart1_data = pd.DataFrame({
    "Crime": list(crime_cols_I.keys()),
    "Cases": [int(india_2023[col]) for col in crime_cols_I.values()]
}).sort_values("Cases", ascending=True)

fig1 = px.bar(
    chart1_data, x="Cases", y="Crime", orientation="h",
    color="Cases", color_continuous_scale="Reds",
    title="Total Reported Cases by Crime Type — All India 2023"
)
fig1.update_layout(showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- Chart 3: Top 10 States ---
st.subheader("🗺️ Which states report the most cases? (2023)")

all_I_cols = [col for col in df_2023.columns if col.endswith("_I")]
df_2023 = df_2023.copy()
df_2023["Total_Crimes"] = df_2023[all_I_cols].sum(axis=1)
top10 = df_2023.nlargest(10, "Total_Crimes").sort_values("Total_Crimes", ascending=True)

fig2 = px.bar(
    top10, x="Total_Crimes", y="State_UT", orientation="h",
    color="Total_Crimes", color_continuous_scale="Reds",
    title="Top 10 States by Total Crimes Against Women — 2023"
)
fig2.update_layout(showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- Chart 4: State comparison ---
st.subheader("🔍 Compare states by specific crime (2023)")

selected_crime = st.selectbox("Select a crime:", list(crime_cols_I.keys()))
selected_col = crime_cols_I[selected_crime]
use_rate = st.toggle("Show crime rate per lakh population (fairer comparison)", value=False)

if use_rate:
    rate_col = selected_col.replace("_I", "_R")
    fig3_data = df_2023[["State_UT", rate_col]].sort_values(rate_col, ascending=True)
    fig3 = px.bar(fig3_data, x=rate_col, y="State_UT", orientation="h",
                  color=rate_col, color_continuous_scale="Reds",
                  title=f"{selected_crime} — Rate per Lakh Population, 2023")
else:
    fig3_data = df_2023[["State_UT", selected_col]].sort_values(selected_col, ascending=True)
    fig3 = px.bar(fig3_data, x=selected_col, y="State_UT", orientation="h",
                  color=selected_col, color_continuous_scale="Reds",
                  title=f"{selected_crime} — Total Cases by State, 2023")

fig3.update_layout(showlegend=False, coloraxis_showscale=False, height=800)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- What Next ---
st.subheader("💡 What can we do?")
st.markdown("""
The data is stark. But data alone doesn't change behaviour — people do.

**Change has to come from the bottom up.**

That means reaching younger, impressionable minds — before harmful patterns are formed.

Some starting points:
- 🧠 **Workshops** on consent, respect, and healthy relationships in schools
- 📚 **Creative resources** — stories, films, and games that model healthy behaviour
- 🗣️ **Community conversations** that normalize talking about gender and safety

*This section is being built. If you know of resources or organisations doing this work, we'd love to feature them.*
""")

st.markdown("---")
st.caption("Data source: NCRB Crime in India Report 2019–2023 | Project Unlearn | Note: 2020 data unavailable. West Bengal 2019 data reflects 2018 figures per NCRB.")