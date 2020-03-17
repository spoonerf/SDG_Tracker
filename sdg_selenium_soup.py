import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import compress

#the sdg-tracker pages I want to get data from
pages = ["https://sdg-tracker.org/no-poverty","https://sdg-tracker.org/zero-hunger",
"https://sdg-tracker.org/good-health", "https://sdg-tracker.org/quality-education",
"https://sdg-tracker.org/gender-equality", "https://sdg-tracker.org/water-and-sanitation",
"https://sdg-tracker.org/energy", "https://sdg-tracker.org/economic-growth", "https://sdg-tracker.org/infrastructure-industrialization",
"https://sdg-tracker.org/inequality", "https://sdg-tracker.org/cities", "https://sdg-tracker.org/sustainable-consumption-production",
"https://sdg-tracker.org/climate-change", "https://sdg-tracker.org/oceans",
"https://sdg-tracker.org/biodiversity", "https://sdg-tracker.org/peace-justice", "https://sdg-tracker.org/global-partnerships"]

for page_in in pages:
    page = requests.get(page_in)   #one of the sdg-tracker pages I want to download from
    soup = BeautifulSoup(page.content, 'html.parser')   #parsing the html from this page
    html = list(soup.children)[2]
    text = [] # Getting the source links with indicator data out into a csv
    fig_src = []
    for tag in html.find_all(class_ = "col-md"):
        x = tag.get_text()
        y = x.split("\n")[1]
        text.append(y)
        print(tag)
        fig = tag.find_all(class_="grapherPreview")
        fig_src.append(fig)
    avail = text[1::2]
    ind = text[::2]
    source = fig_src[1::2]
    df = pd.DataFrame(list(zip(ind, avail, source)), columns =['Indicator', 'Available', 'Source'])
    df.to_csv(r'C:\Users\Fiona\Documents\ECEHH\SDG_Tracker\sdg_tracker_sources.csv', mode='a', header=False)
    figs = soup.find_all(class_="grapherPreview")  #finding all the 'grapherPreview' windows on the page - ignoring the extraneous href tags
    srcs = []
    for fig in figs:
      srcs.append(fig.get('data-grapher-src'))  #getting the source page link for each of the grapherPreview windows
    driver = webdriver.Chrome()   #setting up the web driver
    for src in srcs:      #looping through each of the links
      split_src = src.split("?", 1)   #ensuring that it is the DATA tab that page opens on rather than chart etc
      sub_src = split_src[0]
      src_new = sub_src + "?tab=data"
      print(src_new)
      driver.get(src_new)   #opening up on the DATA tab of the source link
      if driver.current_url == src_new:     #sometimes the page redirects - this checks this and ensures the redirected page opens on the DATA tab
          headlines = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'active', ' ' ))]")   #identifies which tab is 'active' - should be data
          for headline in headlines:
              print(headline.text.strip())
              click_dat = headline.click()     #clicks the active tab
              csv_source = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' '), concat( ' ', 'btn-primary', ' ' ))]")   #identifies the primary button to download data
              csv_source.click()   #clicks the primary button to download data
      else:
          print('Redirecting from ' + src_new)  #reformats the redirected url to ensure the DATA tab is active
          src_red = driver.current_url
          split_src_red = src_red.split("?", 1)
          sub_src_red = split_src_red[0]
          src_new_red = sub_src_red + "?tab=data"
          driver.get(src_new_red)
          headlines = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'active', ' ' ))]")
          for headline in headlines:
              print(headline.text.strip())
              click_dat = headline.click()
              csv_source = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' '), concat( ' ', 'btn-primary', ' ' ))]")
              csv_source.click()
