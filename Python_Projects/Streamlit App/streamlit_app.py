import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from geopy.geocoders import Nominatim
import folium
from folium import plugins
from dateutil import parser





st.set_page_config(layout='wide')

############## Data Bank ####################



###add all data frames, convert date_date_excel do datetime, split df_fin into rub/usd
df_fin = pd.read_csv("D:\Python\WebApp\MLC_Finances_Eng_Final_UTF8.csv")
df_fin['Date'] = pd.to_datetime(df_fin['Date'], format='%d/%m/%Y', errors='coerce')

df_fin_usd = df_fin[df_fin['Classification'].str.contains('USD')]
df_fin_rub = df_fin[~df_fin['Classification'].str.contains('USD')]



df_att = pd.read_csv("D:\Python\WebApp\MLC_Attendance_Eng_FInal_UTF8.csv")

df_forex = pd.read_csv("USD_RUB.csv")


df_forex['Date'] = pd.to_datetime(df_forex['Date'])
df_forex.dropna(subset=['Date', 'Price'], inplace=True)

# Parse the date string using dateutil.parser
df_att['Date_Date_Excel'] = df_att['Date_Date_Excel'].apply(lambda x: parser.parse(x))


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
                background-color: skyblue;
                border-radius: 10px;
                padding: 15px;
                font-weight: bold;
            }
        
            .larger-text {
                font-size: 26px; /* Adjust the font size here */
            }
        </style>
        """,
        unsafe_allow_html=True
    )




    bg_color = 'skyblue'
    
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


   
    bg_color = 'skyblue'

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

    st.markdown("<p style='text-align: center;'>Practices were conducted from 2010 to 2022, but were recorded only starting at the end of 2013. </p>", unsafe_allow_html=True)
    
    
      

    
    
    
  

    html_code = """
    <div style="display: flex; justify-content: center;">
        <iframe src="https://www.google.com/maps/d/u/0/embed?mid=1gRGSSbVfXoknonZODAVIcfEdAeh0vac&ehbc=2E312F&noprof=1" 
            style="width: 100%; height: 500px; border: 0;" 
            allowfullscreen="" loading="lazy">
        </iframe>
    </div>
    """

 

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




    ###################################################################################
 
    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)

    #############################################################


    ##########################  HEATMAP  ###########################
    ################################################################

            
    # Filter out rows with missing latitude or longitude
    
    filtered_df = df_att.loc[(df_att['Status'] == 'Completed') & df_att['lat'].notna() & df_att['lon'].notna()]
        
    # Create a Folium map centered around Moscow
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)  # Coordinates for Moscow

    # Add a HeatMap layer to the map using the latitudes and longitudes from filtered_df
    heat_data = filtered_df[['lat', 'lon']].values.tolist()
    folium.plugins.HeatMap(heat_data).add_to(m)

    # Convert the Folium map to HTML
    html_map = m._repr_html_()
     

    #############################################################################
    ###########################################







    ###################################################################################
 
    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)

    #############################################################




    tab1, tab2 = st.tabs(["MLC Event Locations", "MLC Heatmap"])

    

    with tab1:
        st.write('<h2 style="text-align: center;">MLC Event Locations</h2>', unsafe_allow_html=True)


        html_code = """
        <div style="display: flex; justify-content: center;">
            <iframe src="https://www.google.com/maps/d/u/0/embed?mid=1gRGSSbVfXoknonZODAVIcfEdAeh0vac&ehbc=2E312F&noprof=1" 
                style="width: 100%; height: 500px; border: 0;" 
                allowfullscreen="" loading="lazy">
            </iframe>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)

    with tab2:
        st.write('<h2 style="text-align: center;">MLC Heatmap</h2>', unsafe_allow_html=True)

        
        components.html(html_map, height=500)



    ###################################################################################
 
    ##filler for spacing
    st.markdown("<br><br>", unsafe_allow_html=True)

    #############################################################



###############  pie chart ################ 
###########################################



    container = st.container(border=True)  
    with container:
        # Plot the pie chart with the specified color palette
    
    


        fig, ax = plt.subplots(figsize=(10, 6))  # Set the size here (width, height)
        pie = type_counts_grouped.plot(kind='pie', startangle=140, labels=[None]*len(type_counts_grouped), ax=ax, colors=colors)
        plt.title('Event Distribution by Types')
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

        # Get percentages for legend labels
        percentages_grouped = ['{:1.0f}%'.format(val * 100) for val in type_counts_grouped / type_counts_grouped.sum()]
        # Create legend labels with counts and percentages
        legend_labels_grouped = [f'{type_counts_grouped.index[i]}: {type_counts_grouped.iloc[i]} ({percentages_grouped[i]})' for i in range(len(type_counts_grouped))]

        # Create a legend with percentages multiplied by 100
        plt.legend(legend_labels_grouped, loc='center right', bbox_to_anchor=(1.2, 0.5), title="Event Types")
        plt.ylabel('')  # Remove the y-label
        st.pyplot(fig)



    ############################
   
 

                   
      

########################################################
       

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
        marker=dict(color='skyblue')  # Set the bar color here
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



#########################################

###Team practices should go before skill practices
    
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
        marker=dict(color='skyblue')
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





#########################################

    ##filler for spacing
    st.markdown("<br>", unsafe_allow_html=True)
     ##filler for spacing
   

############################################

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
        marker=dict(color='skyblue')
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
        legend=dict(x=0.3, y=1, traceorder='normal', orientation='h'),
    )
  

###################################################################



    ##filler for spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    ## double space



#####################################################################

  

#####################################################################
    container = st.container(border=True)  
    with container:

        st.markdown("<h2 style='font-size: 24px; text-align: center;'>Event Frequency Charts</h2>", unsafe_allow_html=True)


        with st.expander('Total Team Practices and Avg. Team Practices per Week per Year'):
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("<p style='text-align: center;'>Practices were conducted from 2010 but were recorded only starting at the end of 2013. 2013 has 8 weeks of data, 2022 has 11 weeks of data.</p>", unsafe_allow_html=True)
            

        with st.expander('Total Skills Practices and Avg. Skills Practices per Week per Year'):
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("<p style='text-align: center;'>Skills practices were started in 2015 by two people. One of them moved to a different part of the city after 2016, which decreased the amount of practices they had.</p>", unsafe_allow_html=True)

        with st.expander('Total Events and Avg. Events per Week per Year'):
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<p style='text-align: center;'>This is a sum of all events the Moscow Lacrosse Club conducted. There were 13 unique types of events that were facilitated by the club. </p>", unsafe_allow_html=True)


    






######################################################################

























