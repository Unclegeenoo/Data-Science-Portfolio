import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
        </style>
    """, unsafe_allow_html=True)

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

    ##plt.figure(figsize=(2, 1))

    # Visualize the growth using a bar chart
    
    fig, ax = plt.subplots(figsize=(4, 1))
    ax.bar(data['Source'], data['Growth'])
    ax.set_xlabel('Source', fontsize=6)  # Adjust the fontsize for x-axis label
    ax.set_ylabel('Growth in Gold Bars', fontsize=6)  # Adjust the fontsize for y-axis label
    ax.set_title('Growth in Gold Bars per Source', fontsize=10)  # Adjust the fontsize for the title

    # Display the chart using Streamlit
    st.pyplot(plt)





def show_financial_analysis():
    st.header("Financial Data")
    # Add your financial analysis code and visualizations here

def show_attendance_data():
    st.header("Attendance Data")
    # Add your attendance data analysis code and visualizations here

def show_conclusions():
    st.header("Conclusions")
    # Add your conclusions and summary text here

if __name__ == "__main__":
    main()
