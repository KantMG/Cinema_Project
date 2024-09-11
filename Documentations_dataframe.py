#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:00:53 2024

@author: quentin
"""


import requests
from bs4 import BeautifulSoup


def info_source(url):

    # URL of the HTML page you want to read
    
    # Fetch the content of the URL (requests.get(url): Sends a GET request to the specified URL.)
    response = requests.get(url)
    
    # Check if the request was successful 
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup, allowing you to navigate and manipulate it.
        # response.content: Retrieves the raw HTML content of the page.
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Print the parsed HTML (or you can access specific elements)
        # Formats the HTML content in a readable manner.
        print(soup.prettify())
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")    


# title.akas.tsv.gz
# titleId (string) - a tconst, an alphanumeric unique identifier of the title
# ordering (integer) – a number to uniquely identify rows for a given titleId
# title (string) – the localized title
# region (string) - the region for this version of the title
# language (string) - the language of the title
# types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
# attributes (array) - Additional terms to describe this alternative title, not enumerated
# isOriginalTitle (boolean) – 0: not original title; 1: original title
