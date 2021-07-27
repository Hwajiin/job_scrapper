import requests
from bs4 import BeautifulSoup

URL = "https://weworkremotely.com/remote-jobs/search?term=python"

def wework_get_jobs(term):
  job_list = []
  r = requests.get(f"https://weworkremotely.com/remote-jobs/search?term={term}")
  soup = BeautifulSoup(r.text, 'html.parser')
  lis = soup.find_all('li', {'class': 'feature'})
  for li in lis:
    title = li.find('span', {'class': 'title'}).get_text()
    company = li.find('span', {'class': 'company'}).get_text()
    url = li.find_all('a')[1]['href']
    link = "https://weworkremotely.com" + url
    job_list.append({'title': title,'company': company, 'link': link})
  return job_list