def show_financial_analysis():
    st.write('<h1 style="text-align: center;">Financial Data</h1>', unsafe_allow_html=True)

    

    # Display the selected subsection content
    selected_subsection = st.sidebar.radio("Go to", ("Summary", "Income/Expenses", "Equipment Data"))

    if selected_subsection == "Summary":
        # Add your summary analysis and visualizations here








        st.write('<h2 style="text-align: center;">Team Fund (Total in USD)</h2>', unsafe_allow_html=True)


        # Add CSS for styling the dashboard
        st.markdown(
            """
            <style>
                .dashboard-column {
                    text-align: center;
                    background-color: skyblue;
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


        bg_color = 'skyblue'
    
        # Add CSS for rounded corners
        st.markdown(
            """
            <style>
            .dashboard-column {
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )




        
        
        

        all_attendees = df_att['Going'].str.split(', ').explode()
        filtered_attendees = [attendee for attendee in all_attendees if attendee != "No Data" and len(attendee.split()) <= 3]
        unique_attendees = list(set(filtered_attendees))
        unique_attendees_count = len(unique_attendees)

        df_fin_usd = df_fin[df_fin['Classification'].str.contains('USD')]
        df_fin_rub = df_fin[~df_fin['Classification'].str.contains('USD')]

        total_turnover_usd = df_fin_usd['Sum'].abs().sum()
        total_turnover_rub = df_fin_rub['Sum'].abs().sum()

        total_transactions_usd = df_fin_usd.shape[0]
        total_transactions_rub = df_fin_rub.shape[0]
        

        df_fin_rub = df_fin_rub.assign(**{'Fund Cumulative': df_fin_rub['Sum'].cumsum()})
        df_fin_usd = df_fin_usd.assign(**{'Fund Cumulative': df_fin_usd['Sum'].cumsum()})

        # Merge the DataFrames on the 'Date' column
        merged_df = pd.merge(df_fin_rub, df_forex, on='Date', how='inner')
        merged_df['Fund Cumulative in USD'] = merged_df['Fund Cumulative'] / merged_df['Price']

        # Create a line graph to visualize the cumulative sum over time
        fig_cumulative_sum_rub = px.line(df_fin_rub, x='Date', y='Fund Cumulative',
                                        title='Cumulative Sum Over Time (RUB)')
        
        fig_cumulative_sum_usd = px.line(df_fin_usd, x='Date', y='Fund Cumulative',
                                        title='Cumulative Sum Over Time (USD)')
        


        fig_forex = px.line(df_forex, x='Date', y='Price', title='USD to RUB Exchange Rate Over Time')

        
        fig_fund_forex = px.line(merged_df, x='Date', y='Fund Cumulative in USD', title='RUB Fund in USD by Exchange Rate of that Time')
        fig_fund_forex.update_xaxes(title='Date')
        fig_fund_forex.update_yaxes(title='Fund Cumulative in USD')

        combined_data = pd.read_csv("D:\Python\WebApp\combined_data.csv")
        combined_data['Date'] = pd.to_datetime(combined_data['Date'])

        # Calculate 'Total Fund USD' after filling NaN values
        combined_data['Total Fund USD'] = combined_data['Fund Cumulative'].add(combined_data['Fund Cumulative in USD'], fill_value=0)

        # Create a line plot using Plotly Express
        fig_combined = px.line(combined_data, x='Date', y='Total Fund USD', 
                            labels={'Date': 'Date', 'Total Fund USD': 'Amount in USD'},
                            title='Combined Funds in USD')
        

        container = st.container(border=True)  
        with container:
            st.plotly_chart(fig_combined, use_container_width=True)

        
            




        ################### Create the layout for the financial summary page
        col11, col22 = st.columns(2)

        container = st.container(border=True)

        
        # First row
        with col11:
            container = st.container(border=True)  
            with container:
                col1, col2 = st.columns(2)
                with col1:
                    

                    st.markdown(
                        f"<div class='dashboard-column'>Total Turnover RUB<br><span class='larger-text'>{total_turnover_rub}</span></div>",
                        unsafe_allow_html=True
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

            
                with col2:

                    st.markdown(
                    f"<div class='dashboard-column'>Total Transactions RUB<br><span class='larger-text'>{total_transactions_rub}</span></div>",
                    unsafe_allow_html=True
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                st.plotly_chart(fig_cumulative_sum_rub, use_container_width=True)
            

                    
            
        with col22:
            container = st.container(border=True)  
            with container:
                col1, col2 = st.columns(2)
                with col1:
                        
                    st.markdown(
                        f"<div class='dashboard-column'>Total Turnover USD<br><span class='larger-text'>{total_turnover_usd}</span></div>",
                        unsafe_allow_html=True
                    )

                    st.markdown("<br>", unsafe_allow_html=True)
                
                with col2:

                    st.markdown(
                        f"<div class='dashboard-column'>Total Transactions USD<br><span class='larger-text'>{total_transactions_usd}</span></div>",
                        unsafe_allow_html=True
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                st.plotly_chart(fig_cumulative_sum_usd, use_container_width=True) 
                    
     
   


        col111, col222 = st.columns(2)

       
        
        with col111:
            with st.expander('Exchange Rate from Aug 2015 - April 2022'):
                st.plotly_chart(fig_forex, use_container_width=True)
            with st.expander('RUB fund denominated in US Dollars'):
                st.plotly_chart(fig_fund_forex, use_container_width=True)
            transaction_count = df_fin.groupby('Date').size().reset_index(name='Transaction Volume')

            # Create a line plot using Plotly Express
            with st.expander('Volume of Transactions'):
                fig_transactions = px.line(transaction_count, x='Date', y='Transaction Volume', 
                                            labels={'Date': 'Date', 'Transaction Volume': 'Transaction Volume'},
                                            title='Transaction Volume Over Time')

                # Show the graph for transaction volume
                st.plotly_chart(fig_transactions, use_container_width=True)


        
        with col222:
            container = st.container(border=True)
            with container:
                       
                    
                st.write('''Due to fluctuations and subsequent devaluation of the Ruble over time, 
                        the club decided to open a second fund in 2018 that would hold foreign currency. 
                        This would protect against the Ruble's inflation and devaluation, 
                        facilitate payments for events and federation memberships abroad, 
                        as well as equipment purchases.                        
                        ''')
                    
                st.write('''Throughout the club's history the value of the Ruble dropped from 30 RUB for 1 USD to near 150 RUB for 1 USD.
                        The fund ledger started in 2015, and even then we had to deal with fluctuations of the rate betwwen 60-80 RUB for 1 USD for 
                        the majority of the time, with the exchange rate average rising (value decreasing) over time.
                        ''')
                    
                

       


       
        

   
       
       

    



       

        
        


    elif selected_subsection == "Income/Expenses":
        # Add your income/Expenses analysis and visualizations here
        st.write('<h2 style="text-align: center;">Income/Expenses Cashflow</h2>', unsafe_allow_html=True)

        df_fin_rub = df_fin[~df_fin['Classification'].str.contains('USD')]
        df_fin_usd = df_fin[df_fin['Classification'].str.contains('USD')]

        

        col1, col2 = st.columns(2)

        
        
        with col1:
            container = st.container(border=True)  
            with container: 
                source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
                target = [8, 8, 8, 8, 8, 8, 8, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

                # Values for the links
                value = [537468, 5800, 1447299, 1000, 1290, 33400, 15650, 147400, 12430, 33936, 410529, 1410810, 33400, 90659, 40850, 15000, 26151, 5000, 4900, 7742, 97900 ]

                # Creating the Sankey diagram
                fig_sankey = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color='black', width=0.5),
                        
                        label=['Equipment', 'Event', 'Field', 'Fine', 'Interest Payment', 'Internal Transfer',
                        'Loan', 'Membership Fee', 'Total Income', 'Accounting Services', 'Digital Services', 'Equipment', 'Field', 'Internal Transfer',
                        'International Membership Fee', 'Legal Services', 'Loan', 'Logistical Debits',
                        'Logistical Fees', 'Marketing', 'Misc', 'Payout' ],

                        color=[
                        'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightblue',
                        'indianred', 'indianred', 'indianred', 'indianred', 'indianred', 'indianred', 'indianred', 'indianred',
                        'indianred', 'indianred', 'indianred', 'indianred', 'indianred'
                        ]  

                    ),
                    
                    link=dict(
                        source=source,
                        target=target,
                        value=value,
                        color='rgba(0, 0, 0, .05)'  # Example: semi-transparent black lines
                    )
                )])

                # Updating layout properties
                fig_sankey.update_layout(title_text="RUB Fund Cash Flow")

                # Show the Sankey diagram
                st.plotly_chart(fig_sankey, use_container_width=True)

                st.markdown('''
                    <h2 style='text-align: center; font-size: 12px;'>
                        *Equipment in the RUB fund is all player and non-player equipment. From heads, shafts, gloves to goals, nets, cones, etc.
                    </h2>
                ''', unsafe_allow_html=True)

         


            # Filter rows without "(Liquidation)" in the Commentary column
            df_filtered_rub = df_fin_rub[~df_fin_rub['Commentary'].str.contains('(Liquidation)', na=False)]

            # Extract the year from the 'Date' column  
            df_filtered_rub['Year'] = df_filtered_rub['Date'].dt.year

            # Calculate the sum of profits and losses for each year
            profits = df_filtered_rub[df_filtered_rub['Sum'] > 0].groupby('Year')['Sum'].sum()
            losses = df_filtered_rub[df_filtered_rub['Sum'] < 0].groupby('Year')['Sum'].sum()

            # Calculate the net profit or loss for each year
            net_profit_loss = profits.add(losses, fill_value=0)

            # Convert 'Year' to strings
            net_profit_loss.index = net_profit_loss.index.astype(str)

            # Create a bar graph
            fig_net_rub = px.bar(x=net_profit_loss.index, y=net_profit_loss.values, title='Net Profit/Loss by Year RUB Fund')
            fig_net_rub.update_traces(marker_color='green', selector=dict(type='bar', marker_line_color='green'))
            fig_net_rub.update_xaxes(title_text='Year')
            fig_net_rub.update_yaxes(title_text='Net Profit/Loss')

            

            category_summary_rub = df_fin_rub.groupby('Category').agg({'Sum': ['sum', 'count']})
            category_summary_rub.columns = ['Total Sum', 'Number of Transactions']
            category_summary_rub = category_summary_rub.reset_index()

            category_summary_rub['Profit/Loss per Transaction'] = category_summary_rub['Total Sum'] / category_summary_rub['Number of Transactions']

            # Sort the DataFrame by 'Total Sum' in descending order and select the top 5 rows
            top_5_total_sum_rub = category_summary_rub.sort_values(by='Total Sum', ascending=False).head(5)

            # Create a horizontal bar graph for 'Total Sum'
            fig_total_sum_rub = px.bar(top_5_total_sum_rub, x='Category', y='Total Sum',
                                title='Top 5 Categories by Total Profit (RUB)')

            # Create a horizontal bar graph for 'Number of Transactions'
            top_10_transactions_rub = category_summary_rub.sort_values(by='Number of Transactions', ascending=False).head(5)
            fig_transactions_rub = px.bar(top_10_transactions_rub, x='Category', y='Number of Transactions',
                                    title='Top 5 Categories by Number of Transactions (RUB)')

            # Create a horizontal bar graph for 'Profit/Loss per Transaction'
            top_10_profit_loss_rub = category_summary_rub.sort_values(by='Profit/Loss per Transaction', ascending=False).head(5)
            fig_profit_loss_rub = px.bar(top_10_profit_loss_rub, x='Category', y='Profit/Loss per Transaction',
                                    title='Top 5 Categories by Profit per Transaction (RUB)')
            
            # Extract the month from the 'Date' column
            df_fin_rub['Month'] = df_fin_rub['Date'].dt.strftime('%B')

            # Calculate the sum of profits and losses for each month
            profits = df_fin_rub[df_fin_rub['Sum'] > 0].groupby('Month')['Sum'].sum().reset_index()
            losses = df_fin_rub[df_fin_rub['Sum'] < 0].groupby('Month')['Sum'].sum().reset_index()

            # Merge the profits and losses dataframes
            merged = pd.merge(profits, losses, on='Month', how='outer', suffixes=('_Profit', '_Loss'))

            # Fill missing values with 0
            merged = merged.fillna(0)

            # Calculate the net profit or loss for each month
            merged['Net_Profit_Loss'] = merged['Sum_Profit'] + merged['Sum_Loss']


            # Assuming you have a DataFrame named 'merged' containing the data

            # Define the order of months
            month_order = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]

            # Convert 'Month' column to categorical with defined order
            merged['Month'] = pd.Categorical(merged['Month'], categories=month_order, ordered=True)

            # Sort the DataFrame by the categorical 'Month' column
            merged = merged.sort_values('Month')

            # Create a bar graph
            fig_month_rub = px.bar(merged, x='Month', y='Net_Profit_Loss',
                                    title='Net Profit/Loss by Month (Grouped)')
            fig_month_rub.update_traces(marker_color='green', selector=dict(type='bar', marker_line_color='green'))
            fig_month_rub.update_xaxes(title_text='Month')
            fig_month_rub.update_yaxes(title_text='Net Profit/Loss')



            container = st.container(border=True)  
            with container:

                st.write('<h4 style="text-align: center;">Profit/Loss by Time (RUB)</h4>', unsafe_allow_html=True)
                
                st.markdown('''
                    <h2 style='text-align: center; font-size: 12px;'>
                        July and the Summer in general were heavy expenditure months.
                        Investments in Equipment were usually made in the summer as well as expenditures for accounting services and International
                        Memberships such as the FIL/World Lacrosse.
                    </h2>
                ''', unsafe_allow_html=True)

                with st.expander('Profit/Loss by Month (Grouped)'):                
                    st.plotly_chart(fig_month_rub, use_container_width=True)

                


                with st.expander('Profit/Loss by Year (Grouped)'): 
                    st.plotly_chart(fig_net_rub, use_container_width=True)


            container = st.container(border=True)  
            with container:

                st.write('<h4 style="text-align: center;">Profit Category Analysis (RUB)</h4>', unsafe_allow_html=True)
    

             
                with st.expander('Total Sum Leading Categories'):
                    st.plotly_chart(fig_total_sum_rub, use_container_width=True)
                
                with st.expander('Transactions per Category'):
                    st.plotly_chart(fig_transactions_rub, use_container_width=True)

                with st.expander('Profit per Transaction'):
                    st.plotly_chart(fig_profit_loss_rub, use_container_width=True)

            st.write('''In the RUB fund the Membership Fee (~100 RUB per person per practice) was the main source of income until 
                     2017 since practices were conducted on city property no field rental was needed. 
                     Therefore to keep the cost of practices down, and to reimburse the fund for amortization of equipment,
                     logistics, and other expenses were funded
                     mostly by the Membership Fee. After the Membership Fee was discontinued, it was replaced by profit
                     from equipment sales and field rental as well as other minor revenue sources.                     
                        ''')   
            st.write('''However, the most profitable transaction was having any type of Events, such as intra-squad games, championships,
                     tournaments, where a large amount of players would come and provide a large profit boost for the fund, as well as a 
                     boost in overall morale since these games were very competitive and of a high level (for Russia). In our experience, one event
                     a quarter is a good frequency since doing it too many times lowered the attendance rate of each individual event. 
                     i.e. Supply/Demand. Events once a quarter (instead of monthly) increased the intrinsic value of the event and gave people something to look forward to 
                     and get excited about. Additionally, since
                     the events were not common, people made an effort to come to them as they wouldn't have another chance to play
                     on a high level for another 3 months.
                        ''')    
            

        




        with col2:
            container = st.container(border=True)  
            with container: 
                source = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 10, 10, 10, 10]
                target = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 12, 13, 14, 15]

                # Values for the links
                value = [310, 259, 250, 240, 195, 181, 80, 25, 5, 2000, 250, 181, 68, 2000, 1046]

                # Creating the Sankey diagram
                fig_sankey2 = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color='black', width=0.5),
                        
                        label=['Head Sale', 'Shafts Sale', 'Savings', 'Helmet Sale', 'Gloves Sale', 'Reimbursement',
                               'Elbows Sale', 'Strings Sale', 'Equipment Sale', 'Rolling Inventory', 'Total Income',
                                'Elbows Purchase', 'Ball Purchases', 'Strings Purchase', 'Rolling Inventory', 'Payout'],

                        color=[
                        'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen',
                        'lightgreen', 'lightgreen', 'lightblue',
                        'indianred', 'indianred', 'indianred', 'indianred', 'indianred'
                        ]  
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value,
                        color='rgba(0, 0, 0, .05)'  # Example: semi-transparent black lines
                    )
                )])

                # Updating layout properties
                fig_sankey2.update_layout(title_text="USD Fund Cash Flow")

                # Show the Sankey diagram
                st.plotly_chart(fig_sankey2, use_container_width=True)

                st.markdown('''
                    <h2 style='text-align: center; font-size: 12px;'>
                        *Since the USD fund does not have as many Categories, the Equipment Category was extrapolated to show a better
                        cash flow picture. Therefore, in the USD fund chart "Equipment" is non-player equipment. Things such as goals, nets, cones, etc.
                    </h2>
                ''', unsafe_allow_html=True)

                

            



            df_filtered_usd = df_fin_usd[~df_fin_usd['Commentary'].str.contains('(Liquidation)', na=False)]

            
            # Extract the year from the 'Date' column
            df_filtered_usd['Year'] = df_filtered_usd['Date'].dt.year

            # Calculate the sum of profits and losses for each year
            profits = df_filtered_usd[df_filtered_usd['Sum'] > 0].groupby('Year')['Sum'].sum()
            losses = df_filtered_usd[df_filtered_usd['Sum'] < 0].groupby('Year')['Sum'].sum()

            # Calculate the net profit or loss for each year
            net_profit_loss = profits.add(losses, fill_value=0)

            # Convert 'Year' to strings
            net_profit_loss.index = net_profit_loss.index.astype(str)

            # Create a bar graph
            fig_net_usd = px.bar(x=net_profit_loss.index, y=net_profit_loss.values, title='Net Profit/Loss by Year USD Fund')
            fig_net_usd.update_traces(marker_color='green', selector=dict(type='bar', marker_line_color='green'))
            fig_net_usd.update_xaxes(title_text='Year')
            fig_net_usd.update_yaxes(title_text='Net Profit/Loss')
                         

            category_summary_usd = df_fin_usd.groupby('Category').agg({'Sum': ['sum', 'count']})
            category_summary_usd.columns = ['Total Sum', 'Number of Transactions']
            category_summary_usd = category_summary_usd.reset_index()

            category_summary_usd['Profit/Loss per Transaction'] = category_summary_usd['Total Sum'] / category_summary_usd['Number of Transactions']

            # Sort the DataFrame by 'Total Sum' in descending order and select the top 5 rows
            top_5_total_sum_usd = category_summary_usd.sort_values(by='Total Sum', ascending=False).head(5)

            # Create a horizontal bar graph for 'Total Sum'
            fig_total_sum_usd = px.bar(top_5_total_sum_usd, x='Category', y='Total Sum',
                                title='Categories by Total Sum (USD)')

            # Create a horizontal bar graph for 'Number of Transactions'
            top_10_transactions_usd = category_summary_usd.sort_values(by='Number of Transactions', ascending=False).head(5)
            fig_transactions_usd = px.bar(top_10_transactions_usd, x='Category', y='Number of Transactions',
                                    title='Number of Transactions per Category (USD)')

            # Create a horizontal bar graph for 'Profit/Loss per Transaction'
            top_10_profit_loss_usd = category_summary_usd.sort_values(by='Profit/Loss per Transaction', ascending=False).head(5)
            fig_profit_loss_usd = px.bar(top_10_profit_loss_usd, x='Category', y='Profit/Loss per Transaction',
                                    title='Profit/Loss per Transaction (USD)')

            # Extract the month from the 'Date' column
            df_fin_usd['Month'] = df_fin_usd['Date'].dt.strftime('%B')

            # Calculate the sum of profits and losses for each month
            profits = df_fin_usd[df_fin_usd['Sum'] > 0].groupby('Month')['Sum'].sum().reset_index()
            losses = df_fin_usd[df_fin_usd['Sum'] < 0].groupby('Month')['Sum'].sum().reset_index()

            # Merge the profits and losses dataframes
            merged = pd.merge(profits, losses, on='Month', how='outer', suffixes=('_Profit', '_Loss'))

            # Fill missing values with 0
            merged = merged.fillna(0)

            # Calculate the net profit or loss for each month
            merged['Net_Profit_Loss'] = merged['Sum_Profit'] + merged['Sum_Loss']


            # Assuming you have a DataFrame named 'merged' containing the data

            # Define the order of months
            month_order = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]

            # Convert 'Month' column to categorical with defined order
            merged['Month'] = pd.Categorical(merged['Month'], categories=month_order, ordered=True)

            # Sort the DataFrame by the categorical 'Month' column
            merged = merged.sort_values('Month')

            # Create a bar graph
            fig_month_usd = px.bar(merged, x='Month', y='Net_Profit_Loss',
                                    title='Net Profit/Loss by Month (Grouped)')
            fig_month_usd.update_traces(marker_color='green', selector=dict(type='bar', marker_line_color='green'))
            fig_month_usd.update_xaxes(title_text='Month')
            fig_month_usd.update_yaxes(title_text='Net Profit/Loss')



            container = st.container(border=True) 
            with container: 

                st.write('<h4 style="text-align: center;">Profit/Loss by Time (USD)</h4>', unsafe_allow_html=True)

            
                st.markdown('''
                    <h2 style='text-align: center; font-size: 12px;'>
                        In the USD fund, May 2022 was the month of fund liquidation, all the cash in the fund was returned to the founders. While the RUB fund shows a 
                        modest loss, RUB profits in May over the years helped offset the liquidation loss.
                        However, since the USD fund was still young, the loss looks more severe as there were not as many years of profit in May
                        to cover the liquidation loss. There were even some months and years that showed no transactions. 
                        
                    </h2>
                ''', unsafe_allow_html=True)



                with st.expander('Profit/Loss by Month (Grouped)'):   

                                                     
                    st.plotly_chart(fig_month_usd, use_container_width=True)

         

                with st.expander('Profit/Loss by Year (Grouped)'): 
                    st.plotly_chart(fig_net_usd, use_container_width=True)


            container = st.container(border=True)  
            with container:
            
                st.write('<h4 style="text-align: center;">Profit Category Analysis (USD)</h4>', unsafe_allow_html=True)

             
                with st.expander('Profit/Loss per Category USD'):
                    st.plotly_chart(fig_total_sum_usd, use_container_width=True)
                
                with st.expander('Transactions per Category USD'):
                    st.plotly_chart(fig_transactions_usd, use_container_width=True)

                with st.expander('Leading Category for P/L per Transaction USD'):
                    st.plotly_chart(fig_profit_loss_usd, use_container_width=True)
            

            st.write('''The USD fund shows that the majority of the revenue, (excluding a credit from savings of \$250) was all for Player Equipment. 
                        Although the liquidation payout nullified any remaining funds from all sources, there still remained a 
                        rolling inventory of about \$2000 that still belongs to the fund.
                        ''')

       
            
            








   

    elif selected_subsection == "Equipment Data":

        st.write('<h2 style="text-align: center;">Equipment Sales Data</h2>', unsafe_allow_html=True)
        st.markdown("""
                <p style='text-align: center;'>
                    Equipment sales transactions were gradually migrated from the RUB fund to the USD fund over time to combat the falling Ruble. At the time of liquidation,
                    both funds were still selling equipment. 
                </p>
            """, unsafe_allow_html=True)
        

        ##############################Data Bank#################################################3

        df_fin_rub = df_fin[~df_fin['Classification'].str.contains('USD')]

        #order_refund_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Order Refund', 'Sum'].sum()
        #payment_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Payment', 'Sum'].sum()
        #payout_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Payout', 'Sum'].sum()
        #player_fine_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Player Fine', 'Sum'].sum()
        #reimbursement_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Reimbursement', 'Sum'].sum()
        shoulders_sale_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Shoulders Sale', 'Sum'].sum()
        #transfer_to_artur_total_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Transfer to Artur', 'Sum'].sum()
        ##bank_interest_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Credit', 'Sum'].sum()
        #materials_purchase_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Materials Purchase', 'Sum'].sum()
        ##lacrosse_clinic_rub = df_fin_rub.loc[df_fin_rub['Operation'] == 'Lacrosse Clinic', 'Sum'].sum()
        ball_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Ball Purchase', 'Ball Sale', 'Ball Purchases']), 'Sum'].sum()
        elbows_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Elbows Purchase', 'Elbows Sale']), 'Sum'].sum()
        equipment_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Equipment Purchase', 'Equipment Sale']), 'Sum'].sum()
        ##field_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Field Fees', 'Field Rental']), 'Sum'].sum()
        gloves_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Gloves Purchase', 'Gloves Sale']), 'Sum'].sum()
        head_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Head Purchase', 'Head Sale']), 'Sum'].sum()
        helmet_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Helmet Purchase', 'Helmet Sale']), 'Sum'].sum()
        ##loan_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Loan Issuance', 'Loan Repayment', 'Loan']), 'Sum'].sum()
        ##membership_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Membership Fee', 'Membership Fee EFL', 'Membership Fee FIL']), 'Sum'].sum()
        shafts_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Shafts Purchase', 'Shafts Sale']), 'Sum'].sum()
        stick_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Stick Sale', 'Sticks Purchase']), 'Sum'].sum()
        strings_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['Strings Purchase', 'Strings Sale']), 'Sum'].sum()
        t_shirt_total_rub = df_fin_rub.loc[df_fin_rub['Operation'].isin(['T-Shirt Sale', 'T-Shirts Purchase']), 'Sum'].sum()


        ###############################################


        
        

        ##################################################Data Bank############################################3

        # Calculate the total sums for each operation
        total_sums_rub = [
            ("Ball", ball_total_rub),
            ("Elbows", elbows_total_rub),
            ("Equipment", equipment_total_rub),
            #("Field", field_total_rub),
            ("Gloves", gloves_total_rub),
            ("Head", head_total_rub),
            ("Helmet", helmet_total_rub),
            #("Loan", loan_total_rub),
            #("Membership", membership_total_rub),
            ("Shafts", shafts_total_rub),
            ("Stick", stick_total_rub),
            ("Strings", strings_total_rub),
            ("T-Shirt", t_shirt_total_rub),
            #("Clinic", lacrosse_clinic_rub),
            #("Bank Interest", bank_interest_rub),
            ("Shoulder Pads", shoulders_sale_total_rub),
            

        ]

        # Create a DataFrame
        df_total_sums_rub = pd.DataFrame(total_sums_rub, columns=["Operation", "Total Sum"])

        # Sort the DataFrame by Total Sum in descending order
        df_total_sums_rub  = df_total_sums_rub .sort_values(by="Total Sum", ascending=False)

        # Select the top (x) rows
        top_total_sums_rub = df_total_sums_rub .head(25)

        # Create a bar graph
        fig_op_profit_rub = px.bar(
            top_total_sums_rub,
            x="Operation",
            y="Total Sum",
            labels={"Total Sum": "Total Sum (RUB)"},
            title="Top Profit for RUB Operations",
        )

        # Show the graph
     
        


        ###################################################


        # Group the data by 'Operation' and sum the 'Sum' values for each group
        operation_summary_rub = df_fin_rub.groupby('Operation')['Sum'].sum().reset_index()

        # Sort the data in descending order by the 'Sum' column and get the top (x) rows
        top_operations_rub = operation_summary_rub.sort_values(by='Sum', ascending=False).head(15)

        # Create a bar graph using Plotly Express
        fig_op_revenue_rub = px.bar(top_operations_rub, x='Operation', y='Sum', title='Top Operations by Revenue (RUB)')

      

     

        # Exclude specific operation types
        operations_to_exclude = ["Field Fees", "Payout", "Payment", "Field Rental", "Loan", "Membership Fee", "Loan Issuance", "Loan Repayment", "Lacrosse Clinic", "Membership Fee EFL", "Membership Fee FIL", "Clinic", "Bank Interest", "Order Refund", "Reimbursement", "Player Fine", "Credit", "Transfer to Artur", "Materials Purchase"]
        operation_summary_rub = operation_summary_rub[~operation_summary_rub['Operation'].isin(operations_to_exclude)]

        # Get the top operations
        top_operations_rub = operation_summary_rub.sort_values(by='Sum', ascending=False).head(25)

        # Create the bar chart
        fig_op_revenue_rub = px.bar(top_operations_rub, x='Operation', y='Sum', title='Top Equipment Operations by Revenue (RUB)')

       

        
        
        


        ##################################################################

        # Filter the DataFrame for 'Equipment' operations in the 'Category' column
        equipment_df_rub = df_fin_rub[df_fin_rub['Category'].str.contains('Equipment', case=False, na=False)]

        # Extract the year from the 'Date' column
        equipment_df_rub['Year'] = equipment_df_rub['Date'].dt.year

        # Group by year and count the occurrences
        count_by_year = equipment_df_rub.groupby('Year').size().reset_index(name='Count')

        # Create a line graph
        fig_equip_rub = px.line(count_by_year, x='Year', y='Count', title='Equipment Operations Over Time RUB Fund')
        fig_equip_rub.update_xaxes(title_text='Year')
        fig_equip_rub.update_yaxes(title_text='Count')






        ##################################################################

        col1, col2 = st.columns(2)

       

        with col1:
            container = st.container(border=True)  
            with container:

                st.plotly_chart(fig_equip_rub, use_container_width=True)
            
            container = st.container(border=True)  
            with container: 

                st.plotly_chart(fig_op_profit_rub, use_container_width=True)
                st.markdown("""
                    <p style='text-align: center;'>
                        While Sticks were the most profitable item, they were sometimes assembled from parts of heads and shafts, which is reflected
                        in the statistics for shafts. Heads were replaced at a much higher rate than shafts, so sitting inventory and using shafts for
                        complete-stick assembly skewed the profit calculations. Equipment in this case is goals/nets/cones/bags/etc.
                    
                    </p>
                """, unsafe_allow_html=True)

            container = st.container(border=True)  
            with container:

                st.plotly_chart(fig_op_revenue_rub, use_container_width=True)
                st.markdown("""
                    <p style='text-align: center;'>
                        This shows a more detailed view of how much was purchased and sold over the duration of the fund. All leftovers are now in the USD 
                        Rolling inventory valued and denominated in USD at the time of liquidation. 
                    </p>
                """, unsafe_allow_html=True)

            




        df_fin_usd = df_fin[df_fin['Classification'].str.contains('USD')]

        # Create variables for each pair/group of usd operations
        ball_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Ball Purchase', 'Ball Sale', 'Ball Purchases']), 'Sum'].sum()
        elbows_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Elbows Purchase', 'Elbows Sale']), 'Sum'].sum()
        equipment_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Equipment Purchase', 'Equipment Sale']), 'Sum'].sum()
        #field_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Field Fees', 'Field Rental']), 'Sum'].sum()
        gloves_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Gloves Purchase', 'Gloves Sale']), 'Sum'].sum()
        head_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Head Purchase', 'Head Sale']), 'Sum'].sum()
        helmet_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Helmet Purchase', 'Helmet Sale']), 'Sum'].sum()
        #loan_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Loan Issuance', 'Loan Repayment', 'Loan']), 'Sum'].sum()
        #membership_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Membership Fee', 'Membership Fee EFL', 'Membership Fee FIL']), 'Sum'].sum()
        shafts_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Shafts Purchase', 'Shafts Sale']), 'Sum'].sum()
        #stick_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Stick Sale', 'Sticks Purchase']), 'Sum'].sum()
        strings_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['Strings Purchase', 'Strings Sale']), 'Sum'].sum()
        t_shirt_total_usd = df_fin_usd.loc[df_fin_usd['Operation'].isin(['T-Shirt Sale', 'T-Shirts Purchase']), 'Sum'].sum()


        # Calculate the total sums for each operation
        total_sums_usd = [
            ("Ball", ball_total_usd),
            ("Elbows", elbows_total_usd),
            ("Equipment", equipment_total_usd),
            
            ("Gloves", gloves_total_usd),
            ("Head", head_total_usd),
            ("Helmet", helmet_total_usd),
           
           
            ("Shafts", shafts_total_usd),
           
            ("Strings", strings_total_usd),
           
            
        ]

        # Create a DataFrame
        df_total_sums_usd = pd.DataFrame(total_sums_usd, columns=["Operation", "Total Sum"])

        # Sort the DataFrame by Total Sum in descending order
        df_total_sums_usd  = df_total_sums_usd .sort_values(by="Total Sum", ascending=False)

        # Select the top (x) rows
        top_total_sums_usd = df_total_sums_usd .head(25)

        # Create a bar graph
        fig_op_profit_usd = px.bar(
            top_total_sums_usd,
            x="Operation",
            y="Total Sum",
            labels={"Total Sum": "Total Sum (usd)"},
            title="Top Profit for USD Operations",
        )

        # Show the graph
        
        


        #########################################################################

        # Group the data by 'Operation' and sum the 'Sum' values for each group
        operation_summary_usd = df_fin_usd.groupby('Operation')['Sum'].sum().reset_index()

        # Sort the data in descending order by the 'Sum' column and get the top (x) rows
        #top_operations_usd = operation_summary_usd.sort_values(by='Sum', ascending=False).head(12)

        # Create a bar graph using Plotly Express
        #fig_op_revenue_usd = px.bar(top_operations_usd, x='Operation', y='Sum', title='Top Equipment Operations by Revenue (USD)')

       

        # Exclude specific operation types
        operations_to_exclude = ["Reimbursement", "Payout", "Savings"]
        operation_summary_usd = operation_summary_usd[~operation_summary_usd['Operation'].isin(operations_to_exclude)]

        # Get the top operations
        top_operations_usd = operation_summary_usd.sort_values(by='Sum', ascending=False).head(25)

        # Create the bar chart
        fig_op_revenue_usd = px.bar(top_operations_usd, x='Operation', y='Sum', title='Top Equipment Operations by Revenue (USD)')
        

        

        
        
        



        #########################################################

        
        

      
        
        


        #########################################################

        # Filter the DataFrame for 'Equipment' operations in the 'Category' column
        equipment_df_usd = df_fin_usd[df_fin_usd['Category'].str.contains('Equipment', case=False, na=False)]

        # Extract the year from the 'Date' column
        equipment_df_usd['Year'] = equipment_df_usd['Date'].dt.year

        # Group by year and count the occurrences
        count_by_year = equipment_df_usd.groupby('Year').size().reset_index(name='Count')

        # Create a line graph
        fig_equip_usd = px.line(count_by_year, x='Year', y='Count', title='Equipment Operations Over Time USD Fund')
        fig_equip_usd.update_xaxes(title_text='Year')
        fig_equip_usd.update_yaxes(title_text='Count')

        # Show the graph


        ##################################################### ##############
        with col2:
            container = st.container(border=True)  
            with container:
        
                st.plotly_chart(fig_equip_usd, use_container_width=True)

            container = st.container(border=True)  
            with container:

                st.plotly_chart(fig_op_profit_usd, use_container_width=True)
                st.markdown("""
                    <p style='text-align: center;'>
                        Not long before liquidation, a large purchase of elbows strings and balls was still unsold in our rolling inventory.
                        This purchase was to cover the elbow pad and string needs of the club for at least 5 years.
                            
                    </p>
                """, unsafe_allow_html=True)
            
            

            container = st.container(border=True)  
            container.markdown("""
                <style>
                    .st-geAtf {
                        background-color: #f2f2f2; /* Replace with your desired grey color */
                        padding: 10px; /* Optional: Add padding for better appearance */
                    }
                </style>
            """, unsafe_allow_html=True)


            with container:

                st.plotly_chart(fig_op_revenue_usd, use_container_width=True)
                st.markdown("""
                    <p style='text-align: center;'>
                        Heads and shafts (unassembled sticks) are the most profitable and most purchased items in the equipment category. Unfortunately
                        Elbows, and Strings didn't have a chance to sell off. Balls are consumables that were also sold, but never profitable since most of them
                        got used before being sold, and were considered an unavoidable expense. 
                         
                    </p>
                """, unsafe_allow_html=True)

            
                 
                
            
            












