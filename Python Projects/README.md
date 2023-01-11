# Facebook group past events attenedance scraper
  - This is a scraper that I built to get attendance data from past events in a group I manage. The given Facebook API does not give this information, 
    therefore I decided to build a scraper to extract that data.
## Considerations
  - Facebook restrictions restrict button (functions) access to a certain number per day (about 150), therefore the 1866 links to events that were gathered must be split up into 
    multiple queries. i.e. If there are 1866 links, the numbers in [#:#] need to be adjusted or the time between server requests.
    In this case, it is easier to split the requests over the span of two weeks. 
  - Some unnecessary data was gathered such as some comments on posts that had the same "span" marker in the given link. 
    The logic was that it would save time. Trying to find and write and test the correct code to exempt unnecessary data took more time, because it would be faster to just clean the data after extracting.
  - Some modules were downloaded but not used in the final version. I have left them as part of the code for future flexibility and revisions. 
