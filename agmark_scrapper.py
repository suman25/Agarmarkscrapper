from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_data_for_given_source(source):
    try:
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table', attrs={'class': 'tableagmark_new'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns and columns[0].text != 'No Data Found':
                    cols = [ele.text.strip() for ele in columns]
                    print(cols)
    except Exception as e:
        print(e)


def get_source_for_given_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    page_source = browser.page_source
    get_data_for_given_source(page_source)
    try:
        doc = browser.find_element_by_xpath(
            '//*[@id="cphBody_GridPriceData"]/tbody/tr[52]/td/table/tbody/tr/td[1]/input').click()
        time.sleep(5)
        page_source = browser.page_source.encode('utf-8')
        get_data_for_given_source(page_source)
        while check_if_nextpage_exits(browser):
            doc = browser.find_element_by_xpath(
                '//*[@id="cphBody_GridPriceData"]/tbody/tr[52]/td/table/tbody/tr/td[3]/input').click()
            time.sleep(5)
            page_source = browser.page_source.encode('utf-8')
            get_data_for_given_source(page_source)
        browser.quit()
    except Exception as e:
        print(e)


def check_if_nextpage_exits(browser):
    try:
        browser.find_element_by_xpath('//*[@id="cphBody_GridPriceData"]/tbody/tr[52]/td/table/tbody/tr/td[3]/input')
        return True
    except NoSuchElementException:
        return False

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
    url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=MH&Tx_District=0&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Maharashtra&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    print('Data for Tomato commodity in pune district\n')
    get_source_for_given_url(url)
    url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=MH&Tx_District=14&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Maharashtra&Tx_DistrictHead=Pune&Tx_MarketHead=--Select--'
    print('Data for Tomato commodity in all districts\n')
    get_source_for_given_url(url)
    print('Data for all commodities in all districts\n')
    url = 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=0&Tx_State=MH&Tx_District=0&Tx_Market=0&DateFrom=01-Jan-2021&DateTo=10-Aug-2021&Fr_Date=01-Jan-2021&To_Date=10-Aug-2021&Tx_Trend=0&Tx_CommodityHead=--Select--&Tx_StateHead=Maharashtra&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    get_source_for_given_url(url)
