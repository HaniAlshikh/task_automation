import mechanicalsoup
import datetime
import os

STELLENWERK = 'https://www.stellenwerk-hamburg.de'


########## browse ##########
# initialize a new browser instance
browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
  )

# open jobs page and check for errors
login_page = browser.open("%s/jobboerse/privat?type=2" % STELLENWERK)
login_page.raise_for_status()

# returns bs4.BeautifulSoup object form the first page
jobs_page = browser.get_current_page()

# Testing with local file
# from bs4 import BeautifulSoup
# html_doc = open("./test1.html", "r")
# jobs_page = BeautifulSoup(html_doc, 'html.parser')

# select the jobs
jobs = jobs_page.select('div.views-row')
#############################


########## scrape and print ##########

def job_strings(job):
  strings = []
  for string in job.stripped_strings:
    strings.append(string)  
  return strings


cache_file = './cach.html'
if not os.path.isfile(cache_file):
  with open(cache_file, 'w'): pass

with open(cache_file) as file:
  cache = file.read()

first = True
for job in jobs:
  string = job_strings(job)
  # if the first job is the same job in the cache -> no new jobs
  # break if the first job matches the job in the cache
  if string[0] == str(cache):
    break
  # write only the first job to cache
  if first:
    with open(cache_file, 'w') as file:
      file.write(str(string[0]))
    first = False
  # write the jobs to stdout
  link = job.select_one('a') 
  print("%s%s" % (STELLENWERK, link['href']))
  print(*string, sep = "\n")
  print("-"*40)


#######################################