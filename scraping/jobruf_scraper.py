#!/usr/bin/env python3
# 
# this script scraps Jobruf.de for new students jobs 
#
# written by Hani Alshikh
#
####################################################################

import mechanicalsoup
import datetime
import config

JOBRUF = 'https://www.jobruf.de'
USERNAME = config.jobruf['username']
PASSWORD = config.jobruf['password']


# initialize a new browser instance
browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
  )

# Uncomment for a more verbose output:
# browser.set_verbose(2)

# open the login page and check for errors
login_page = browser.open("%s/secure/login" % JOBRUF)
login_page.raise_for_status()

# Fill-in the login form
# select the form biased on a css selector
browser.select_form('form[action="/secure/login_check"]')
# display a summary of the form fields
# browser.form.print_summary()
browser['_username'] = USERNAME
browser['_password'] = PASSWORD
browser.submit_selected()

# apply the correct jobRuf filter for new jobs
filter = browser.select_form('form[action="/student/interessen/filter"]')
# values can be also changed like above (username and password)
filter.set_radio({'interests[order]': '0:2', 'interests[radius]': '25'})
# returns response code by default and .txt return html
browser.submit_selected()


# returns bs4.BeautifulSoup object
jobs_page = browser.get_current_page()

# Testing with local file
# from bs4 import BeautifulSoup
# html_doc = open("./test.html", "r")
# jobs_page = BeautifulSoup(html_doc, 'html.parser')


# filter only the jobs section from the page
jobs = jobs_page.select('.results > ul.jobruf-list > li')


# itreate through listed jobs and notify with the new ones
for job in jobs:
  # skip if the job is not new
  if not job.find('span', class_="badge-new", recursive=False):
    continue

  # if you don't care how the output looks this can replace all the code below it
  # for string in job.stripped_strings:
  #   print(string)

  # get apply link
  link = job.select_one('a:contains("Bewerben")') 
  print("%s%s" % (JOBRUF, link["href"]))

  # get only the tags containging a title
  titles = job.find_all(title=True)
  for title in titles:
      try:
        # get tag string even if the tag contains multiple tags
        # job_string = next(title.stripped_strings)
        job_string = ''
        for string in title.stripped_strings:
          job_string += string + ' '
      except:
        # skip titles that have no strings 
        continue
      
      try:
        if title['title'] == 'Start':
          job_string += ("%s" % datetime.datetime.strptime(job_string.split()[0], "%d.%m.%Y").strftime("%A"))
      except ValueError:
        pass
      # print the title and it's string (job's main info)
      print("%s: %s" % (title['title'], job_string))
  
  # get job details (job's extra info)
  job_details = job.select('div.jobDetails-row')
  for job_detail in job_details:
    try:
      # p contains the title and span contains the string contains 
      print("%s: %s" % (job_detail.p.string, job_detail.span.string)) 
    except:
      # pass if p or span is missing or don't have a string
      pass   
  print("-"*40)