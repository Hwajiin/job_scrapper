import requests
from bs4 import BeautifulSoup


URL = "https://stackoverflow.com/jobs?r=true&q=java"

def so_find_last_page(term):
  r = requests.get(f"https://stackoverflow.com/jobs?r=true&q={term}")
  soup = BeautifulSoup(r.text, 'html.parser')
  pagination = soup.find('div', 's-pagination')
  last_page = pagination.find_all('span')[-2].get_text()
  return int(last_page)

def so_get_jobs(term, lastpage):
  job_list = []
  for num in range(lastpage):
    r = requests.get(f"https://stackoverflow.com/jobs?r=true&q={term}&pg={num}")
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.find_all('div', {'class': '-job'})
    for div in divs:
      h2 = div.find('h2', {'class' : 'mb4'})
      h3 = div.find('h3', {'class': 'mb4'})
      title = h2.a['title']
      url = h2.a['href']
      link = "https://stackoverflow.com" + url
      company = h3.find('span').get_text().strip()
      job_list.append({ 'title': title, 'company': company, 'link': link})
  return job_list

def so_search(term):
  last_page = so_find_last_page(term)
  datalist = so_get_jobs(term, last_page)
  return datalist