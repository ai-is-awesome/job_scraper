import requests
from bs4 import BeautifulSoup



def get_indeed_url(country):
    pass






class IndeedQueryManager:
    origin_url = 'https://www.indeed.in/'


    def __init__(self, query = '', city = '', country = 'India', num_pages = 1):
        self.query = query
        self.country = country
        self.city = city
        self.num_pages = num_pages



    def get_urls_from_query(self):
        start = 0
        urls = list()

        for i in range(self.num_pages):
            url = f'https://www.indeed.co.in/jobs?q={self.query}&start={start}&l={self.city}'
            urls.append(url)
            start += 10

        return urls
    
    def set_query(self, query):
        self.query= query

    def set_city(self, city):
        self.city = city

    def set_country(self, country):
        self.country = country

    def set_num_pages(self, num_pages):
        self.num_pages = num_pages



class Request(object):

    max_tries = 5

    headers = {
    #'Host': 'www.amazon.in',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36', 
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
    'accept-language': 'en-US,en;q=0.9', 
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',

    }



    def __init__(self):
        return None



    def get(self, url):
        session = requests.session()
        resp = session.get(url, headers = self.headers)
        num_tries = 1
        while resp.status_code != 200 and  num_tries < self.max_tries:
            resp = session.get(url, headers=  self.headers)
            num_tries += 1

        if num_tries == self.max_tries:
            raise Exception("Max number of tries reached")

        return resp
            

    def post(self, url, data):

        session = requests.session()
        resp = session.post(data = data)
        return resp




class IndeedJobScraper(Request):
    origin_url = 'https://www.indeed.in'
    #query = IndeedQueryManager(query = '', city = '', country = 'India', num_pages = 1)


    def __init__(self, query):
        '''
        Input: IndeedQueryManager object


        Constructs the query. 

        '''
        self.query = query

    def get_text_or_tag(self, tag):
        if tag == None:
            return None
        else:
            return tag.text
    

    def get_soup(self, url = None):
        
        resp = self.get(url)
        text = resp.text
        soup = BeautifulSoup(text, 'lxml')
        return soup



    def get_details_from_job_container(self, soup):
        '''
        input: A job container containing all the text of a single Job box in indeed(beatufiul soup object)
        output: Dictionary with details of the Job
        '''
        
        results = {}
        title = soup.find('h2' , class_ = 'title')
        results['title'] = title.a.get('title')
        
        results['company'] = self.get_text_or_tag(soup.find('span', class_ = 'company'))
        
        results['location'] = (soup.find('div', class_ = 'recJobLoc').get('data-rc-loc'))
        
        results['salary'] = self.get_text_or_tag(soup.find('span', class_ = 'salaryText'))
        
        results['description'] = self.get_text_or_tag(soup.find('div', class_ = 'summary'))
        
        return results
        


    def get_indeed_job_details(self,):    
        urls_list = self.query.get_urls_from_query()
        jobs_list = []
        card_class = 'jobsearch-SerpJobCard unifiedRow row result'
        for url in urls_list:
            soup = self.get_soup(url)
            for job_detail in soup.find_all('div', class_ = card_class):
                jobs_list.append(self.get_details_from_job_container(job_detail))
                
            
        return jobs_list
            
    
    
        



    def query_formatter(query):
        return query.replace(' ', '+')







class IOOperations:
    '''
    For managing operations from JSON to CSV/Excel etc...

    '''
    pass