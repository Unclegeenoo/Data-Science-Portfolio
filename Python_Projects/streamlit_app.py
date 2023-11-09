import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(layout='wide')

############## Data Bank ####################
data = pd.DataFrame({
        'Source': ['Africa', 'Asia', 'South America', 'North America'],
        'Jan': [5, 3, 1, 3],
        'Feb': [8, 4, 2, 4],
        'Mar': [8, 5, 2, 5],
        'Apr': [9, 8, 3, 6]
})
data['Growth'] = data['Apr'] - data['Jan']


###add all data frames, convert date_date_excel do datetime, split df_fin into rub/usd
df_fin = pd.read_csv("D:\Python\WebApp\MLC_Finances_Eng_Final_UTF8.csv")
df_fin['Date'] = pd.to_datetime(df_fin['Date'], format='%d/%m/%Y', errors='coerce')

df_fin_usd = df_fin[df_fin['Classification'].str.contains('USD')]
df_fin_rub = df_fin[~df_fin['Classification'].str.contains('USD')]

df_att = pd.read_csv("D:\Python\WebApp\MLC_Attendance_Eng_FInal_UTF8.csv")

df_att['Date_Date_Excel'] = pd.to_datetime(df_att['Date_Date_Excel'], format='%A, %B %d, %Y')


##############Variable Bank##################
###Attendance###
# Total count of events
total_events = df_att.shape[0]

# Count of events by Creator
events_by_creator = df_att['Creator'].value_counts()

# Count of different Status (Cancelled and Completed count)
status_counts = df_att['Status'].value_counts()

# Percent completed from all events
completed_percent = (status_counts['Completed'] / total_events) * 100

# Count of different Type (Team Practice, etc)
type_counts = df_att['Type'].value_counts()

# Count of different elements in the Name column
name_counts = df_att['Name'].value_counts()

# Count of events by Location
location_counts = df_att['Location'].value_counts()


#############################################



def main():
    # Custom CSS styles #ff0000, #f9f9f9
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
        st.markdown("<h1 style='text-center: left; white-space: nowrap;'>MLC Financial and Attendance Data Analysis</h1>", unsafe_allow_html=True)
        show_general_stats()
    elif section == "Financial Data":
        show_financial_analysis()
    elif section == "Attendance Data":
        show_attendance_data()
    else:
        show_conclusions()

def show_general_stats():
    st.write('<h2 style="text-align: center;">General Statistics</h2>', unsafe_allow_html=True)
    

    # Add your general statistics code and visualizations here
    status_counts = df_att['Status'].value_counts()

    # Display a title
    st.write('<h1 style="text-align: center;">MLC Event Locations</h1>', unsafe_allow_html=True)

    # Define the HTML code to embed a Google Map
    html_code = """
    <div style="display: flex; justify-content: center;">
    <iframe src="https://www.google.com/maps/d/u/0/embed?mid=1gRGSSbVfXoknonZODAVIcfEdAeh0vac&ehbc=2E312F&noprof=1" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
    </div>
    """

    # Display the Google Map using the HTML code
    st.markdown(html_code, unsafe_allow_html=True)

    # Create two columns for side-by-side display
    col1, col2, col3 = st.columns(3)

    # Display status_counts in the first column
    with col1:
        st.markdown("<h2 style='font-size: 24px;'>Event Status</h2>", unsafe_allow_html=True)
        st.write(status_counts)

    # Display type_counts in the second column
    with col2:
        st.markdown("<h2 style='font-size: 24px;'>Event by Types</h2>", unsafe_allow_html=True)
        st.write(type_counts)

    # Display location_counts in the second column
    with col3:
        st.markdown("<h2 style='font-size: 24px;'>Event Locations</h2>", unsafe_allow_html=True)
        st.write(location_counts)



    st.write("text here text here text here text here")

    data['Growth'] = data['Apr'] - data['Jan']
    bar_width = 0.4  ## Set the bar width (you can adjust this value)
    fig, ax = plt.subplots(figsize=(3, 1))
    ax.bar(data['Source'], data['Growth'], width=bar_width)
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.set_xticks(range(len(data['Source'])))
    ax.set_xticklabels(data['Source'], rotation=45, ha='right')
    ##ax.set_xlabel('Source', fontsize=5)  --- x label (if needed)
    ax.set_ylabel('Growth in Gold Bars', fontsize= 5)
    ax.set_title('Growth in Gold Bars per Source', fontsize=7)

    st.write("text here text here text here text here")

    # Display the chart using Streamlit
    st.pyplot(fig)

    st.write("text here text here text here text here")

    st.pyplot(fig)

