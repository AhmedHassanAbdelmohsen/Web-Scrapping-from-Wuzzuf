from bs4 import BeautifulSoup
import requests
import pandas as pd

def lookingForJob(JobTypeLink):
    page = 0
    all_job_titles = []
    daytime = []
    all_companies = []
    all_locations = []
    all_skills = []
    all_links = []

    while True:
        # Fetch the page with the current page number
        url = f'{JobTypeLink}{page}'
        pag1 = requests.get(url)

        # Check if the request was successful
        if pag1.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {pag1.status_code}")
            break

        soup = BeautifulSoup(pag1.content, 'html.parser')

        # Extract job titles
        jobTit = soup.find_all('h2', {'class': 'css-m604qf'})
        jobtitle = [job.text.strip() for job in jobTit]

        # Extract days since posted
        da = soup.find_all('div', {'class': 'css-4c4ojb'})
        day1 = [job.text.strip() for job in da]
        da1 = soup.find_all('div', {'class': 'css-do6t5g'})
        day2 = [job.text.strip() for job in da1]
        dayy = day1 + day2  # Combine both lists into a single list

        # Extract company names
        co_ = soup.find_all('a', {'class': 'css-17s97q8'})
        Company = [l.text.strip() for l in co_]

        # Extract locations
        loc_ = soup.find_all('span', {'class': 'css-5wys0k'})
        location = [l.text.strip() for l in loc_]

        # Extract skills
        skil_ = soup.find_all('div', {'class': 'css-y4udm8'})
        skills = [l.text.strip() for l in skil_]

        # Extract job links
        links = ['https://wuzzuf.net' + job.find('a')['href'] for job in jobTit]

        # Append current page data to the accumulated lists
        all_job_titles.extend(jobtitle)
        all_companies.extend(Company)
        all_locations.extend(location)
        all_skills.extend(skills)
        all_links.extend(links)
        daytime.extend(dayy)

        # Increment page number for next iteration
        page += 1

        # Find total number of jobs and calculate page limit
        try:
            pageCount = int(soup.find('strong').text.strip())
            pagelimi = (pageCount // 15) + 1  # Adjust for 0-based index
        except Exception as e:
            print(f"Error fetching total job count: {e}. Exiting...")
            break

        # Stop when we've reached the last page
        if page >= pagelimi:  # Use >= to include the last page
            break

    # Create a DataFrame after all pages are scraped
    df = pd.DataFrame({
        'JobTitle': all_job_titles,
        'Period': daytime,
        'Company': all_companies,
        'Location': all_locations,
        'Skills': all_skills,
        'Links': all_links

    })

    # Save the DataFrame to a CSV file
    df.to_csv(r'C:\Users\Ahmed Hassan\Documents\python for begginer\csvFiles\wuzzufPython.csv', mode='w',
              index=False)
    return 'Successfully, the file was created.'

# Get the job type link from user input
JobTypeLink = input('Enter Wuzzuf job link similar to this (e.g., https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=data%20analysis&start=): ')
print(lookingForJob(JobTypeLink))
