from bs4 import BeautifulSoup
import requests
import pandas as pd
Imports
BeautifulSoup: A library for parsing HTML and XML documents, allowing for easy data extraction from web pages.
requests: A library for making HTTP requests to retrieve web content.
pandas: A powerful data manipulation and analysis library that provides data structures for efficiently storing and manipulating large datasets.
python
Copy code
def lookingForJob(JobTypeLink):
Function Definition
lookingForJob: A function that accepts a URL (string) as input to scrape job listings from Wuzzuf based on the specified search criteria.
python
Copy code
    page = 0
    all_job_titles = []
    daytime = []
    all_companies = []
    all_locations = []
    all_skills = []
    all_links = []
Variables Initialization
page: An integer to track the current page number being scraped.
all_job_titles, daytime, all_companies, all_locations, all_skills, all_links: Lists to store the accumulated job data for titles, posting dates, company names, locations, required skills, and application links, respectively.
python
Copy code
    while True:
Infinite Loop
The loop continues until explicitly broken, allowing for scraping multiple pages of job listings.
python
Copy code
        url = f'{JobTypeLink}{page}'
        pag1 = requests.get(url)
Fetching Web Page
url: Constructs the complete URL for the current page by appending the page number to the input link.
pag1: Sends an HTTP GET request to retrieve the page content.
python
Copy code
        if pag1.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {pag1.status_code}")
            break
Error Handling
Checks if the HTTP request was successful (status code 200). If not, it prints an error message and exits the loop.
python
Copy code
        soup = BeautifulSoup(pag1.content, 'html.parser')
Parsing HTML
soup: Parses the HTML content of the page using BeautifulSoup, creating a BeautifulSoup object for data extraction.
python
Copy code
        jobTit = soup.find_all('h2', {'class': 'css-m604qf'})
        jobtitle = [job.text.strip() for job in jobTit]
Extracting Job Titles
jobTit: Finds all <h2> elements with the specified class, which contain job titles.
jobtitle: Extracts and cleans the text from each job title element.
python
Copy code
        da = soup.find_all('div', {'class': 'css-4c4ojb'})
        day1 = [job.text.strip() for job in da]
        da1 = soup.find_all('div', {'class': 'css-do6t5g'})
        day2 = [job.text.strip() for job in da1]
        dayy = day1 + day2  # Combine both lists into a single list
Extracting Days Since Posted
da: Finds elements with the class containing the days since posting.
day1 and day2: Extracts and cleans the text for two different elements that may contain posting times.
dayy: Combines both lists into a single list of posting times.
python
Copy code
        co_ = soup.find_all('a', {'class': 'css-17s97q8'})
        Company = [l.text.strip() for l in co_]
Extracting Company Names
co_: Finds all <a> elements with the specified class, which contain company names.
Company: Extracts and cleans the text for each company name.
python
Copy code
        loc_ = soup.find_all('span', {'class': 'css-5wys0k'})
        location = [l.text.strip() for l in loc_]
Extracting Locations
loc_: Finds all <span> elements with the specified class, which contain location information.
location: Extracts and cleans the text for each location.
python
Copy code
        skil_ = soup.find_all('div', {'class': 'css-y4udm8'})
        skills = [l.text.strip() for l in skil_]
Extracting Required Skills
skil_: Finds all <div> elements with the specified class, which contain required skills for the jobs.
skills: Extracts and cleans the text for each required skill.
python
Copy code
        links = ['https://wuzzuf.net' + job.find('a')['href'] for job in jobTit]
Extracting Application Links
links: Constructs the full application URLs by finding the <a> tags within the job title elements.
python
Copy code
        all_job_titles.extend(jobtitle)
        all_companies.extend(Company)
        all_locations.extend(location)
        all_skills.extend(skills)
        all_links.extend(links)
        daytime.extend(dayy)
Accumulating Data
Appends the extracted data from the current page to the respective lists that store all job listings.
python
Copy code
        page += 1
Incrementing Page Number
Increases the page counter to move to the next set of job listings.
python
Copy code
        try:
            pageCount = int(soup.find('strong').text.strip())
            pagelimi = (pageCount // 15) + 1  # Adjust for 0-based index
        except Exception as e:
            print(f"Error fetching total job count: {e}. Exiting...")
            break
Fetching Total Job Count
Attempts to find the total number of job listings on the current page and calculates how many pages to scrape. If it encounters an error, it prints a message and exits.
python
Copy code
        if page >= pagelimi:  # Use >= to include the last page
            break
Page Limit Check
Stops the loop if the current page number exceeds the calculated page limit.
python
Copy code
    df = pd.DataFrame({
        'JobTitle': all_job_titles,
        'Company': all_companies,
        'Location': all_locations,
        'Skills': all_skills,
        'Links': all_links,
        'Period': daytime
    })
Creating DataFrame
Constructs a pandas DataFrame from the accumulated lists, organizing the job data into a structured format.
python
Copy code
    df.to_csv(r'C:\Users\Ahmed Hassan\Documents\python for beginner\csvFiles\wuzzufPython.csv', mode='w', index=False)
Saving to CSV
Saves the DataFrame to a CSV file at the specified path, allowing for easy access and analysis of the job listings.
python
Copy code
    return 'Successfully, the file was created.'
Function Return
Returns a success message indicating that the CSV file was created successfully.
python
Copy code
JobTypeLink = input('Enter Wuzzuf job link similar to this (e.g., https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=data%20analysis&start=): ')
print(lookingForJob(JobTypeLink))
User Input and Function Call
Prompts the user to enter a Wuzzuf job search link and calls the lookingForJob function with the provided URL, displaying the success message.
Summary
This code provides a structured approach to scraping job listings from the Wuzzuf website, focusing on key job-related information and saving it in a CSV format. It demonstrates practical web scraping techniques, error handling, and data manipulation using Python.
