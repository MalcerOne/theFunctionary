# The Functionary RPA Framework challenge!
Your challenge is to automate the process of extracting data from the news site. Link to the news site: www.nytimes.com

# Setups
You must have 3 configured variables (you can save them in the configuration file, but it is better to put them to the Robocorp Cloud work items):<br>
- search phrase<br>
- news category or section<br>
- number of months for which you need to receive news<br>
  Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on<br><br>

# Main steps
1. Open the site by following the link
2. Enter a phrase in the search field
3. On the result page, apply the following filters:
    - select a news category or section
    - choose the latest news
4. Get the values: title, date, and description.
5. Store in an excel file:
    - title
    - date
    - description (if available)
    - picture filename
    - count of search phrases in the title and description
    - True or False, depending on whether the title or description contains any amount of money
        
        > Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        > 
6. Download the news picture and specify the file name in the excel file
7. Follow the steps 4-6 for all news that fall within the required time period
