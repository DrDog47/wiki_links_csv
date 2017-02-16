#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import csv
import requests
from lxml import html
#import logging

       
def request_url(adress):
    '''function connecting to the Wiki page of Company'''
    try:
        response = requests.get(url = adress) 
    except requests.exceptions.Timeout:
        print ("Time is Out")
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)    
    return response

def extract_link(response,xpath_config):
    '''Here I'm getting link to web site 
       of company with help of XPATH 
       https://www.w3schools.com/xml/xpath_intro.asp'''
    html_page = html.fromstring(response.text)
    arr = html_page.xpath(xpath_config)
    if len(arr) == 0:       
        print("Can't find url")
        return ''
    return arr[0]

def write_csv_file(file_output_name,links_list,header_list):
    '''function writes list of lists in csv file
       and also writes header of file
    '''
    with open (file_output_name,'w',newline='') as file_wr:
        writer = csv.writer(file_wr,delimiter = ',',quotechar = '|',quoting=csv.QUOTE_NONE)
        writer.writerow(header_list)
        writer.writerows(links_list)  
    print("File {0} is ready ".format(file_output_name)) 

if __name__ == '__main__':
    file_output_name = 'wikipedia_answers_example.csv' #name of the output file
    links_list = []
    csv_header_list = ['"wikipedia_page"','"website"']
    
    xpath_config = '//div[@id="mw-content-text"]/table[contains(@class,"infobox")]//\
                                th[text()="Website"]/following-sibling::td[1]//a/@href'
       
    try:
        file_input = sys.argv[1]
    except NameError:
        print("No Argument Error")
        sys.exit(1)
        
    #reading file_input.csv 
    with open (file_input,'r') as file_r:
        for line in file_r:
            wiki_link = line.replace('\n','').strip().strip('"')
            site_link = extract_link(request_url(wiki_link),xpath_config)
            links_list.append(['"{}"'.format(wiki_link),'"{}"'.format(site_link)])
            
    
    #calling function to write wikipedia_answers_example.csv file        
    write_csv_file(file_output_name, links_list, csv_header_list)
    
    



        
 
    
    




