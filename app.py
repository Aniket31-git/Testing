import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================
# Page Configuration
# ============================
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Retail Sales Analysis Dashboard")
st.markdown("Interactive data analysis of retail sales dataset")

# ============================
# Load Data
# ============================
@st.cache_data
def load_data():
    return pd.read_csv("retail_sales_dataset.csv")

df = load_data()

# ============================
# Sidebar Filters
# ============================
st.sidebar.header("🔧 Filters")

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include="object").columns.tolist()

selected_numeric = st.sidebar.selectbox(
    "Select numeric column",
    numeric_cols
)

selected_category = None
if categorical_cols:
    selected_category = st.sidebar.selectbox(
        "Select category column",
        categorical_cols
    )

# ============================
# KPI Section
# ============================
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Total Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Avg Value", round(df[selected_numeric].mean(), 2))

st.divider()

# ============================
# Tabs Layout
# ============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Dataset Overview",
    "📊 Distribution Analysis",
    "🏷️ Category Analysis",
    "🔗 Correlation"
])

# ============================
# Tab 1: Dataset Overview
# ============================
with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("Basic Statistics")
    st.write(df.describe())

# ============================
# Tab 2: Distribution Analysis
# ============================
with tab2:
    st.subheader(f"Distribution of {selected_numeric}")

    fig, ax = plt.subplots()
    ax.hist(df[selected_numeric])
    ax.set_xlabel(selected_numeric)
    ax.set_ylabel("Frequency")
    ax.set_title(f"{selected_numeric} Distribution")
    st.pyplot(fig)

    st.markdown("**Insights:**")
    st.write(
        f"- Shows spread and skewness of `{selected_numeric}` values.\n"
        "- Helps identify outliers and data concentration."
    )

# ============================
# Tab 3: Category-wise Analysis
# ============================
with tab3:
    if selected_category:
        st.subheader(f"{selected_numeric} by {selected_category}")

        grouped = (
            df.groupby(selected_category)[selected_numeric]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        grouped.plot(kind="bar", ax=ax)
        ax.set_ylabel(selected_numeric)
        ax.set_title(f"{selected_numeric} by {selected_category}")
        st.pyplot(fig)

        st.markdown("**Insights:**")
        st.write(
            "- Identifies top-performing categories.\n"
            "- Useful for business decision-making."
        )
    else:
        st.info("No categorical column available for analysis.")

# ============================
# Tab 4: Correlation Analysis
# ============================
with tab4:
    if len(numeric_cols) > 1:
        st.subheader("Correlation Matrix")

        corr = df[numeric_cols].corr()

        fig, ax = plt.subplots()
        cax = ax.matshow(corr)
        fig.colorbar(cax)

        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=90)
        ax.set_yticklabels(numeric_cols)

        st.pyplot(fig)

        st.markdown("**Insights:**")
        st.write(
            "- Shows relationships between numeric variables.\n"
            "- Helps detect strongly related features."
        )
    else:
        st.info("Not enough numeric columns for correlation analysis.")

# ============================
# Footer
# ============================
st.divider()
st.markdown(
    "📘 *This dashboard is designed for data analysis, visualization, and academic project demonstration.*"
)

