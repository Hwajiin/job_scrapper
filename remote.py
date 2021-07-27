import requests
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


URL = "https://remoteok.io/remote-dev+python-jobs"


def remote_get_jobs(term):
  job_list = []
  r = requests.get(f"https://remoteok.io/remote-dev+{term}-jobs", headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  table = soup.find('table', {'id': 'jobsboard'})
  trs = table.find_all('tr', {'class': 'job'})
  for tr in trs:
    url = tr.attrs['data-url']
    link = "https://remoteok.io" + url
    company = tr.attrs['data-company']
    title = tr.find('h2', {'itemprop': 'title'}).get_text()
    job_list.append({'title': title, 'company': company, 'link': link })
  return job_list
    