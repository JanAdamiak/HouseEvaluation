from bs4 import BeautifulSoup
import numpy as np
import requests
import time
import csv


def get_property_list(website):
    '''Find website given as an argument.
        Parse it using BeautifulSoup.
        Return a list with all the property listings on the website.
        Starting with the newest ones.'''
    r = requests.get(website)
    soup = BeautifulSoup(r.content, 'html5lib')
    return soup.select('li[class*="srp clearfix"]')


def data_collect(current_listing):
    '''Collect data from main page and individual property pages.'''

    zoopla = 'https://www.zoopla.co.uk'
    indv_listing = []
    # Get the property's href.
    href = current_listing.select('a[class*="listing-results-price text-price"]')[0]['href']
    indv_listing.append(zoopla + href)
    # Make a temporary website request, parse it through bs4 and scrape data.
    temp_request = requests.get(zoopla + href)
    temp_soup = BeautifulSoup(temp_request.content, 'html5lib')
    temp_list = []

    # Get the property's number of bedrooms.
    try:
        indv_listing.append(current_listing.select('span[class*="num-icon num-beds"]')[0].text)
    except:
        indv_listing.append(0)
    # Get the property's number of bathrooms.
    try:
        indv_listing.append(current_listing.select('span[class*="num-icon num-baths"]')[0].text)
    except:
        indv_listing.append(0)
    # Get the property's number of receptions.
    try:
        indv_listing.append(current_listing.select('span[class*="num-icon num-reception"]')[0].text)
    except:
        indv_listing.append(0)
    # Get the property's date of listing.
    try:
        indv_listing.append(' '.join(current_listing.select('div[class*="listing-results-footer clearfix"]')[0].small.text.split()))
    except:
        indv_listing.append(np.nan)
    # Get the agency's address.
    try:
        indv_listing.append(current_listing.select('div[class*="listing-results-footer clearfix"]')[0].span.text)
    except:
        indv_listing.append(np.nan)
    # Get the property's price.
    try:
        indv_listing.append(current_listing.select('a[class*="listing-results-price text-price"]')[0].text.replace('\n','').replace(' ', ''))
    except:
        indv_listing.append(np.nan)
    # Get the property's address.
    try:
        indv_listing.append(temp_soup.select('h2[class*="ui-property-summary__address"]')[0].text)
    except:
        indv_listing.append(np.nan)
    # Get the property's floorplan.
    try:
        for floorplan_image in temp_soup.select('ul[class*="dp-floorplan-assets__no-js-links"]')[0].find_all('a'):
            temp_list.append(floorplan_image)
    except:
        temp_list.append(np.nan)
    finally:
        indv_listing.append(temp_list)

    return indv_listing

def Zoopla(starting_page, listings):
    '''
    '''
    if type(listings) == int:
        counter = 0
        all_properties = {}
        # Throw an error if amount of listings is too small.
        if listings < -1 or listings == 0:
            raise Exception('Argument value too small.')
        # If number of listings is -1, scrape all properties on the website.
        elif listings == -1:
            temporary_page_listings = get_property_list(starting_page)
            while True:
                try:
                    # TODO: figure out a way to iterate through all properties
                    # TODO: figure a way to change pages

                    for property_listing in temporary_page_listings:

                except:
                    try:
                        pass #Next page
                        # if .text == 'Next'
                        #
                    except:
                        return all_properties
        # Scrape amount of properties equal to listings.
        else:
            while counter < listings:
                try:
                    pass #my parser here
                    counter += 1
                except:
                    try:
                        pass #Next page
                    except Exception as e:
                        raise
    # Raise an error if not an integer.
    else:
        raise Exception('Not an integer!')

if __name__ == '__main__':
    Zoopla()
