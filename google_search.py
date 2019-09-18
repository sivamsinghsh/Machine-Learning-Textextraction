# from googlesearch import search
# import urllib.request
# from bs4 import BeautifulSoup

# def google_scrape(url):
#     #thepage = urllib.urlopen(url)
#     with urllib.request.urlopen(url) as url:
# 	    s = url.read()
# 	    # I'm guessing this would output the html source code ?
# 	    #print(s)
# 	    soup = BeautifulSoup(s, "html.parser")
# 	    return soup.title.text

# i = 1
# query = 'sachin'
# for url in search(query, stop=10):
#     a = google_scrape(url)
#     print(str(i) + ". " + a)
#     print(url)
#     print(" ")
#     i += 1

import argparse
import json
import itertools
import logging
import re
import os
import uuid
import sys
import csv
from urllib.request import urlopen, Request
import urllib.parse
import urllib
from requests.utils import requote_uri

from bs4 import BeautifulSoup

import tkinter
import base64
from PIL import Image, ImageTk

import requests
from PIL import Image
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(handler)
    return logger

logger = configure_logging()

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    #print('google url',url)
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')

def get_query_url(query):
    return requote_uri("https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q=%s&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:m,itp:face,iar:s" % query)
    #return requote_uri("https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query)

def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    return link_type_records

def extract_images(query, num_images):
    url = get_query_url(query)
    print('query url==>>',url)
    logger.info("Souping")
    soup = get_soup(url, REQUEST_HEADER)
    logger.info("Extracting image urls")
    link_type_records = extract_images_from_soup(soup)
    return itertools.islice(link_type_records, num_images)

def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)
    resp = urlopen(req)
    return resp.read()

def save_image(raw_image, image_type, save_directory):
    extension = image_type if image_type else 'jpg'
    file_name = uuid.uuid4().hex
    save_path = os.path.join(save_directory, file_name)
    with open(save_path, 'wb') as image_file:
        image_file.write(raw_image)

def download_images_to_dir(images, save_directory, num_images,name,PID):
    for i, (url, image_type) in enumerate(images):
        try:
            logger.info("Making request (%d/%d): %s", i, num_images, url)
            #print('num_images==>>',url)
            raw_image = get_raw_image(url)

            with open('C:/Users/Shivam Singh/Desktop/1_to_2500_data.csv','a',newline='',encoding='utf-8') as csvfile:
                filewriter=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
                # filewriter.writerow(i for i in header)
                print("Response Url==>>",url)
                filewriter.writerow([PID,name,url])
            	#save_image(raw_image, image_type, save_directory)
        except Exception as e:
            logger.exception(e)

def run(query, save_directory, num_images=10):
    query = '+'.join(query.split())
    #print('image lnks==>>',query)
    logger.info("Extracting image links")
    images = extract_images(query, num_images)
    logger.info("Downloading images")
    #download_images_to_dir(images, save_directory, num_images,name,PID)
    logger.info("Finished")

def main():
    parser = argparse.ArgumentParser(description='Scrape Google images')
    # parser.add_argument('-n', '--num_images', default=1, type=int, help='num images to save')
    # parser.add_argument('-d', '--directory', default='/Users/Shivam Singh/images/', type=str, help='save directory')

    # name1 = 'sachin'.encode('ascii', 'ignore').decode('ascii')

    # args = parser.parse_args()
    # run(args.search, args.directory, args.num_images)

    with open('C:/Users/Shivam Singh/Desktop/1_to_2500.csv','rt',encoding='utf-8') as f:
    	names=csv.reader(f)
    	i=0
    	for name in names:
            name1=name[1]
            if i>0:
                name1 = name1.encode('ascii', 'ignore').decode('ascii')
                #name1="eoghan o'connell"
                name1.replace("'", "")
                name1.replace('\'', '')
                name1 = name1.replace("'", " ")
                name1 = name1.replace('"', " ")
                #parser.add_argument('-s', '--search', default=name1, type=str, help='search term')
                images = extract_images(name1+' footballar', 1)
                logger.info("Downloading images")
                download_images_to_dir(images, '', 1,name1,name[0])
                # parser.add_argument('-s', '--search', default=name1, type=str, help='search term')
                # args = parser.parse_args()
                #run(args.search,'',1)

            # if i==1:
            #         sys.exit()
            print('increement count==>>',i)
            i +=1
if __name__ == '__main__':
    main()