def show_financial_analysis():
    st.header("Financial Data")

    # Display the selected subsection content
    selected_subsection = st.sidebar.radio("Go to", ("Summary", "Income", "Expenses"))

    if selected_subsection == "Summary":
        # Add your summary analysis and visualizations here

        st.subheader("Summary Section Content")

        st.write("text here text here text here text here")

        data['Growth'] = data['Apr'] - data['Jan']

        # Create a bar chart using st.bar_chart (use st.altair_chart if the app doesnt guess the chart correctly)
        st.bar_chart(data, x="Source", y="Growth",  width=0, height=0, use_container_width=True)
        
        
        st.write("Growth in Gold Bars per Source:")
        st.write("text here text here text here text here")
        st.dataframe(data[['Source', 'Growth']])

        
        


    elif selected_subsection == "Income":
        # Add your income analysis and visualizations here
        st.subheader("Income Section Content")

        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(data['Source'], data['Growth'])
        ax.set_xlabel('Source', fontsize=12)
        ax.set_ylabel('Growth in Gold Bars', fontsize=12)
        ax.set_title('Growth in Gold Bars per Source', fontsize=16)
        
        # Add a slider widget to interact with the chart
        slider_value = st.slider("Adjust Data", min_value=0, max_value=5, value=1)
        for bar in bars:
            bar.set_height(bar.get_height() + slider_value)  # Adjust the bar heights

        # Display the chart using Streamlit
        st.pyplot(fig)

        st.write("text here text here text here text here")


    elif selected_subsection == "Expenses":
        # Add your expenses analysis and visualizations here
        st.subheader("Expenses Section Content")
        st.bar_chart(data, x="Source", y="Growth",  width=0, height=0, use_container_width=True)
        
        
        st.write("Growth in Gold Bars per Source:")
        st.dataframe(data[['Source', 'Growth']])

        st.write("text here text here text here text here")

        selected_source = st.selectbox("Select a Source", data['Source'])

        # Filter the data for the selected Source
        filtered_data = data[data['Source'] == selected_source].drop('Source', axis=1)

        # Plot a bar chart for the selected Source
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(filtered_data.columns, filtered_data.values.tolist()[0])
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.set_title(f'{selected_source} Data', fontsize=16)

        # Display the chart using Streamlit
        st.pyplot(fig)


def show_attendance_data():
    st.header("Attendance Data")
    # Add your attendance data analysis code and visualizations here
    st.write("text here text here text here text here")

    st.bar_chart(data, x="Source", y="Growth",  width=0, height=0, use_container_width=True)
        
        
    st.write("Growth in Gold Bars per Source:")
    st.dataframe(data[['Source', 'Growth']])

def show_conclusions():
    st.header("Conclusions")
    # Add your conclusions and summary text here
    st.write("text here text here text here text here")

    # Using h1 tag for larger text
    st.markdown("<h1 style='font-size: 36px;'>This is a larger text</h1>", unsafe_allow_html=True)

    # Using h2 tag for moderately large text
    st.markdown("<h2 style='font-size: 24px;'>This is a moderately large text</h2>", unsafe_allow_html=True)

    # Using plain text for default text size
    st.write("This is the default text size")

    # Using custom CSS style
    st.markdown("<p style='font-size: 18px;'>This is a custom font size</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

