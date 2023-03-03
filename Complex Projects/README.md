# Moscow Lacrosse Club Team Fund (In Process)
Ths project set out to write the history, growth, and development of the Moscow Lacrosse Team through their team fund finances over time. Additionally, attendance data and growth data was complied over the whole history of the club.
## Tools Used
- Google Sheets
- Personal Knowledge of Russian
- Python
- Excel, Powerpoint
- R Studio
- Power BI
## Background Information
The data used was complied from three separate sources (fund ledger, facebook events, world lacrosse grant schedule). The Facebook events provide the exact dates of the events as well as the attendance records, while the fund ledger is when that transaction was recorded, not necessarily the date it happened. Therefore the financial data should be looked at as a whole or over a period of time, and the facebook events are more time-accurate

Additionally, not everyone checked in to the facebook event all the time, so the attendance was actually about 20% higher than the actual number. 
All the fund ledger data, as well as some of the facebook data was in Russian, so that has to be translated to English before anything can be processed.
This Data is original and was complied over the course of a decade by me and my colleagues. 

* 1.0 Data Gathering steps and observations for financial data (Google Sheets, Excel)
  * 1.1 Data was taken from the team fund google sheet and was extracted to my personal hard drive as an excel file for further manipulation. The source data is still on Google Sheets.
  * 1.2 All of the data is in one file in separate sheets (tables), and the columns evolved over time as the ledger evolved, so the columns must be standardized.  
  * 1.3 Some of the data is missing. Ex. Dates were recorded only from late 2017, so those will have to be filled in
  * 1.4 The Ledger started in 2015 but the practices started in 2013
 
 * 2.0 Cleaning the Financial data (Excel)
   * 2.1 To standardize the data, columns from the most recent ledger table were copied into the tables from the past (the most recent column titles were copied onto the tables), new columns were created as necessary. 
    * 2.1.1 Nomenclature in columns that categorize data (transaction type, date) were standardized for better organization of data and transactions, as well as to make translating easier down the line. Ex: "helmet sale" was categorized as "equipment sale", but "helmet sale" was added to an information column that defined the transaction.
    * 2.1.2 A column for transaction category was created (income, expense, income usd, expense usd) to separate each separate account that was used
   * 2.2 Missing data was filled in 
    *  2.2.1 Dates were filled in the ledger by cross referencing bank statements and events
    *  2.2.2 New columns were created to identifiy the transaction type (income, expense, etc).
   * 2.3 rows were inspected one by one for consistency and correctness. Some rows were split as there were multiple transactions summed in one cell
   * 2.4 Language/words were standardized in Russian, English words in the Russian data were deliberately left because the data was to be translated anyway, information about the transaction was added where needed.
   * 2.5 Categories for each column were simplified and consolidated and categorized
   * 2.6 "Union All" tables into one sheet in Excel
   * 2.7 The final Excel data sheet was sent to colleagues for accuracy and validity inspection
 
 * 3.0 Translating Financial Data from Russian to English (Excel)
   * 3.1 All standardized titles/categories were translated into English using the Find command in excel
   * 3.2 Individual records had comments with no standardization, therefore they had to be translated one by one manually
  
 * 4.0 Scraping Attendance Records from FB Private group (Python)
     * 4.1 All attendance records were kept in facebook using their attendance recording system (going, maybe, can't go). There is no way to fetch the data through an api, nor is it efficient to download a csv with missing data from 1000+ events over 10+ years.
     * 4.2 A scraping bot was created to fetch the data and store it automatically from all events in the private group
      * 4.2.1 Data that was needed: name of event, date and time of event, location of event, people that replied with "going", duration of event, creator of event.
      * 4.2.2 Main coding obstacles incurred for fetching data:
        * 4.2.2.1 log in directly to the group page with no notification popups
        * 4.2.2.2 "see more" button pressing loop for showing all events in the group history and scrolling down to the bottom automatically 
        * 4.2.2.3 opening and closing consecutive pages while gathering data on those pages
        * 4.2.2.4 set pauses between requests to allow for more loading time so that all elements are loaded
        * 4.2.2.5 open a pop up window inside the target url and count "going" attendees
        * 4.2.2.6 gathering data into a .csv and storing data until no events are left on the page
        * 4.2.2.7 facebook function limits ("see more" scrolling button, attendance button)
      * 4.2.3 Due to facebook restrictions, scraping had to be split into multiple days with output stored in seperate files
        * 4.2.3.1 Links to each event were extracted (1866 links). Restrictions allow scraping of about 150 links per day.
        * 4.2.3.2 restrictions on activating certain functions stated above causes the scraping time to increase since one function restriction can cripple the whole process
      * 4.2.4 Due to above issues, a second version of the script was written to record all links into a .csv, therefore avoiding at least the "see more" button function restriction
        * 4.2.4.1 the script does the same task as the first version, but instead of recalling links from the script memory, the links are reacalled from a csv list
        
 * 5.0 Cleaning the Attendance data (Excel)
      * 5.1 Changed patterns of unknown symbols into russian letters and words that were not copied correctly from Facebook
      * 5.2 Noticed that the time of the event corresponded to the time zone I am in currently, not the time zone I was in during the event, therefore the data needs to be rescraped
      
 * 6.0 Analysis of Financial Data (R Studio)
 * 7.0 Analysis of Attendance Data (R Studio)
 * 8.0 Visualization of Financial Data (Power BI)
 * 9.0 Visualization of Attendance Data (Power BI)
 * 10.0 Cross-referencing information with colleagues 
 * 11.0 Presentation of Compiled Data (Powerpoint)
  
   
 
      





