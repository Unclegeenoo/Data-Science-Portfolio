# Moscow Lacrosse Club Team Fund
Ths project set out to write the history, growth, and development of the Moscow Lacrosse Team through their team fund finances over time. Additionally, attendance data and growth data was complied over the whole history of the club.
## Tools Used
Google Sheets
Google Translate/Personal Knowledge of Russian
Excel
R Studio
Power BI
## Background Information
The data used was complied from three separate sources (fund ledger, facebook events, world lacrosse grant schedule). The Facebook events provide the exact dates of the events as well as the attendance records, while the fund ledger is when that transaction was recorded, not necessarily the date it happened. Therefore the financial data should be looked at as a whole or over a period of time, and the facebook events are more time-accurate

Additionally, not everyone checked in to the facebook event all the time, so the attendance was actually about 20% higher than the actual number. 
All the fund ledger data, as well as some of the facebook data was in Russian, so that has to be translated to English before anything can be processed.
This Data is original and was complied over the course of a decade by me and my colleagues. 

* 1.0 Data Gathering steps and observations (Google Sheets, Excel)
  * 1.1 Data was taken from the team fund google sheet and was extracted to my personal hard drive as an excel file for further manipulation. The source data is still on Google Sheets.
  * 1.2 All of the data is in one file in separate sheets (tables), and the columns evolved over time as the ledger evolved, so the columns must be standardized.  
  * 1.3  Some of the data is missing. Ex. Dates were recorded only from late 2017, so those will have to be filled in
  * 1.4  The Ledger started in 2015 but the practices started in 2013
 
 * 2.0 Cleaning/Filling the data (Excel)
   * 2.1 To standardize the data, columns from the most recent ledger table were copied into the tables from the past, new columns were created as necessary. 
    * 2.1.1 Nomenclature in columns that categorize data (transaction type, date) were standardized. Ex: "helmet sale" was categorized as "equipment sale", but "helmet sale" was added to an information column.
    * 2.1.2 A column for transaction category was created (income, expense, income usd, expense usd)
   * 2.2 Missing data was filled in
    *  2.2.1 Dates were filled in the ledger by cross referencing bank statements and events
    *  2.2.2 New columns were created to identifiy the transaction type (income, expense, etc).
   * 2.3 rows were inspected one by one for consistency and correctness. Some rows were split as there were multiple transactions summed in one cell
   * 2.4 Language/words were standardized in Russian, English words in the Russian data were deliberately left because the data was to be translated anyway, information about the transaction was added where needed.
   
 
      





