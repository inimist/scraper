#!/usr/bin/python3
from selectorlib import Extractor
import requests
from time import sleep
import csv
import json

domainurl = "https://www.booking.com"
MAX_PROPS = 20
fieldnames = [
    "Title",
    "Reviews",
    "Rating",
    "Gallery",
    "Thumbs",
    "Features",
    "Type",
    "URL",
    "URL Stays",
    "Beds",
    "Bedrooms",
    "Sleeps",
    "Map",
    "Description",
    "ID",
    "Best For",
    "Category"
]

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('properties.yml')
p = Extractor.from_yaml_file('property.yml')

def scrape(url):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    print("\n--------------------------------------------------\n")
    r = requests.get(url, headers=headers)
    # Pass the HTML of the page and create 
    return e.extract(r.text,base_url=url)

def scrape_property(url):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Reading Property %s"%url)
    print("\n--------------------------------------------------\n")
    r = requests.get(url, headers=headers, stream=False)
    # Pass the HTML of the page and create 
    return p.extract(r.text,base_url=url)

with open("urls.json",'r') as json_urllist, open('properties.csv','w', newline='') as outfile:

    writer = csv.DictWriter(outfile, fieldnames=fieldnames,quoting=csv.QUOTE_ALL)
    writer.writeheader()
   
    json_data = json.load(json_urllist)

    #print(json_data)
    #print(fieldnames)

    for pair in json_data: # iterator over a dictionary
        #print (pair)
        for place, url in pair.items():
            #print(place, url)
            data = scrape(url)
            if data:
                #print(data)
                n=0
                for h in data['properties']:

                    if(h['url']):
       
                        url = h['url']

                        if( url.find(domainurl) < 0 ):
                            url = domainurl + h['url']

                        pdata = scrape_property(url)
                        #print(pdata)
                        pdata['URL'] = url

                        if(pdata['Features']):
                            pdata['Features'] = ',' . join(pdata['Features'])
                        
                        if(pdata['Gallery']):
                            pdata['Gallery'] = ',' . join(pdata['Gallery'])

                        if(pdata['Thumbs']):
                            pdata['Thumbs'] = ',' . join(pdata['Thumbs'])
                        
                        #print(pdata)
                        #break

                        pdata['Category'] = place

                        if pdata:
                            #for h in data['hotels']:
                            writer.writerow(pdata)
                            print("Property row written")
                            print("\n--------------------------------------------------\n")

                            # sleep(5)

                    n = n + 1

                    if( n>=MAX_PROPS ):
                        break
        #break

print("Property scrapping completed!!")
