import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from geopy.geocoders import Nominatim
import folium
from folium import plugins


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
# Filter for Team Practice events
team_practice_df = df_att[df_att['Type'] == 'Team Practice']

# Calculate average attendance per Team Practice event per year
average_attendance_team_practice_per_year = team_practice_df.groupby('Year')['Attendance'].mean()

# Filter for Skills Practice events
skills_practice_df = df_att[df_att['Type'] == 'Skills Practice']

# Calculate average attendance per Skills Practice event per year
average_attendance_skills_practice_per_year = skills_practice_df.groupby('Year')['Attendance'].mean()

# Filter for Intra-Squad Game events
intra_squad_game_df = df_att[df_att['Type'] == 'Intra-Squad Game']

# Calculate average attendance per Intra-Squad Game event per year
average_attendance_intra_squad_game_per_year = intra_squad_game_df.groupby('Year')['Attendance'].mean()

# Filter for Championship events
championship_df = df_att[df_att['Type'] == 'Championship']

# Calculate average attendance per Championship event per year
average_attendance_championship_per_year = championship_df.groupby('Year')['Attendance'].mean()

# Filter for Tournament events
tournament_df = df_att[df_att['Type'] == 'Tournament']

# Calculate average attendance per Tournament event per year
average_attendance_tournament_per_year = tournament_df.groupby('Year')['Attendance'].mean()


############calculations for events per year

############BELOW calculations dont account for less than 52 available weeks in 2013 and 2022########
#events_per_year = df_att['Year'].value_counts().sort_index()
#events_per_year = events_per_year.reset_index()
#events_per_year.columns = ['Year', 'Total Events']
#events_per_year['Events per Week'] = events_per_year['Total Events'] / 52

# Assuming 'Date_Date_Excel' is in datetime format
#df_att['Year'] = df_att['Date_Date_Excel'].dt.year
############ABOVE calculations dont account for less than 52 available weeks in 2013 and 2022########


# Calculate events per week and add it as a new column
events_per_year = df_att['Year'].value_counts().sort_index().reset_index()
events_per_year.columns = ['Year', 'Total Events']
events_per_year['Events per Week'] = events_per_year.apply(lambda row: row['Total Events'] / 8 if row['Year'] == 2013 else (row['Total Events'] / 11 if row['Year'] == 2022 else row['Total Events'] / 52), axis=1)

average_events_per_year = events_per_year.mean()
events_per_week = average_events_per_year / 52

###################################
all_durations = df_att['Duration']
# Sample duration values from all rows
durations = all_durations
# Define a function to convert a duration string to minutes
def convert_duration_to_minutes(duration_str):
    parts = duration_str.split()
    minutes = 0

    for i in range(len(parts)):
        if parts[i] == 'days':
            minutes += int(parts[i - 1]) * 24 * 60
        elif parts[i] == 'hr':
            minutes += int(parts[i - 1]) * 60
        elif parts[i] == 'min':
            minutes += int(parts[i - 1])

    return minutes

# Convert the duration strings to minutes and sum them
total_minutes = sum([convert_duration_to_minutes(duration) for duration in durations])

# Convert the total minutes back to hours and minutes
total_hours = total_minutes // 60
remaining_minutes = total_minutes % 60




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
        #st.markdown("<h1 style='text-center: left; white-space: nowrap;'>MLC Financial and Attendance Data Analysis</h1>", unsafe_allow_html=True)
        show_general_stats()
    elif section == "Financial Data":
        show_financial_analysis()
    elif section == "Attendance Data":
        show_attendance_data() 
    else:
        show_conclusions()

