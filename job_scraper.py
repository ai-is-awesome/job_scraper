def get_soup(url):
    import requests
    from bs4 import BeautifulSoup
    resp = requests.get(url)
    text = resp.text
    soup = BeautifulSoup(text, 'lxml')
    return soup
    


def get_indeed_job_details(soup):
    card_class = 'jobsearch-SerpJobCard unifiedRow row result'
    
    job_details_dict = {'title' : [], 'salary' : [], 'company' : [], 'location' : [], 'description' : []}
    
    for job_detail in soup.find_all('div', class_ = card_class):
        title = job_detail.find('h2' , class_ = 'title')
        title = title.a.get('title')
        
        company = get_text_or_tag(job_detail.find('span', class_ = 'company'))
        
        location = (job_detail.find('div', class_ = 'recJobLoc').get('data-rc-loc'))
        
        salary = get_text_or_tag(job_detail.find('span', class_ = 'salaryText'))
        
        description = get_text_or_tag(job_detail.find('div', class_ = 'summary'))
        job_details_dict['title'].append(title)
        job_details_dict['salary'].append(salary)
        job_details_dict['company'].append(company)
        job_details_dict['location'].append(location)
        job_details_dict['description'].append(description)
        
    return job_details_dict




def query_formatter(query):
    return query.replace(' ', '+')


def get_text_or_tag(tag):
    if tag == None:
        return None
    else:
        return tag.text





def main():
    import time
    import datetime
    import pandas as pd
    
    country = input('Search jobs in India(y/n): ')
    if country.lower() == 'n':
        home_page_url = input('Enter the indeed url manually of the country you want to scrape jobs from:\nFor example for jobs in uk\
        type https://www.indeed.co.uk/')

        url = home_page_url + 'jobs?q=%s&start=%s&l=%s'

    
    query = query_formatter(input('Enter the job you want to search on indeed: '))
    location = input('Enter the city/state in which you want to search the job on indeed, hit enter to skip: ')
        
    while True:
        try:
            num_pages = int(input('Enter the number of pages you want to scrape the data for?: '))
        
        except:
            print('Invalid response, input must be an integer')
        
        else:
            break
        

    
    
    all_pages_details = {}
    
    start = 0
    print('Location is %s' % (location))
    for i in range(1, num_pages + 1):
        
        if country == 'y':
            url = 'https://www.indeed.co.in/jobs?q=%s&start=%s&l=%s'
            
        else:
            url = home_page_url + 'jobs?q=%s&start=%s&l=%s'
        url = url % (query, start, location)
        print('Scraping url:', url)
        
        soup = get_soup(url)
#         resp = requests.get(url)
#         soup = BeautifulSoup(resp.text, 'lxml')
        details = get_indeed_job_details(soup)
        for key, item in details.items():
            if not key in all_pages_details:
                all_pages_details[key] = item
            
            else:
                all_pages_details[key] =all_pages_details[key] + item
                
                     
                     
        start += 10
        print(f'{i} pages scraped.')
        time.sleep(2)
        
    
    
    current_dt = datetime.datetime.now()
    date_format = current_dt.strftime('%d') + current_dt.strftime('%B') + current_dt.strftime('%Y')
    file_name = f'{query}_{location}_{date_format}'
    df.to_excel('%s.xlsx' % (file_name))
    print(f'Scraped jobs for "{query}" and saved in file {file_name}')
    return pd.DataFrame(all_pages_details)


      
        
#     inp = query_formatter(query)
#     resp = requests.get(url % inp)
#     print('Scraping URL: %s' % (url % inp))
#     soup = BeautifulSoup(resp.text, 'lxml')
#     details = get_indeed_job_details(soup)
#     df = pd.DataFrame(details)
    
#     current_dt = datetime.datetime.now()
    
#     file_name = query + ' ' + 'indeed' + ' ' + current_dt.strftime('%d') + current_dt.strftime('%B') + current_dt.strftime('%Y')
    
#     df.to_excel('%s.xlsx' % (file_name))
#     print('CSV file: %s written successfully...' % (file_name))
#     return df














