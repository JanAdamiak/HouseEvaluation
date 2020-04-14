import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import csv
import time

def get_property_list(website):
    """Find website given as an argument.
        Parse it using BeautifulSoup.
        Return a list with all the property listings on the website.
        Starting with the newest ones."""
    r = requests.get(website)
    soup = BeautifulSoup(r.content, "html5lib")
    return soup.select("li[class*='srp clearfix']")

def data_collect(current_listing):
    """Collect data from main page and individual property pages."""

    zoopla = "https://www.zoopla.co.uk"
    indv_listing = []
    # Get the property"s href.
    href = current_listing.select("a[class*='listing-results-price text-price']")[0]["href"]
    indv_listing.append(zoopla + href)
    # Make a temporary website request, parse it through bs4 and scrape data.
    temp_request = requests.get(zoopla + href)
    temp_soup = BeautifulSoup(temp_request.content, "html5lib")
    temp_list = []

    # Get the property"s number of bedrooms.
    try:
        indv_listing.append(current_listing.select("span[class*='num-icon num-beds']")[0].text)
    except:
        indv_listing.append(0)
    # Get the property"s number of bathrooms.
    try:
        indv_listing.append(current_listing.select("span[class*='num-icon num-baths']")[0].text)
    except:
        indv_listing.append(0)
    # Get the property"s number of receptions.
    try:
        indv_listing.append(current_listing.select("span[class*='num-icon num-reception']")[0].text)
    except:
        indv_listing.append(0)
    # Get the property"s date of listing.
    try:
        indv_listing.append(" ".join(current_listing.select("div[class*='listing-results-footer clearfix']")[0].small.text.split()))
    except:
        indv_listing.append(np.nan)
    # Get the agency"s address.
    try:
        indv_listing.append(current_listing.select("div[class*='listing-results-footer clearfix']")[0].span.text)
    except:
        indv_listing.append(np.nan)
    # Get the property"s price.
    try:
        indv_listing.append(current_listing.select("a[class*='listing-results-price text-price']")[0].text.replace("\n","").replace(" ", ""))
    except:
        indv_listing.append(np.nan)
    # Get the property"s address.
    try:
        indv_listing.append(temp_soup.select("h2[class*='ui-property-summary__address']")[0].text)
    except:
        indv_listing.append(np.nan)
    # Get the property"s floorplan.
    try:
        for floorplan_image in temp_soup.select("ul[class*='dp-floorplan-assets__no-js-links']")[0].find_all("a"):
            temp_list.append(floorplan_image)
    except:
        temp_list.append(np.nan)
    finally:
        indv_listing.append(temp_list)

    return indv_listing

def Zoopla(number_of_pages):
    dataframe = []
    url = "https://www.zoopla.co.uk/for-sale/property/edinburgh-county/?identifier=edinburgh-county&page_size=100&q=Edinburgh&search_source=home&radius=0&pn="
    for page in range(1, number_of_pages + 1):
        properties_from_current_page = get_property_list(url + str(page))
        for idx in range(len(properties_from_current_page)):
            dataframe.append(data_collect(properties_from_current_page[idx]))
            time.sleep(5)
    return pd.DataFrame(dataframe, columns=["website", "bedrooms", "toilets", "other_rooms", "date_listed", "agency_address", "price", "address","floorplan"])


def Cleaner(df):
    df["price"] = df["price"].str.replace(r"\D", "")
    df.fillna(0)

    def get_day(row):
        x = row.split()
        y = re.match("\d+", x[2])
        return y.group()


    def get_month(row):
        x = row.split()
        return x[3]


    def get_year(row):
        x = row.split()
        return x[4]


    def get_postcode(row):
        if row == "[nan]":
            return 0
        else:
            x = row.split()[-1]
            return x

    df["day_listed"] = df["date_listed"].apply(get_day)
    df["month_listed"] = df["date_listed"].apply(get_month)
    df["year_listed"] = df["date_listed"].apply(get_year)
    df["postcode"] = df["address"].apply(get_postcode)

    return df

if __name__ == "__main__":
    data = Zoopla(9)
    raw_data = Cleaner(data)
    raw_data.to_csv("C:\\Users\\Jan\\Desktop\\Projects\\Regression_Appartment_model\\Zoopla_data.csv", index = False)