def show_general_stats():
    st.write('<h1 style="text-align: center;">General Statistics</h1>', unsafe_allow_html=True)
    

    # Add your general statistics code and visualizations here
    status_counts = df_att['Status'].value_counts()
    unique_location_count = df_att['Location'].nunique()  # Count of unique locations
   
   
    # Add CSS for styling the dashboard
    st.markdown(
        """
        <style>
            .dashboard-column {
                text-align: center;
                background-color: lightblue;
                border-radius: 10px;
                padding: 15px;
            }
        
            .larger-text {
                font-size: 26px; /* Adjust the font size here */
            }
        </style>
        """,
        unsafe_allow_html=True
    )




    bg_color = 'lightblue'
    
    # Add CSS for rounded corners
    st.markdown(
        """
        <style>
        .dashboard-column {
            border-radius: 10px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # Create the layout for the dashboard
    col1, col2, col3, col4 = st.columns(4)

    # First row
    with col1:
        # Display unique location counts
        st.markdown(
            f"<div class='dashboard-column'>Unique Locations<br><span class='larger-text'>{unique_location_count}</span></div>",
            unsafe_allow_html=True
        )

    with col2:
        # Display average events per week cumulative
        st.markdown(
            f"<div class='dashboard-column'>Avg Events/Year<br><span class='larger-text'>{average_events_per_year['Total Events']:.2f}</span></div>",
            unsafe_allow_html=True
        )

    with col3:
        # Display average events per year cumulative
        st.markdown(
            f"<div class='dashboard-column'>Avg Events/Week<br><span class='larger-text'>{average_events_per_year['Events per Week']:.2f}</span></div>",
            unsafe_allow_html=True
        )

    with col4:
        # Display total hours (total_duration)
        st.markdown(
            f"<div class='dashboard-column'>Total Event Hours<br><span class='larger-text'>{total_hours}</span></div>",
            unsafe_allow_html=True
        )



    

    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)


   
    bg_color = 'lightblue'

    # Create the layout for the dashboard
    col5, col6, col7 = st.columns(3)

    # Second row
    with col5:
        # Display the number of completed events
        st.markdown(
            f"<div class='dashboard-column' style='text-align: center; background-color: {bg_color};'>Completed Events<br><span class='larger-text'>{status_counts.get('Completed', 0)}</span></div>",
            unsafe_allow_html=True
        )

    with col6:
        # Display the number of cancelled events
        st.markdown(
            f"<div class='dashboard-column' style='text-align: center; background-color: {bg_color};'>Cancelled Events<br><span class='larger-text'>{status_counts.get('Cancelled', 0)}</span></div>",
            unsafe_allow_html=True
        )

    with col7:
        # Display the percentage of completed events
        completed_percent = (status_counts.get('Completed', 0) / len(df_att)) * 100
        st.markdown(
            f"<div class='dashboard-column' style='text-align: center; background-color: {bg_color};'>Completed Percentage<br><span class='larger-text'>{completed_percent:.2f}%</span></div>",
            unsafe_allow_html=True
        )


 
    
    ###################################################################################
 
    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)

    #############################################################

    

    # Display a title
    st.write('<h2 style="text-align: center;">MLC Event Locations</h2>', unsafe_allow_html=True)

    html_code = """
    <div style="display: flex; justify-content: center;">
        <iframe src="https://www.google.com/maps/d/u/0/embed?mid=1gRGSSbVfXoknonZODAVIcfEdAeh0vac&ehbc=2E312F&noprof=1" 
            style="width: 100%; height: 500px; border: 0;" 
            allowfullscreen="" loading="lazy">
        </iframe>
    </div>
    """




    # Display the Google Map using the HTML code
    st.markdown(html_code, unsafe_allow_html=True)

    ##################################################################

    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)


    ######################################################################

    # Calculate percentages
    percentages = type_counts / type_counts.sum()

    # Find types with less than 1% and group them
    threshold = 0.01
    types_to_group = percentages[percentages < threshold].index

    # Create a new DataFrame with aggregated values
    type_counts_grouped = type_counts.copy()
    other_events_count = type_counts[types_to_group].sum()
    type_counts_grouped = type_counts_grouped[percentages >= threshold]
    type_counts_grouped['Other Events'] = other_events_count

    

    # Set a blue color palette
    # Define a color palette based on the number of unique event types
    num_types = len(type_counts_grouped)
    colors = plt.cm.tab20c(range(num_types))

    # Plot the pie chart with the specified color palette
    st.markdown("<h2 style='font-size: 24px; text-align: center;'>Event by Types</h2>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the size here (width, height)
    pie = type_counts_grouped.plot(kind='pie', startangle=140, labels=['']*len(type_counts_grouped), ax=ax, colors=colors)
    plt.title('Event Distribution by Types')
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # Get percentages for legend labels
    percentages_grouped = ['{:1.0f}%'.format(val * 100) for val in type_counts_grouped / type_counts_grouped.sum()]
    legend_labels_grouped = [f'{type_counts_grouped.index[i]}: {percentages_grouped[i]}' for i in range(len(type_counts_grouped))]

    # Create a legend with percentages multiplied by 100
    plt.legend(legend_labels_grouped, loc='center right', bbox_to_anchor=(1.2, 0.5), title="Event Types")
    plt.ylabel('')  # Remove the y-label
    st.pyplot(fig)


    ############################
   



    ###################################################################################
 
    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)

    #############################################################


    ##########################  HEATMAP  ###########################
    ################################################################

    st.markdown("<h2 style='font-size: 24px; text-align: center;'>Event Addresses</h2>", unsafe_allow_html=True)
        
    # Filter out rows with missing latitude or longitude
    
    filtered_df = df_att.loc[(df_att['Status'] == 'Completed') & df_att['lat'].notna() & df_att['lon'].notna()]

    # Create a scatter mapbox plot
    #fig = px.scatter_mapbox(filtered_df, lat='lat', lon='lon', zoom=10)

    # Set map layout and display the map
    #fig.update_layout(mapbox_style="open-street-map")
    #fig.update_layout(
        #title='Geographic Scatter Map of Moscow',
        #margin=dict(l=0, r=0, t=30, b=0)
    #)
    #st.plotly_chart(fig)
        
    # Create a Folium map centered around Moscow
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)  # Coordinates for Moscow

    # Add a HeatMap layer to the map using the latitudes and longitudes from filtered_df
    heat_data = filtered_df[['lat', 'lon']].values.tolist()
    folium.plugins.HeatMap(heat_data).add_to(m)

    # Convert the Folium map to HTML
    html_map = m._repr_html_()
  

    # Display the map in Streamlit
    st.markdown("<h2 style='font-size: 24px; text-align: center;'>Geographic Heatmap of Moscow</h2>", unsafe_allow_html=True)
    components.html(html_map, height=500)
    

    #############################################################################
 



        
        
      

########################################################
    ##Total Events/Avg Events per week chart
    # Set title
    
    st.write('<h2 style="text-align: center;">Total Events and Avg. Events per Week per Year</h2>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>2013 has 8 weeks of data, 2022 has 11 weeks of data</p>", unsafe_allow_html=True)



    # Create a Plotly figure with subplots
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    # Add bar chart with labels
    fig.add_trace(go.Bar(
        x=events_per_year['Year'],
        y=events_per_year['Total Events'],
        name='Total Events',
        text=events_per_year['Total Events'],  
        textposition='inside',
        insidetextanchor='end',  # Adjust text anchor as needed
        textfont=dict(size=16, color='black'),
        marker=dict(color='lightblue')  # Set the bar color here
    ), secondary_y=False)


    # Round the 'Events per Week' values to the tenths
    rounded_values = events_per_year['Events per Week'].round(1)

    # Add line chart with labels
    fig.add_trace(go.Scatter(
        x=events_per_year['Year'],
        y=events_per_year['Events per Week'],
        mode='lines+markers+text',
        name='Events per Week',
        text=rounded_values,
        textposition='top center',
        marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
        textfont=dict(size=16, color='red'),
    ), secondary_y=True)

    #Set layout
    fig.update_layout(
        xaxis=dict(title='Year'),
        yaxis=dict(title='Total Events', showgrid=False, range=[0, 200]),
        yaxis2=dict(title='Events per Week', overlaying='y', side='right', showgrid=False, range=[0, 3.5]),
        legend=dict(x=0.5, y=.99, traceorder='normal', orientation='h'),
    )


    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<p style='text-align: center;'>Practices were conducted from 2010 but were recorded only starting at the end of 2013 at which the rate of practice was 2.1 per week. </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Same with the beginning of 2022, at that time, for those first weeks of 2022 the rate of practice was 1.2. </p>", unsafe_allow_html=True)
    




#########################################

###Team practices should go before skill practices

    st.write('<h2 style="text-align: center;">Total Team Practices and Avg. Team Practices per Week per Year</h2>', unsafe_allow_html=True)
    
    team_practice_data = df_att[df_att['Type'] == 'Team Practice']
    team_practice_counts = team_practice_data.groupby('Year').size()
    df_att['Date_Date_Excel'] = pd.to_datetime(df_att['Date_Date_Excel'], format='%A, %B %d, %Y')
    team_practice_data['Week_Number'] = team_practice_data['Date_Date_Excel'].dt.strftime('%U')

    average_weekly_counts = team_practice_data.groupby(['Year', 'Week_Number']).size().groupby('Year').mean()

    fig3 = make_subplots(specs=[[{'secondary_y': True}]])

    fig3.add_trace(go.Bar(
        x=team_practice_counts.index,
        y=team_practice_counts.values,
        name='Total Team Practice Counts',
        text=team_practice_counts.values,
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(size=16, color='black'),
        marker=dict(color='lightblue')
    ), secondary_y=False)

    fig3.add_trace(go.Scatter(
        x=average_weekly_counts.index,
        y=average_weekly_counts.values,
        mode='lines+markers+text',
        name='Avg Weekly Events',
        text=average_weekly_counts.values.round(1),
        textposition='top center',
        marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
        textfont=dict(size=16, color='red')
    ), secondary_y=True)

    fig3.update_layout(
        xaxis=dict(title='Year'),
        yaxis=dict(title='Total Team Practice Counts', showgrid=False, range=[0,150]),
        yaxis2=dict(title='Avg Weekly Team Practice Counts', overlaying='y', side='right', showgrid=False, range=[0, 2.9]),
        legend=dict(x=.3, y=1, traceorder='normal', orientation='h')
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<p style='text-align: center;'>conclusion text here</p>", unsafe_allow_html=True)













#########################################

    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)
     ##filler for spacing
   

############################################

    st.write('<h2 style="text-align: center;">Total Skills Practices and Avg. Skills Practices per Week per Year</h2>', unsafe_allow_html=True)
    

    # Assuming df_att is your DataFrame containing the data
    skills_practice_data = df_att[df_att['Type'] == 'Skills Practice']
    skills_practice_counts = skills_practice_data.groupby('Year').size()
    df_att['Date_Date_Excel'] = pd.to_datetime(df_att['Date_Date_Excel'], format='%A, %B %d, %Y')
    skills_practice_data['Week_Number'] = skills_practice_data['Date_Date_Excel'].dt.strftime('%U')

    average_weekly_counts_skills = skills_practice_data.groupby(['Year', 'Week_Number']).size().groupby('Year').mean()

    fig2 = make_subplots(specs=[[{'secondary_y': True}]])

    fig2.add_trace(go.Bar(
        x=skills_practice_counts.index,
        y=skills_practice_counts.values,
        name="Total Skills Practices",
        text=skills_practice_counts.values, 
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(size=16, color='black'),
        marker=dict(color='lightblue')
    ), secondary_y=False)

    
    # Add line chart with labels
    fig2.add_trace(go.Scatter(
        x=average_weekly_counts_skills.index,
        y=average_weekly_counts_skills.values,
        mode='lines+markers+text',
        name='Avg Weekly Events',
        text=average_weekly_counts_skills.values.round(1), 
        textposition='top center',
        marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
        textfont=dict(size=16, color='red'),
    ), secondary_y=True)

    #Set layout
    fig2.update_layout(
        xaxis=dict(title='Year'),
        yaxis=dict(title='Total Events', showgrid=False, range=[0, 100]),
        yaxis2=dict(title='Events per Week', overlaying='y', side='right', showgrid=False, range=[0, 4]),
        legend=dict(x=0, y=1, traceorder='normal', orientation='h'),
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<p style='text-align: center;'>conclusion text here</p>", unsafe_allow_html=True)



#####################################################################










































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
        
    # Display the selected subsection content
    selected_subsection = st.sidebar.radio("Go to", ("Summary", "Player Stats"))
    st.write('<h1 style="text-align: center;">Team/Skill Practice Attendance</h1>', unsafe_allow_html=True)
        



    if selected_subsection == "Summary":
                
        st.write('<h2 style="text-align: center;">Attendance Data</h2>', unsafe_allow_html=True)

        # Add CSS for styling the dashboard
        st.markdown(
            """
            <style>
                .dashboard-column {
                    text-align: center;
                    background-color: lightblue;
                    border-radius: 10px;
                    padding: 15px;
                }
        
                .larger-text {
                    font-size: 26px; /* Adjust the font size here */
                }
            </style>
            """,
            unsafe_allow_html=True
        )


        bg_color = 'lightblue'
    
        # Add CSS for rounded corners
        st.markdown(
            """
            <style>
            .dashboard-column {
                border-radius: 10px;
                padding: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


        # Create the layout for the dashboard
        col1, col2, col3 = st.columns(3)


        
        average_attendance_per_event = round(df_att[df_att['Status'] == 'Completed']['Attendance'].mean(), 1)
        total_attendees_completed_events = df_att[df_att['Status'] == 'Completed']['Attendance'].sum()
        

        all_attendees = df_att['Going'].str.split(', ').explode()
        filtered_attendees = [attendee for attendee in all_attendees if attendee != "No Data" and len(attendee.split()) == 2]
        unique_attendees = list(set(filtered_attendees))
        unique_attendees_count = len(unique_attendees)


        # First row
        with col1:
            # Display unique location counts
            st.markdown(
                f"<div class='dashboard-column'>Total Attendees<br><span class='larger-text'>{total_attendees_completed_events}</span></div>",
                unsafe_allow_html=True
            )

        with col2:
            # Display average events per week cumulative
            st.markdown(
                f"<div class='dashboard-column'>Avg Att. per Event<br><span class='larger-text'>{average_attendance_per_event}</span></div>",
                unsafe_allow_html=True
            )

        with col3:
            # Display average events per year cumulative
            st.markdown(
                f"<div class='dashboard-column'>Unique Attendees<br><span class='larger-text'>{unique_attendees_count}</span></div>",
                unsafe_allow_html=True
            )


        # Filter DataFrame for 'Completed' events
        completed_events = df_att[df_att['Status'] == 'Completed']

        # Calculate average attendance per event per year
        avg_attendance_per_event_per_year = completed_events.groupby('Year')['Attendance'].mean()


        # Group by year and sum the attendees
        total_attendees_per_year = completed_events.groupby('Year')['Attendance'].sum()

        # Create a Plotly figure with subplots
        fig = make_subplots(specs=[[{'secondary_y': True}]])

        # Add bar chart for total attendees per year
        fig.add_trace(go.Bar(
            x=total_attendees_per_year.index,
            y=total_attendees_per_year.values,
            name='Total Attendees',
            marker=dict(color='lightblue'),  # Set the bar color here
            text=total_attendees_per_year.values,
            textposition='inside',
            textfont=dict(size=16, color='black'),
        ), secondary_y=False)

        # Round average values to tenths
        rounded_avg_values = avg_attendance_per_event_per_year.round(1)

        # Add line chart for average attendance per event per year
        fig.add_trace(go.Scatter(
            x=avg_attendance_per_event_per_year.index,
            y=avg_attendance_per_event_per_year.values,
            mode='lines+markers+text',
            name='Avg Attendance per Event',
            marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
            text=rounded_avg_values,
            textposition='top center',
            textfont=dict(size=16, color='red'),
        ), secondary_y=True)


        # Set layout
        fig.update_layout(
            xaxis=dict(title='Year'),
            yaxis=dict(title='Total Attendees', showgrid=False, range=[0, 1300]),
            yaxis2=dict(title='Avg. Attendance per Week', showgrid=False, range=[5, 11]),
            legend=dict(x=.3, y=1, traceorder='normal', orientation='h'),
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)


        # Create the figure
        fig = go.Figure()

        # Add bar graph for Team Practice events
        fig.add_trace(go.Bar(
            x=average_attendance_team_practice_per_year.index,
            y=average_attendance_team_practice_per_year.values,
            name='Team Practice - Average Attendance',
            marker=dict(color='lightblue'),  # Change the bar color here
        ))

        # Add line graph for Team Practice events
        fig.add_trace(go.Scatter(
            x=average_attendance_team_practice_per_year.index,
            y=average_attendance_team_practice_per_year.values,
            mode='lines+markers',
            name='Team Practice - Average Attendance',
            line=dict(color='green'),  # Change the line color here
        ))

        # Update layout
        fig.update_layout(
            title='Average Attendance for Team Practice Events per Year',
            xaxis_title='Year',
            yaxis_title='Average Attendance',
            barmode='group',
        )

        # Show the plot
        st.plotly_chart(fig)




        # Add your attendance data analysis code and visualizations here
        st.write("text here text here text here text here")

        st.bar_chart(data, x="Source", y="Growth",  width=0, height=0, use_container_width=True)
        
        
        st.write("Growth in Gold Bars per Source:")
        st.dataframe(data[['Source', 'Growth']])



    elif selected_subsection == "Player Stats": 
        st.write('<h2 style="text-align: center;">Individual Stats</h2>', unsafe_allow_html=True)



        st.write("text here text here text here text here")









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

