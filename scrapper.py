import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

def get_jobs_form_remoteok(word):
  url = f"https://remotive.io/api/remote-jobs?search={word}"
  request = requests.get(url, headers = headers)
  results = request.json()['jobs']
  jobs = []
  for result in results:
    title = result['title']
    company = result['company_name']
    link = result['url']
    job = {
        "title": title,
        "company": company,
        "link": link
    }
    jobs.append(job) 

  # soup = BeautifulSoup(request.text,'html.parser')
  # posts = soup.select('tbody > tr.job')
  # jobs = []
  # for post in posts:
  #   info = post.find("td", {"class": "company position company_and_position"})
  #   title = info.find("h3",{"itemprop": "name"}).string.strip()
  #   company = info.find("h2",{"itemprop": "title"}).string.strip()
  #   link_tail = info.find("a",{"itemprop": "url"})['href']
  #   link = "https://remoteok.io/" + link_tail
  #   job = {
  #       "title": title,
  #       "company": company,
  #       "link": link
  #   }
  #   jobs.append(job)
  return jobs

def get_jobs_form_weworkremotely(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  request = requests.get(url)
  soup = BeautifulSoup(request.text,'html.parser')
  sections = soup.find_all('section',{'class':'jobs'})
  posts = []
  for section in sections:
    lis = section.find_all('li')
    posts += lis[:-1]
  jobs = []
  for post in posts:
    title = post.find('span',{'class':'title'}).string.strip()
    company = post.select_one('span:nth-of-type(1)').string.strip()
    link_tail = post.find('a',recursive=False)['href']
    link = "https://weworkremotely.com/" + link_tail
    job = {
        "title": title,
        "company": company,
        "link": link
    }
    jobs.append(job)
  return jobs

def get_jobs_form_stackoverflow(word):
  url = f"https://stackoverflow.com/jobs?r=true&q={word}"
  request = requests.get(url)
  soup = BeautifulSoup(request.text,'html.parser')
  posts = soup.find_all('div', {"class": "-job"})
  jobs = []
  for post in posts:
    title = post.find("h2", {"class": "mb4"}).find("a")['title']
    company_html = post.find("h3", {"class": "mb4"}).find("span", recursive=False)
    try:
        company = company_html.string.strip()
    except:
        company_html.span.replace_with('////')
        company = company_html.get_text(strip=True).split('////')
    job_id = post['data-jobid']
    job = {
        "title": title,
        "company": company,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }
    jobs.append(job)
  return jobs


def get_total_jobs(word):
  total_jobs = []
  total_jobs += get_jobs_form_stackoverflow(word)
  total_jobs += get_jobs_form_weworkremotely(word)
  total_jobs += get_jobs_form_remoteok(word)
  return total_jobs