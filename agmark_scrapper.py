from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv


def get_data_for_given_source(source):
    try:
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table', attrs={'class': 'tableagmark_new'})
        data = []
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns and columns[0].text != 'No Data Found':
                    cols = [ele.text.strip() for ele in columns]
                    print(cols)
                    data.append(cols)
            return data
    except Exception as e:
        print(e)


def write_to_csv(file_name, data):
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Id", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Min price", "Max Price",
             "Modal price", "Price Date"])
        for outer_element in data:
            writer.writerows(outer_element)


def get_source_for_given_url(url):
    data_list = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    page_source = browser.page_source
    data = get_data_for_given_source(page_source)
    data_list.append(data)
    try:
        doc = browser.find_element_by_xpath(
            '//*[@id="cphBody_GridPriceData"]/tbody/tr[52]/td/table/tbody/tr/td[1]/input').click()
        time.sleep(5)
        page_source = browser.page_source.encode('utf-8')
        data = get_data_for_given_source(page_source)
        data_list.append(data)
        while check_if_nextpage_exits(browser):
            doc = browser.find_element_by_xpath(
                '//*[@id="cphBody_GridPriceData"]/tbody/tr[52]/td/table/tbody/tr/td[3]/input').click()
            time.sleep(5)
            page_source = browser.page_source.encode('utf-8')
            data = get_data_for_given_source(page_source)
            data_list.append(data)
        browser.quit()
        return data_list
    except Exception as e:
        print(e)


def check_if_nextpage_exits(browser):
    try:
        browser.find_element_by_xpath('//*[@id="cphBody_GridPriceData"]/tbody/tr[52]/td/table/tbody/tr/td[3]/input')
        return True
    except NoSuchElementException:
        return False


def handler():
    url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=MH&Tx_District=14&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Maharashtra&Tx_DistrictHead=Pune&Tx_MarketHead=--Select--'
    print('Data for Tomato commodity in pune district\n')
    print("Id", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Min price", "Max Price",
          "Modal price", "Price Date")
    data = get_source_for_given_url(url)
    write_to_csv('tomato_pune.csv', data)
    url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=MH&Tx_District=0&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Maharashtra&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    print("Id", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Min price", "Max Price",
          "Modal price", "Price Date")
    print('Data for Tomato commodity in all districts\n')
    get_source_for_given_url(url)
    write_to_csv('tomato_all_districts.csv', data)
    print('Data for all commodities in all districts\n')
    print("Id", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Min price", "Max Price",
          "Modal price", "Price Date")
    url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=0&Tx_State=MH&Tx_District=0&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=--Select--&Tx_StateHead=Maharashtra&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    get_source_for_given_url(url)
    write_to_csv('all_commodities.csv', data)


# since it is possible to get the data using single url have commented this part out to avoid mutliple calls
# def get_data_for_each_commodity():
#     url = 'https://agmarknet.gov.in'
#     source = requests.get(url).text
#     soup = BeautifulSoup(source, 'lxml')
#     commodities = soup.find('select', attrs={'id': "ddlCommodity"})
#
#     for option in commodities.find_all('option'):
#         url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=' + option[
#             'value'] + '&Tx_State=MH&Tx_District=0&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=--Select--&Tx_StateHead=Maharashtra&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
#         source = requests.get(url).text
#         soup = BeautifulSoup(source, 'lxml')
#         table = soup.find('table', attrs={'class': 'tableagmark_new'})
#         if table:
#             rows = table.find_all('tr')
#             for row in rows:
#                 columns = row.find_all('td')
#                 if columns and columns[0].text != 'No Data Found':
#                     for column in columns:
#                         if column != 'No Data Found':
#                             cols = [ele.text.strip() for ele in columns]
#                             print(cols)
#             time.sleep(5)

if __name__ == '__main__':
    handler()