def show_attendance_data():
        
    # Display the selected subsection content
    selected_subsection = st.sidebar.radio("Go to", ("Summary", "Player Stats"))
    st.write('<h1 style="text-align: center;">Attendance Data</h1>', unsafe_allow_html=True)
        



    if selected_subsection == "Summary":
                
        st.write('<h2 style="text-align: center;">All Events</h2>', unsafe_allow_html=True)

        # Add CSS for styling the dashboard
        st.markdown(
            """
            <style>
                .dashboard-column {
                    text-align: center;
                    background-color: skyblue;
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


        bg_color = 'skyblue'
    
        # Add CSS for rounded corners
        st.markdown(
            """
            <style>
            .dashboard-column {
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
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
        filtered_attendees = [attendee for attendee in all_attendees if attendee != "No Data" and len(attendee.split()) <= 3]
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


        ############################################################################
###################################################################################
 
        ##filler for spacing
        st.markdown("<br>", unsafe_allow_html=True)

#############################################################
        #############################################################################

        container = st.container(border=True)  
        with container:

            # Title of chart
            st.write("<h3 style='text-align: center;'>Attendance Over Time</h3>", unsafe_allow_html=True)
            

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
                marker=dict(color='skyblue'),  # Set the bar color here
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

            container = st.container(border=True)  
            with container:

                # Display the plot in Streamlit
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("""
                    <p style='text-align: center;'>
                        The attendance average dropped from 2015 was due to the club adding weekday skills practices.
                        Skills practices were conducted near two of the founders in different parts of the city. However, since the attendance of the 
                        skills practices were lower and skills practices were more frequent, the total average attendees per event dropped significantly. 
                    </p>
                """, unsafe_allow_html=True)

            def calculate_cumulative_unique_attendees(df):
                cumulative_unique_attendees = []
                unique_attendees = set()

                for year in range(2015, df['Date_Date_Excel'].dt.year.max() + 1):
                    attendees_in_year = df[df['Date_Date_Excel'].dt.year <= year]['Going'].str.split(', ').explode()
                    # Filter out specific entries
                    attendees_filtered = [attendee for attendee in attendees_in_year if attendee not in ["No Data", "No Name"] and len(attendee.split()) <= 3]
                    unique_attendees.update(attendees_filtered)
                    cumulative_unique_attendees.append(len(unique_attendees))

                return cumulative_unique_attendees

        

            # Calculate cumulative unique attendees
            cumulative_counts = calculate_cumulative_unique_attendees(df_att)

            # Plot cumulative unique attendees count for each year using Plotly
            years = range(2015, df_att['Date_Date_Excel'].dt.year.max() + 1)
            data = {"Year": years, "Cumulative Unique Attendees": cumulative_counts}
            fig_unique = px.line(data, x="Year", y="Cumulative Unique Attendees")
            fig_unique.update_traces(line=dict(color='skyblue'))  # Set the line color

            

               
            with st.expander('Unique Attendees Per Year'):
                 st.plotly_chart(fig_unique, use_container_width=True)



        

        #####################################################################
        container = st.container(border=True)  
        with container:
            st.write("<h3 style='text-align: center;'>Field Rental Operations</h3>", unsafe_allow_html=True)
            with st.expander('By Year'):
                
                # Filter the DataFrame for 'Field Rental' operations
                field_rental_df = df_fin[df_fin['Operation'] == 'Field Rental']

                # Group by year and count the occurrences
                field_rental_df['Year'] = field_rental_df['Date'].dt.year
                count_by_year = field_rental_df.groupby('Year').size().reset_index(name='Count')

                # Create a line graph
                fig_fieldrental = px.line(count_by_year, x='Year', y='Count')
                fig_fieldrental.update_traces(line=dict(color='skyblue'))  # Change to your desired color
                fig_fieldrental.update_xaxes(title_text='Year')
                fig_fieldrental.update_yaxes(title_text='Count')

                # Show the graph
                
                st.plotly_chart(fig_fieldrental, use_container_width=True)

        ####################################################################
        
        
            with st.expander('By Month'):
                

                # Extract the month from the 'Date' column
                field_rental_df['Month'] = field_rental_df['Date'].dt.strftime('%B')

                # Define a custom sorting order for months
                month_order = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]

                # Group by month and count the occurrences
                count_by_month = field_rental_df.groupby('Month').size().reset_index(name='Count')

                # Sort the months in chronological order
                count_by_month['Month'] = pd.Categorical(count_by_month['Month'], categories=month_order, ordered=True)
                count_by_month = count_by_month.sort_values('Month')

                # Create a line graph
                fig_rentalmonth = px.line(count_by_month, x='Month', y='Count')
                fig_rentalmonth.update_traces(line=dict(color='skyblue'))  # Change to your desired color
                fig_rentalmonth.update_xaxes(title_text='Month')
                fig_rentalmonth.update_yaxes(title_text='Count')

                # Show the graph
                st.plotly_chart(fig_rentalmonth, use_container_width=True)
                st.markdown("""
                    <p style='text-align: center;'>
                        In the first few years, all practices during acceptable weather were conducted on free courts/fields, which limited the need
                        for field rental to only Championships/Intra-Squad games on full-size fields. 
                    </p>
                """, unsafe_allow_html=True)








        #####################################################################
        # Title of chart
        
            
            


            def calculate_cumulative_unique_attendees(df):
                cumulative_unique_attendees = []
                unique_attendees = set()

                for year in range(2015, df['Date_Date_Excel'].dt.year.max() + 1):
                    attendees_in_year = df[df['Date_Date_Excel'].dt.year <= year]['Going'].str.split(', ').explode()
                    # Filter out specific entries
                    attendees_filtered = [attendee for attendee in attendees_in_year if attendee not in ["No Data", "No Name"] and len(attendee.split()) <= 3]
                    unique_attendees.update(attendees_filtered)
                    cumulative_unique_attendees.append(len(unique_attendees))

                return cumulative_unique_attendees

        

           
               

















        #######################################################

        # Filter DataFrame for team practices and skills practices
        team_practices = completed_events[completed_events['Type'] == 'Team Practice']
        skills_practices = completed_events[completed_events['Type'] == 'Skills Practice']

        # Calculate total attendance for team practices per year
        total_attendance_team_practices = team_practices.groupby('Year')['Attendance'].sum()
        # Calculate total attendance for skills practices per year
        total_attendance_skills_practices = skills_practices.groupby('Year')['Attendance'].sum()

        # Calculate average attendance per event per year for Team Practice
        average_attendance_team_practice_per_year = team_practices.groupby('Year')['Attendance'].mean()
        rounded_average_attendance_team_practice = average_attendance_team_practice_per_year.round(1)

        # Calculate average attendance per event per year for Skills Practice
        average_attendance_skills_practice_per_year = skills_practices.groupby('Year')['Attendance'].mean()
        rounded_average_attendance_skills_practice = average_attendance_skills_practice_per_year.round(1)


        # Assign the categorical data to the DataFrame
        df_att['Month_Name'] = df_att['Date_Date_Excel'].dt.strftime('%B')
        team_practices['Month_Name'] = team_practices['Date_Date_Excel'].dt.strftime('%B')
        skills_practices['Month_Name'] = skills_practices['Date_Date_Excel'].dt.strftime('%B')

        # Create a categorical data type with month names in correct order
        months_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        cat_month = pd.Categorical(df_att['Month_Name'], categories=months_order, ordered=True)
        cat_month1 = pd.Categorical(team_practices['Month_Name'], categories=months_order, ordered=True)
        cat_month2 = pd.Categorical(skills_practices['Month_Name'], categories=months_order, ordered=True)

        # Assign the categorical data to the DataFrame
        df_att['Month_Name'] = cat_month
        team_practices['Month_Name'] = cat_month1
        skills_practices['Month_Name'] = cat_month2
        

        
        event_attendance_per_month = df_att.groupby('Month_Name')['Attendance'].sum()
        avg_attendance_per_event_per_month = df_att.groupby('Month_Name')['Attendance'].mean()
        rounded_avg_attendance_per_event_per_month = avg_attendance_per_event_per_month.round(1)


        total_attendance_team_practices_month = team_practices.groupby('Month_Name')['Attendance'].sum()
        avg_attendance_team_practices_month = team_practices.groupby('Month_Name')['Attendance'].mean()
        rounded_avg_attendance_team_practices_month = avg_attendance_team_practices_month.round(1)

        total_attendance_skills_practices_month = skills_practices.groupby('Month_Name')['Attendance'].sum()
        avg_attendance_skills_practices_month = skills_practices.groupby('Month_Name')['Attendance'].mean()
        rounded_avg_attendance_skills_practices_month = avg_attendance_skills_practices_month.round(1)





        # Create subplots with secondary y-axis
        fig_events = make_subplots(specs=[[{'secondary_y': True}]])

        # Add bar chart for total events per month
        fig_events.add_trace(go.Bar(
            x=event_attendance_per_month.index,
            y=event_attendance_per_month.values,
            name="Total Attendance per Month",
            text=event_attendance_per_month.values, 
            textposition='inside',
            insidetextanchor='end',
            textfont=dict(size=16, color='black'),
            marker=dict(color='skyblue')
        ), secondary_y=False)

        # Add line chart for average attendance per event per month
        fig_events.add_trace(go.Scatter(
            x=avg_attendance_per_event_per_month.index,
            y=avg_attendance_per_event_per_month.values,
            mode='lines+markers+text',
            name='Avg Attendance per Event',
            marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
            text=rounded_avg_attendance_per_event_per_month,  # Replace with your rounded average values
            textposition='top center',
            textfont=dict(size=16, color='red'),
        ), secondary_y=True)

        # Set layout for the chart
        fig_events.update_layout(
            xaxis=dict(title='Month'),
            yaxis=dict(title='Total Attendees', showgrid=False, range=[0, event_attendance_per_month.max() + 100]),
            yaxis2=dict(title='Secondary Y-Axis Title', overlaying='y', side='right', showgrid=False),
            legend=dict(x=0.3, y=1, traceorder='normal', orientation='h'),
        )

        # Display the figure
       
        



##########################################################33


         # Create subplots with secondary y-axis
        fig_tp_mo = make_subplots(specs=[[{'secondary_y': True}]])

        # Add bar chart for total events per month
        fig_tp_mo.add_trace(go.Bar(
            x=total_attendance_team_practices_month.index,
            y=total_attendance_team_practices_month.values,
            name="Total Team Practice Attendance per Month",
            text=total_attendance_team_practices_month.values, 
            textposition='inside',
            insidetextanchor='end',
            textfont=dict(size=16, color='black'),
            marker=dict(color='skyblue')
        ), secondary_y=False)

         # Add line chart for average attendance per event per month
        fig_tp_mo.add_trace(go.Scatter(
            x=avg_attendance_team_practices_month.index,
            y=avg_attendance_team_practices_month.values,
            mode='lines+markers+text',
            name='Avg Attendance per Team Practice',
            marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
            text=rounded_avg_attendance_team_practices_month,  # Replace with your rounded average values
            textposition='top center',
            textfont=dict(size=16, color='red'),
        ), secondary_y=True)

        # Set layout for the chart
        fig_tp_mo.update_layout(
            xaxis=dict(title='Month'),
            yaxis=dict(title='Total Attendees', showgrid=False, range=[0, total_attendance_team_practices_month.max() + 100]),
            yaxis2=dict(title='Secondary Y-Axis Title', overlaying='y', side='right', showgrid=False),
            legend=dict(x=0.3, y=1, traceorder='normal', orientation='h'),
        )


        



###################################################################
       

         # Create subplots with secondary y-axis
        fig_sp_mo = make_subplots(specs=[[{'secondary_y': True}]])

        # Add bar chart for total events per month
        fig_sp_mo.add_trace(go.Bar(
            x=total_attendance_skills_practices_month.index,
            y=total_attendance_skills_practices_month.values,
            name="Total Skills Practice Attendance per Month",
            text=total_attendance_skills_practices_month.values, 
            textposition='inside',
            insidetextanchor='end',
            textfont=dict(size=16, color='black'),
            marker=dict(color='skyblue')
        ), secondary_y=False)

         # Add line chart for average attendance per event per month
        fig_sp_mo.add_trace(go.Scatter(
            x=avg_attendance_skills_practices_month.index,
            y=avg_attendance_skills_practices_month.values,
            mode='lines+markers+text',
            name='Avg Attendance per Skills Practice',
            marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
            text=rounded_avg_attendance_skills_practices_month,  # Replace with your rounded average values
            textposition='top center',
            textfont=dict(size=16, color='red'),
        ), secondary_y=True)

        # Set layout for the chart
        fig_sp_mo.update_layout(
            xaxis=dict(title='Month'),
            yaxis=dict(title='Total Attendees', showgrid=False, range=[0, total_attendance_skills_practices_month.max() + 100]),
            yaxis2=dict(title='Secondary Y-Axis Title', overlaying='y', side='right', showgrid=False, range=[0, avg_attendance_skills_practices_month.max() + 1]),
            legend=dict(x=0.3, y=1, traceorder='normal', orientation='h'),
        )


       



##################################################################

        ##filler for spacing
        st.markdown("<br><br>", unsafe_allow_html=True)


#################################################################


        container = st.container(border=True)  
        with container:

            st.write("<h3 style='text-align: center;'>Attendance per Month</h3>", unsafe_allow_html=True)

            st.markdown("""
                    <p style='text-align: center;'>
                        While Team Practices were stable throughout the year, when the weather would improve in Moscow, 
                        the club would conduct more Skills practices. The uptick in July was usually due to a Championship or 
                        Tournament that was usually attended by more people on average. 
                    </p>
                """, unsafe_allow_html=True)
            

            ##filler for spacing
            st.markdown("<br><br>", unsafe_allow_html=True)


        # Calculate cumulative unique attendees
            

            with st.expander('Total Attendees per Month'):
                    st.plotly_chart(fig_events, use_container_width=True)
                    
            
            with st.expander('Total Team Practice Attendees per Month'):
                    st.plotly_chart(fig_tp_mo, use_container_width=True)
                    st.markdown("""
                            <p style='text-align: center;'>
                                Summertime in Russia is a time to go to the country house ("dacha") outside of the city. These traditional weekend trips for the urban 
                                poplulation would take away from our attendance. Additionally, from April to October is vacation season in Russia, which would
                                take its share of the attendance as well. Initially practices were twice a weekend, but due to these persisting factors,
                                practices were limited to once a week. This raised the intrinsic value of each practice since they were less frequent, and over time would
                                raise the attendance level at each weekend team practice since people started to schedule their weekend knowing that there is no second
                                practice available that weekend for them.
                            </p>
                        """, unsafe_allow_html=True)

            with st.expander('Total Skills Practice Attendees per Month'):
                    st.plotly_chart(fig_sp_mo, use_container_width=True)
                    st.markdown("""
                            <p style='text-align: center;'>
                                Skills practices were available for free for everybody. In the beginning, Team Practices were just Skills Practices that 
                                grew too large for free courts/fields. So while the club developed a consistent regiment of team practices for experienced players,
                                skills practices were used and expanded to develop and maintain a solid on-boarding procedure for new players in multiple districts of Moscow. 
                                These free practices would provide the foundational skills and knowledge to be able to participate in Team Practices down the line, as
                                well as get to know the players and coaches of the team. i.e. these skills practices would be a valueable on-ramp for players wishing to 
                                join the team but haven't the experience, or are too intimidated to make the big leap from stick skills to pads and full contact. 
                            </p>
                        """, unsafe_allow_html=True)
            






###################################################################
##################################################################

        ##filler for spacing
        st.markdown("<br><br>", unsafe_allow_html=True)


#################################################################








        container = st.container(border=True)  
        with container:

            st.write("<h3 style='text-align: center;'>Lacrosse Event Attendance Segmented</h3>", unsafe_allow_html=True)


            # Create the layout for the dashboard row 1
            col1, col2, = st.columns(2) 

            


            # First row
            with col1:
                st.write("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)
                fig_team = go.Figure()

                fig_team.add_trace(go.Bar(
                    x=total_attendance_team_practices.index,
                    y=total_attendance_team_practices.values,
                    marker=dict(color='skyblue'),  # Set the bar color here
                    text=total_attendance_team_practices.values,
                    textposition='inside',
                    textfont=dict(size=16, color='black'),
                    name='Total Attendance'
                ))

                fig_team.add_trace(go.Scatter(
                    x=average_attendance_team_practice_per_year.index,
                    y=average_attendance_team_practice_per_year.values,
                    mode='lines+markers+text',
                    name='Avg Attendance per Event',
                    marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
                    text=rounded_average_attendance_team_practice.values,
                    textposition='top center',
                    textfont=dict(size=16, color='red'),
                    yaxis='y2'
                ))


                
                fig_team.update_layout(
                    xaxis=dict(title='Year'),
                    yaxis=dict(showgrid=False, range=[0, 900], showticklabels=False, showline=False),
                    yaxis2=dict(overlaying='y', side='right', showgrid=False, range=[6, 12], showticklabels=False, showline=False),
                    legend=dict(x=0.3, y=1, traceorder='normal', orientation='h'),
                )

                
                




            with col2:
                st.write("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)

                fig_skills = go.Figure()
                fig_skills.add_trace(go.Bar(
                    x=total_attendance_skills_practices.index,
                    y=total_attendance_skills_practices.values,
                    marker=dict(color='skyblue'),  # Set the bar color here
                    text=total_attendance_skills_practices.values,
                    textposition='inside',
                    textfont=dict(size=16, color='black'),
                    name='Total Attendance'
                ))

                fig_skills.add_trace(go.Scatter(
                    x=average_attendance_skills_practice_per_year.index,
                    y=average_attendance_skills_practice_per_year.values,
                    mode='lines+markers+text',
                    name='Avg Attendance per Event',
                    marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
                    text=rounded_average_attendance_skills_practice.values,
                    textposition='top center',
                    textfont=dict(size=16, color='red'),
                    yaxis='y2'
                ))

                fig_skills.update_layout(
                    xaxis=dict(title='Year'),
                    yaxis=dict(showgrid=False, range=[0, 300], showticklabels=False, showline=False),
                    yaxis2=dict(overlaying='y', side='right', showgrid=False, range=[0, 10], showticklabels=False, showline=False),
                    legend=dict(x=0.3, y=.99, traceorder='normal', orientation='h'),
                )


                # Set the x-axis to start from 2013
                fig_skills.update_xaxes(range=[2013, 2022])


                




            # Create the layout for the dashboard row 2
            col1, col2, = st.columns(2)

            # Filter data for 'Championship' and 'Intra-Squad Game'
            championship_events = completed_events[completed_events['Type'] == 'Championship']
            intra_squad_game_events = completed_events[completed_events['Type'] == 'Intra-Squad Game']

            # Compute total attendance for 'Championship' and 'Intra-Squad Game' per year
            total_attendance_championship = championship_events.groupby('Year')['Attendance'].sum()
            total_attendance_intra_squad_game = intra_squad_game_events.groupby('Year')['Attendance'].sum()

            # Compute average attendance per event per year for 'Championship' and 'Intra-Squad Game'
            average_attendance_championship_per_year = championship_events.groupby('Year')['Attendance'].mean()
            average_attendance_intra_squad_game_per_year = intra_squad_game_events.groupby('Year')['Attendance'].mean()

            
            # Round average attendance for Championship per year to tenths
            average_attendance_championship_per_year = average_attendance_championship_per_year.round(1)

            # Round average attendance for Intra-Squad Game per year to tenths
            average_attendance_intra_squad_game_per_year = average_attendance_intra_squad_game_per_year.round(1)

            
            ################## chart 4 data (2nd chart in 2nd row) ######################

            # Filter the DataFrame for 'Tournament' events
            tournament_events = df_att[df_att['Type'] == 'Tournament']

            # Compute total attendance per year for Tournament events
            total_attendance_per_year_tournament = tournament_events.groupby('Year')['Attendance'].sum()
            

            # Filter the DataFrame for 'Intra-Squad Game' events
            intra_squad_events = df_att[df_att['Type'] == 'Intra-Squad Game']

            # Compute total attendance per year for Intra-Squad Game events
            total_attendance_per_year_intra_squad_game = intra_squad_events.groupby('Year')['Attendance'].sum()

            # Concatenate the two dataframes
            combined_events = pd.concat([intra_squad_events, tournament_events])

            # Concatenate the two dataframes
            average_combined = combined_events.groupby('Year')['Attendance'].mean()



            #############################################################




            # second row
            with col1:
                st.write("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)
                fig_championship = go.Figure()

                # Add bar chart for total attendance
                fig_championship.add_trace(go.Bar(
                    x=total_attendance_championship.index,
                    y=total_attendance_championship.values,
                    marker=dict(color='skyblue'),
                    text=total_attendance_championship.values,
                    textposition='inside',
                    textfont=dict(size=16, color='black'),
                    name='Championship Attendance'
                ))

                # Add line chart for average attendance per event per year
                fig_championship.add_trace(go.Scatter(
                    x=average_attendance_championship_per_year.index,
                    y=average_attendance_championship_per_year.values,
                    mode='lines+markers+text',
                    name='Avg Attendance per Event',
                    marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
                    text=average_attendance_championship_per_year.values,
                    textposition='top center',
                    textfont=dict(size=16, color='red'),
                    yaxis='y2'
                ))

                fig_championship.update_layout(
                    xaxis=dict(title='Year'),
                    yaxis=dict(showgrid=False, range=[0, 75], showticklabels=False, showline=False),
                    yaxis2=dict(overlaying='y', side='right', showgrid=False, range=[0, 35], showticklabels=False, showline=False),
                    legend=dict(x=0.3, y=1, traceorder='normal', orientation='h'),
                )

                with st.expander('Team Practice Attendance'):
                    st.plotly_chart(fig_team, use_container_width=True)
                    st.markdown("""
                    <p style='text-align: center;'>
                        2018 was a busy year outside of practices. There were tournaments, the World Championship in Israel, recovery time after the
                        Championship, vacations and weather factors limited the amount of times the team could get together in 2018. 
                    </p>
                """, unsafe_allow_html=True)



                with st.expander('Championship Attendance'):
                    st.plotly_chart(fig_championship, use_container_width=True)
                    st.markdown("""
                            <p style='text-align: center;'>
                                Championship Attendance was consistently growing over the years. As seen in lower charts, Championships had one of the best average attendance
                                records for all events.  Everyone loves a Championship.
                            </p>
                        """, unsafe_allow_html=True)
                
                    


            
            with col2:
                st.write("<h3 style='text-align: center;'></h3>", unsafe_allow_html=True)
                fig_intra_tour = go.Figure()

                # Add bar chart for total attendance - Tournament
                fig_intra_tour.add_trace(go.Bar(
                    x=total_attendance_per_year_tournament.index,
                    y=total_attendance_per_year_tournament.values,
                    marker=dict(color='skyblue'),
                    text=total_attendance_per_year_tournament.values,
                    textposition='inside',
                    textfont=dict(size=16, color='black'),
                    name='Tournament Attendance'
                ))

                # Add bar chart for Intra-Squad Game attendance, stacked on top of Tournament attendance
                fig_intra_tour.add_trace(go.Bar(
                    x=total_attendance_per_year_intra_squad_game.index,
                    y=total_attendance_per_year_intra_squad_game.values,
                    marker=dict(color='aqua'),
                    text=total_attendance_per_year_intra_squad_game.values,
                    textposition='inside',
                    textfont=dict(size=16, color='black'),
                    name='Intra-Squad Game Attendance'
                ))

                # Add line chart for the average of Tournament and Intra-Squad Game attendance
                fig_intra_tour.add_trace(go.Scatter(
                    x=average_combined.index,
                    y=average_combined.values,
                    mode='lines+markers+text',
                    name='Avg Combined Attendance',
                    marker=dict(color='rgba(255, 0, 0, 0.7)', size=10),
                    text=average_combined.values.round(1),
                    textposition='top center',
                    textfont=dict(size=16, color='red'),
                    yaxis='y2'
                ))



                fig_intra_tour.update_layout(
                    xaxis=dict(title='Year'),
                    yaxis=dict(showgrid=False, range=[0, 275], showticklabels=False, showline=False),
                    yaxis2=dict(overlaying='y', side='right', showgrid=False, range=[0, 23], showticklabels=False, showline=False),
                    legend=dict(x=0.1, y=1, traceorder='normal', orientation='h'),
                    barmode='stack'  # Stacked bar mode
                )


                with st.expander('Skills Practice Attendance'):  
                    st.plotly_chart(fig_skills, use_container_width=True)
                    st.markdown("""
                            <p style='text-align: center;'>
                                At the end of 2016, one of the founders holding practices moved to a different district in Moscow.
                                this decreased the Total Attendance since the host was now 45mins away from his previous location, 
                                which limited the attendance willing and able to travel that far for skills practices. 
                            </p>
                        """, unsafe_allow_html=True)



                with st.expander('Intra-Squad Game and Tournament Attendance'):
                    st.plotly_chart(fig_intra_tour, use_container_width=True)
                    st.markdown("""
                            <p style='text-align: center;'>
                                Intra-Squad Games were created to compensate for Tournaments (mostly abroad) that were no longer attendable due to sanctions, 
                                financial issues connected with the Ruble losing its value, administrative issues with visas to European countries and etc. 
                                Eventually becoming our most attended type of event. 
                            </p>
                        """, unsafe_allow_html=True)
            
                




###################################################################################
 
        ##filler for spacing
        st.markdown("<br><br>", unsafe_allow_html=True)

#############################################################









        container = st.container(border=True)  
        with container:
            st.write("<h3 style='text-align: center;'>Total and Avg Attendance per Type</h3>", unsafe_allow_html=True)

            # Calculate total attendance per event type
            total_attendance_per_type = df_att.groupby('Type')['Attendance'].sum()

            # Sort the total attendance per event type in descending order
            total_attendance_per_type = total_attendance_per_type.sort_values(ascending=True) 

            # Calculate average attendance per event type
            average_attendance_per_type = df_att.groupby('Type')['Attendance'].mean()

            # Sort the average attendance per event type based on the total attendance order
            average_attendance_per_type = average_attendance_per_type.loc[total_attendance_per_type.index]


            fig_att_type = go.Figure()



#######################################################
############### Attendance per type ###################

            # Add a horizontal bar chart
            fig_att_type.add_trace(go.Bar(
                x=total_attendance_per_type.values,  # Total attendance values
                y=total_attendance_per_type.index,   # Event types
                text=total_attendance_per_type.values,
                textposition='auto',
                textfont=dict(size=16, color='black'),
                orientation='h',                    # Horizontal orientation
                marker=dict(color='skyblue'),
                name='Attendance by Type'       # Bar color
            ))


            # Add a line chart for average attendance per event type
            fig_att_type.add_trace(go.Scatter(
                x=average_attendance_per_type.values,  # Average attendance values
                y=average_attendance_per_type.index,   # Event types
                mode='lines+markers+text',
                name='Average Attendance',            # Line chart name
                marker=dict(color='red', size=10),
                text=average_attendance_per_type.round(1),
                textposition='top center',
                textfont=dict(size=16, color='red'),
                line=dict(color='red'),            # Line color
                xaxis ='x2'
            ))



            fig_att_type.update_layout(
                
                xaxis=dict(showgrid=False, showticklabels=False, range=[0, 4700]),  # Adjust the x-axis range
                yaxis=dict(showgrid=True),  
                height=800,  # Set the height of the chart
                bargap=0.1,  # Set the gap between bars
                legend=dict(x=.5, y=.3),
                xaxis2=dict(title=None, range=[0, 30], overlaying='x', side='bottom', showticklabels=False, showgrid=False),  # Adjust the second x-axis
            )


            # Display the plot
            st.plotly_chart(fig_att_type, use_container_width=True)

  
        #####################################################################
        ####################   interactive attendance chart   ##########################
        container = st.container(border=True)  
        with container:

            st.write("<h3 style='text-align: center;'>Event Type Attendance Per Year Interactive Chart</h3>", unsafe_allow_html=True)

            # Create a multiselect element for selecting event types
            selected_types = st.multiselect("Select Event Type ", df_att['Type'].unique(),label_visibility='collapsed')
        

            # Filter the DataFrame based on the selected event types
            filtered_data = df_att[df_att['Type'].isin(selected_types)]

            # Group by year and calculate total attendance per year
            total_attendance_per_year = filtered_data.groupby(['Year', 'Type'])['Attendance'].sum().reset_index()

            # Create an interactive line chart using Plotly Express
            fig_int_att = px.line(total_attendance_per_year, x='Year', y='Attendance', color='Type')
            fig_int_att.update_xaxes(type='category')  # Ensure the x-axis is treated as categorical (years)

            # Update layout to remove axis labels and tick marks
            fig_int_att.update_xaxes(title_text=None, showticklabels=True)
            fig_int_att.update_yaxes(title_text=None, showticklabels=True)

            # Display the chart in Streamlit
            st.plotly_chart(fig_int_att, use_container_width=True)



        ###########################################################
        ###################### histograms #########################
        container = st.container(border=True)  
        with container:
            st.write("<h3 style='text-align: center;'>Event Attendance Boxplots</h3>", unsafe_allow_html=True)



            
            # Multiselect element to select event types
            selected_types = st.multiselect('Select Event Type', df_att['Type'].unique(), key='multiselect')



            # Filter data based on selected event types
            filtered_data = df_att[df_att['Type'].isin(selected_types)]

            # Create an interactive boxplot chart using Plotly Express
            if not filtered_data.empty:
                fig_box = px.box(filtered_data, x='Type', y='Attendance', points="all")

                # Update layout to remove axis titles
                fig_box.update_xaxes(title_text=None, showticklabels=True)
                fig_box.update_yaxes(title_text='Attendance', showticklabels=True)

                # Set the chart width using the use_container_width function
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.warning("No data available for the selected event types.")
        


        
        st.write("<h3 style='text-align: center;'>Conclusions</h3>", unsafe_allow_html=True)





                   ############################################################################
###################################################################################
 
        ##filler for spacing
        st.markdown("<br>", unsafe_allow_html=True)

#############################################################
        #############################################################################



























       
    elif selected_subsection == "Player Stats": 

        # Filter the DataFrame for 'Team Practice'
        team_practice_df = df_att[df_att['Type'] == 'Team Practice']
        team_practice_count = len(team_practice_df)
        

        # Explode and count attendees
        team_practice_attendees = team_practice_df['Going'].str.split(', ').explode()
        team_practice_attendees_count = team_practice_attendees.value_counts()

        # Filter the DataFrame for 'Skills Practice'
        skills_practice_df = df_att[df_att['Type'] == 'Skills Practice']
        skills_practice_count = len(skills_practice_df)

        # Explode and count attendees
        skills_practice_attendees = skills_practice_df['Going'].str.split(', ').explode()
        skills_practice_attendees_count = skills_practice_attendees.value_counts()
        
    # Assuming you have the 'attendees_count' Series
        all_attendees = df_att['Going'].str.split(', ').explode()

        attendees_count = all_attendees.value_counts()

        # Get the top 7 attendees
        top_7_attendees_team = team_practice_attendees_count[:7]
        top_7_attendees_skills = skills_practice_attendees_count[:7]
        top_7_attendees = attendees_count[:7]

        


        
        st.write('<h2 style="text-align: center;">Top 7 Attendees</h2>', unsafe_allow_html=True)

           
 
        
        # Create the HTML content for the team practice column
        html_content_team = '''
        <div style="background-color: skyblue; border-radius: 5px; padding: 10px;">
            <h3 style="text-align: center;">Team Practices</h3>
        '''

        # Create the HTML content for the skills practice column
        html_content_skills = '''
        <div style="background-color: skyblue; border-radius: 5px; padding: 10px;">
            <h3 style="text-align: center;">Skills Practices</h3>
        '''

        # Create the HTML content for the overall column
        html_content_overall = '''
        <div style="background-color: skyblue; border-radius: 5px; padding: 10px;">
            <h3 style="text-align: center;">Overall</h3>
        '''



        # Iterate through the top team practice attendees and append them to the HTML content
        for i, (attendee, count) in enumerate(top_7_attendees_team.items(), start=1):
            html_content_team += f'<p style="text-align: center; font-weight: bold;">{i}. {attendee} ({count})</p>'

        # Iterate throuth the top skills practice attendees and append them the HTML content
        for i, (attendee, count) in enumerate(top_7_attendees_skills.items(), start=1):
            html_content_skills += f'<p style="text-align: center; font-weight: bold;">{i}. {attendee} ({count})</p>'

        # Iterate through the top overall attendees and append them to the HTML content
        for i, (attendee, count) in enumerate(top_7_attendees.items(), start=1):
            html_content_overall += f'<p style="text-align: center; font-weight: bold;">{i}. {attendee} ({count})</p>'



        # Close the HTML div tag
        html_content_team += '</div>'
        html_content_skills += '</div>'
        html_content_overall += '</div>'

        # Create the 3 column layout for top 5 lists
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(html_content_team, unsafe_allow_html=True)

        with col2:
            st.markdown(html_content_skills, unsafe_allow_html=True)
            
        with col3:
            st.markdown(html_content_overall, unsafe_allow_html=True)















#############################################################################
#############################################################################
 
        ##filler for spacing
        st.markdown("<br><br>", unsafe_allow_html=True)

#############################################################################
#############################################################################















        container = st.container(border=True)  
        with container:    
            st.write('<h2 style="text-align: center;">Individual Attendance Data</h2>', unsafe_allow_html=True)


            
            all_attendees = df_att['Going'].str.split(', ').explode()
            filtered_attendees = [attendee for attendee in all_attendees if attendee != "No Data" and len(attendee.split()) <= 3]
            unique_attendees = sorted(list(set(filtered_attendees))) 


            

            # Dropdown menu to select an attendee's name
            selected_name = st.selectbox("Select an Attendee", unique_attendees)



            if selected_name:
                # Filter data for the selected attendee
                attendee_data = df_att[df_att['Going'].str.contains(selected_name)]

                # Function to calculate the percentage of events attended by each attendee
                def calculate_percentage_attended(df, selected_attendee):
                    total_events = df.shape[0]
                    events_attended = df[df['Going'].str.contains(selected_attendee, case=False)].shape[0]
                    return (events_attended / total_events) * 100 if total_events > 0 else 0
                
                # Calculate the percentage of events attended by each attendee
                df_percentage_attended = pd.DataFrame(columns=['Attendee', 'Percentage'])
                df_percentage_attended['Attendee'] = unique_attendees
                df_percentage_attended['Percentage'] = df_percentage_attended['Attendee'].apply(
                    lambda x: calculate_percentage_attended(df_att, x))


                # Calculate metrics
                total_team_practices_attended = attendee_data[attendee_data['Type'] == 'Team Practice'].shape[0]
                total_skills_practices_attended = attendee_data[attendee_data['Type'] == 'Skills Practice'].shape[0]
                total_events_attended = attendee_data.shape[0]
                first_event_date = attendee_data['Date_Date_Excel'].min()
                last_event_date = attendee_data['Date_Date_Excel'].max()

                # Calculate the number of months between the first and last event
                months_attended = max((last_event_date - first_event_date).days / 30, 1)
                avg_events_per_month = total_events_attended / months_attended if months_attended != 0 else total_events_attended

                # Create a DataFrame to store average events per month for each attendee
                attendees_avg_events = pd.DataFrame(columns=['Attendee', 'AvgEventsPerMonth'])

                

                # Format first and last event dates to the desired format
                formatted_first_date = first_event_date.strftime("%b %d, %Y")
                formatted_last_date = last_event_date.strftime("%b %d, %Y")

                # Compute rankings for different event types based on attendance count
                df_team_practices = df_att[df_att['Type'] == 'Team Practice']
                df_skills_practices = df_att[df_att['Type'] == 'Skills Practice']
                df_total_events = df_att.copy()  # Create a copy of the original DataFrame
                # Sort the DataFrame by percentage in descending order to assign ranks
                df_percentage_attended = df_percentage_attended.sort_values(by='Percentage', ascending=False)
                df_percentage_attended['Rank'] = df_percentage_attended['Percentage'].rank(ascending=False, method='min')


                                    
                
                total_events_ranks = df_total_events['Going'].str.split(', ').explode().value_counts().rank(ascending=False, method='min')
                team_practices_ranks = df_team_practices['Going'].str.split(', ').explode().value_counts().rank(ascending=False, method='min')
                skills_practices_ranks = df_skills_practices['Going'].str.split(', ').explode().value_counts().rank(ascending=False, method='min')
            
                rank_total_events = total_events_ranks[selected_name] if selected_name in total_events_ranks else None
                rank_team_practices = team_practices_ranks[selected_name] if selected_name in team_practices_ranks else None
                rank_skills_practices = skills_practices_ranks[selected_name] if selected_name in skills_practices_ranks else None
                rank_percentage_attended = df_percentage_attended[df_percentage_attended['Attendee'] == selected_name]['Rank'].values[0]
                



                
                # Function to convert a duration string to minutes
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
                
                # Filter the DataFrame to select rows where the selected_name is in the "Going" column
                selected_name_events = df_att[df_att['Going'].str.contains(selected_name, case=False)]

                # Sample duration values from the filtered DataFrame
                selected_name_durations = selected_name_events['Duration']

                # Convert the duration strings to minutes and sum them
                total_player_minutes = sum([convert_duration_to_minutes(duration) for duration in selected_name_durations])

                # Convert the total minutes back to hours and minutes
                total_player_hours = total_player_minutes // 60
                remaining_player_minutes = total_player_minutes % 60

                # Create a dictionary to store minutes attended by each attendee
                attendees_minutes = {}

                # Loop through unique attendees to calculate their total time spent at events
                for attendee in unique_attendees:
                    attendee_events = df_att[df_att['Going'].str.contains(attendee, case=False)]
                    attendee_durations = attendee_events['Duration']
                    total_player_minutes = sum([convert_duration_to_minutes(duration) for duration in attendee_durations])
                    attendees_minutes[attendee] = total_player_minutes


                # Sort attendees by the total minutes attended in descending order to get ranks
                ranked_attendees = sorted(attendees_minutes.items(), key=lambda x: x[1], reverse=True)

                # Get the rank for the selected attendee
                rank_selected_name = [rank for rank, (name, _) in enumerate(ranked_attendees, 1) if name.lower() == selected_name.lower()]


                # Display metrics with formatted dates and rankings
                st.markdown(
                    f"""
                    <div style='text-align: center;'>
                        <h3 style='margin-bottom: 0;'>Attendance Ranks and Stats for {selected_name}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                
                #st.write(f"Total Team Practices Attended: {total_team_practices_attended}, # {int(rank_team_practices) if rank_team_practices else 'N/A'}")
                #st.write(f"Total Skills Practices Attended: {total_skills_practices_attended}, # {int(rank_skills_practices) if rank_skills_practices else 'N/A'}")
                #st.write(f"Total Events Attended: {total_events_attended}, # {int(rank_total_events) if rank_total_events else 'N/A'}")
                #st.write(f"Percentage of All Events Attended by {selected_name}: {total_events_attended / df_att.shape[0] * 100:.2f}%, # {int(rank_percentage_attended)}")
                #st.write(f"Date of First Event Attended: {formatted_first_date}")
                #st.write(f"Date of Last Event Attended: {formatted_last_date}")
                #st.write(f"Average Events Attended per Month: {avg_events_per_month:.2f}")
                #st.write(f"Time spent at events: {total_hours} hr {remaining_minutes} min | # {rank_selected_name[0]}" if rank_selected_name else f"Time spent by {selected_name} at events: {total_hours} hr {remaining_minutes} min | No rank found for {selected_name}")
                







                col1, col2, col3 = st.columns(3)
                
            
                with col1:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>First Event Attended</span>
                            </div>
                            <p style='font-size: 30px;'>{formatted_first_date}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>Avg Events Attended per Month</span>
                            </div>
                            <p style='font-size: 30px;'>{avg_events_per_month:.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>Last Event Attended</span>
                            </div>
                            <p style='font-size: 30px;'>{formatted_last_date}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                



            

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>Team Practices Attended</span>
                            </div>
                            <p style='font-size: 30px;'># {int(rank_team_practices) if rank_team_practices else 'N/A'}  ({total_team_practices_attended})</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    percentage_attended_team = total_team_practices_attended / 381 * 100

                    # Create the gauge chart for team practices attended
                    fig_team_practices = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value = percentage_attended_team,
                        title={'text': "Percentage of Team Practices Attended"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkgreen"},
                            'steps': [
                                {'range': [0, 25], 'color': "lightgray"},
                                {'range': [25, 50], 'color': "lightblue"},
                                {'range': [50, 75], 'color': "skyblue"},
                                {'range': [75, 100], 'color': "steelblue"}
                            ],
                        },
                        number={
                            'suffix': "%",
                            'font': {'size': 50}
                        }
                    ))

                    # Display the centered gauge chart in Streamlit using plotly_chart with use_container_width=True
                    
                    with st.expander('Expand'):
                        st.plotly_chart(fig_team_practices, use_container_width=True)
                    
                    
                    
                    


















                with col2:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>Skills Practices Attended</span>
                            </div>
                            <p style='font-size: 30px;'># {int(rank_skills_practices) if rank_skills_practices else 'N/A'}  ({total_skills_practices_attended})</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    percentage_attended_skills = total_skills_practices_attended / skills_practice_count * 100

                    # Create the gauge chart for skills practices attended
                    fig_skills_practices = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=percentage_attended_skills,
                        title={'text': "Percentage of Skills Practices Attended"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkgreen"},
                            'steps': [
                                {'range': [0, 25], 'color': "lightgray"},
                                {'range': [25, 50], 'color': "lightblue"},
                                {'range': [50, 75], 'color': "skyblue"},
                                {'range': [75, 100], 'color': "steelblue"}
                            ],
                        },
                        number={
                            'suffix': "%",
                            'font': {'size': 50}
                        }
                    ))

                    # Display the centered gauge chart in Streamlit using plotly_chart with use_container_width=True
                    with st.expander('Expand'):
                        st.plotly_chart(fig_skills_practices, use_container_width=True)

                    
                        















                col4, col5 = st.columns(2)

                with col4:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>All Events Attended</span>
                            </div>
                            <p style='font-size: 30px;'># {int(rank_total_events) if rank_total_events else 'N/A'}  ({total_events_attended})</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    percentage_attended = total_events_attended / df_att.shape[0] * 100
                    fig_total_events = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value=percentage_attended,
                        title={'text': "Percent of all Events Attended"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkgreen"},
                            'steps' : [
                                {'range': [0, 25], 'color': "lightgray"},
                                {'range': [25, 50], 'color': "lightblue"},
                                {'range': [50, 75], 'color': "skyblue"},
                                {'range': [75, 100], 'color': "steelblue"}
                            ],
                        },
                        number={
                            'suffix': "%",
                            'font': {'size': 50}
                        }
                    ))

                    # Display the gauge chart in Streamlit
                    with st.expander('Expand'):
                        st.plotly_chart(fig_total_events, use_container_width=True)

                    

                    
        
                with col5:
                    st.markdown(
                        f"""
                        <div style='text-align: center;'>
                            <div style='background-color: skyblue; border-radius: 10px; padding: 10px;'>
                                <span style='font-size: 16px; font-weight: bold;'>Time spent at events</span>
                            </div>
                            <p style='font-size: 30px;'># {rank_selected_name[0] if rank_selected_name else 'N/A'}  ({total_player_hours} hr {remaining_player_minutes} min)</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Calculate the percentage of total time spent at events
                    percentage_time_spent = (total_player_hours / total_hours) * 100

                    # Create the gauge chart for time spent at events
                    fig_time_spent = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=percentage_time_spent,
                        title={'text': "Percent of all events"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkgreen"},
                            'steps': [
                                {'range': [0, 25], 'color': "lightgray"},
                                {'range': [25, 50], 'color': "lightblue"},
                                {'range': [50, 75], 'color': "skyblue"},
                                {'range': [75, 100], 'color': "steelblue"}
                            ],
                        },
                        number={
                            'suffix': "%",
                            'font': {'size': 50}
                        }
                    ))

                    # Display the gauge chart in Streamlit
                    with st.expander('Expand'):
                        st.plotly_chart(fig_time_spent, use_container_width=True)

                


                

              









        


       









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

