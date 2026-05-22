import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Universal CSV Dashboard", layout="wide")

# App Title
st.title(" Universal CSV Dashboard")
st.markdown("Upload any CSV dataset to generate interactive charts dynamically.")



# File Uploader Component
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load data safely
        df = pd.read_csv(uploaded_file)
        
        # 1. Dataset Preview Section
        st.subheader("📋 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Display basic metadata
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Missing Values", df.isna().sum().sum())
        
        st.markdown("---")
        
        # Separate columns by data type for smarter chart options
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        all_cols = df.columns.tolist()

        # 2. Dynamic Chart Builder Section
        st.subheader("📈 Interactive Chart Builder")
        
        # Sidebar controls for chart customization
        st.sidebar.header("Chart Settings")
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"]
        )
        
        # Dynamic axis assignment based on chart type selection
        if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
            x_axis = st.sidebar.selectbox("Select X-Axis", all_cols)
            y_axis = st.sidebar.selectbox("Select Y-Axis (Numeric preferred)", numeric_cols if numeric_cols else all_cols)
            color_by = st.sidebar.selectbox("Color / Group By (Optional)", [None] + categorical_cols)
            
        elif chart_type == "Pie Chart":
            names = st.sidebar.selectbox("Select Labels (Categorical)", categorical_cols if categorical_cols else all_cols)
            values = st.sidebar.selectbox("Select Values (Numeric)", numeric_cols if numeric_cols else all_cols)
            
        elif chart_type in ["Histogram", "Box Plot"]:
            x_axis = st.sidebar.selectbox("Select Variable", numeric_cols if numeric_cols else all_cols)
            color_by = st.sidebar.selectbox("Color / Group By (Optional)", [None] + categorical_cols)

        # Chart Rendering Logic
        fig = None
        
        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} by {x_axis}")
            
        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} over {x_axis}")
            
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} vs {x_axis}")
            
        elif chart_type == "Pie Chart":
            fig = px.pie(df, names=names, values=values, title=f"Distribution of {values} by {names}")
            
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis, color=color_by, title=f"Distribution of {x_axis}")
            
        elif chart_type == "Box Plot":
            fig = px.box(df, y=x_axis, color=color_by, title=f"Box Plot of {x_axis}")

        # Display the generated chart
        if fig:
            fig.update_layout(template="plotly_white", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)
            
        # 3. Data Summary Statistics
        st.markdown("---")
        st.subheader("💡 Summary Statistics")
        st.dataframe(df.describe(include='all').fillna(''), use_container_width=True)

    except Exception as e:
        st.error(f"Error parsing file: {e}. Please ensure it is a valid, well-formatted CSV.")

else:
    # Landing page state before file upload
    st.info("👋 Welcome! Please upload a CSV file using the sidebar to get started.")
    
    # Simple mockup visual of how it works
    st.image(
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80", 
        caption="Upload data to visualize insights instantly.", 
        width=500
    )