import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(layout='wide')

def main():
    # Custom CSS styles
    sidebar_style = """
        background-color: #ff0000;
        padding: 20px;
    """

    page_style = """
        background-color: #f9f9f9;
        padding: 20px;
    """

    title_style = """
        color: blue;
    """

    # Apply custom styles
    st.markdown(f"""
        <style>
            .sidebar .sidebar-content {{
                {sidebar_style}
            }}
            .reportview-container .main .block-container {{
                {page_style}
            }}
            h1, .css-1q9ytk9 {{
                {title_style}
            }}
            .sidebar .sidebar-content .st-image {{
                margin-top: -20x;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Display the image in the sidebar
    image = Image.open("mlclogo.png")
    st.sidebar.image(image, use_column_width=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", ("General", "Financial Data", "Attendance Data", "Conclusions"))

    if section == "General":
        st.markdown("<h1 style='text-align: left; white-space: nowrap;'>Moscow Lacrosse Club Financial and Attendance Data Analysis</h1>", unsafe_allow_html=True)
        show_general_stats()
    elif section == "Financial Data":
        show_financial_analysis()
    elif section == "Attendance Data":
        show_attendance_data()
    else:
        show_conclusions()

def show_general_stats():
    st.header("General Statistics")
    # Add your general statistics code and visualizations here
    data = pd.DataFrame({
        'Source': ['Africa', 'Asia', 'South America', 'North America'],
        'Jan': [5, 3, 1, 3],
        'Feb': [8, 4, 2, 4],
        'Mar': [8, 5, 2, 5],
        'Apr': [9, 8, 3, 6]
    })

    data['Growth'] = data['Apr'] - data['Jan']

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(data['Source'], data['Growth'])
    ax.set_xlabel('Source', fontsize=12)
    ax.set_ylabel('Growth in Gold Bars', fontsize=12)
    ax.set_title('Growth in Gold Bars per Source', fontsize=16)

    # Display the chart using Streamlit
    st.pyplot(fig)

def show_financial_analysis():
    st.header("Financial Data")

    # Display the selected subsection content
    selected_subsection = st.sidebar.radio("Go to", ("Summary", "Income", "Expenses"))

    if selected_subsection == "Summary":
        # Add your summary analysis and visualizations here
        st.subheader("Summary Section Content")
    elif selected_subsection == "Income":
        # Add your income analysis and visualizations here
        st.subheader("Income Section Content")
    elif selected_subsection == "Expenses":
        # Add your expenses analysis and visualizations here
        st.subheader("Expenses Section Content")

def show_attendance_data():
    st.header("Attendance Data")
    # Add your attendance data analysis code and visualizations here

def show_conclusions():
    st.header("Conclusions")
    # Add your conclusions and summary text here

if __name__ == "__main__":
    main()

