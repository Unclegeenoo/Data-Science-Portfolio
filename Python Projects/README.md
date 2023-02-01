# Facebook Group Past Events Attendance Scraper
  - This is a scraper that I built to get attendance data from past events in a group I manage. The given Facebook API does not give this information, 
    therefore I decided to build a scraper to extract that data.
## Considerations
  - Facebook restrictions restrict button (functions) access to a certain number per day (about 150), therefore the 1866 links to events that were gathered must be split up into 
    multiple queries. i.e. If there are 1866 links, the numbers in [#:#] need to be adjusted, or the time between server requests must be increased using "time.sleep(insert # of seconds here)".
    In this case, it is easier to either increase pause times between actions to multiple minutes or split the requests over multiple days. [0:150], [151:300], etc.
  - Some unnecessary data was gathered such as some comments on posts that had the same "span" marker in the given link. 
    The logic was that leaving that data instead of trying to code to exclude it would save time. Trying to find and write and test the correct code to exempt unnecessary data took more time, because it would be faster to just clean the data after extracting.
  - Some modules were downloaded but not used in the final version. I have left them as part of the code for future flexibility and revisions. 

## Versions
  - "**scraper_fb_final_github.ipynb**" : This version reveals all links and iterates through them one by one, with the links saved in the script memory.
  - "**scraper_fromcsv_tocsv.ipynb**" : This version saves all links to a csv file and iterates through them instead of relying on script memory. This was created because there are sometimes errors in the events and the scraper stops (foreign symbols, missing fields, etc), which cause the process to stop, losing all link data in the script memory. Therefore it made more sense to save all href links to a csv and access them from there. This allowed for going around the "see more" button frequency restriction, as well as the link memory problem (as stated above). 
