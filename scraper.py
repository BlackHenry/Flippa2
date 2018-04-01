import pandas as pd
import bs4
from selenium import webdriver
import time


class Scraper:
    def __init__(self, d=False):
        self.debug = d
        self.product_links = []
        self.database = pd.DataFrame()
        self.attributes = ['listing_type', 'site_age', 'platform', 'site_type', 'net_profit', 'template_unique?',
                           'content_unique?', 'content_unique?', 'design_unique?', 'pages_/_session','bounce_rate',
                           'avg._session_duration']

    def collect_links(self, starting_url, total_pages):
        driver = webdriver.Firefox()
        for _ in range(total_pages):
            if self.debug:
                print('Processing page number ' + str(_ + 1))
            url = starting_url + '&page[number]=' + str(_ + 1)
            driver.get(url)
            page = driver.page_source
            soup = bs4.BeautifulSoup(page, 'html.parser')
            link_wrappers = soup.find_all('a', class_='Detailed___linkWrapper grid grid--bleed')
            self.product_links += [link_wrapper['href'] for link_wrapper in link_wrappers]
        driver.close()

    def collect_attribute(self, soup, id_name, element='div'):
        try:
            return ''.join(soup.find(element, id=id_name).find_all(text=True))
        except Exception as e:
            if self.debug:
                print(e)
            return ''

    def process_link(self, link, driver):
        temp_db = pd.DataFrame()
        driver.get(link)
        page = driver.page_source
        soup = bs4.BeautifulSoup(page, 'html.parser')
        for attribute in self.attributes:
            val = self.collect_attribute(soup, attribute)
            temp_db[attribute] = [val]
        if soup.find('div', class_='Listing-trafficTable') is not None:
            traffic_table = soup.find('div', class_='Listing-trafficTable').find('tbody')
            traffic_data = []
            for row in traffic_table.find_all('tr'):
                traffic_data_row = []
                for cell in row.find_all('td'):
                    traffic_data_row.append(cell.find(text=True))
                traffic_data.append(traffic_data_row)
            if len(traffic_data) < 10:
                traffic_data.append([[0, 0, 0] for _ in range(10 - len(traffic_data))])
            if len(traffic_data) > 10:
                traffic_data = traffic_data[:10]
            for _ in range(10):
                temp_db['page_visitors_' + str(_)] = [traffic_data[_][1]]
                temp_db['page_views_' + str(_)] = [traffic_data[_][2]]
        temp_db['starting_price'] = soup.find('h2').find(text=True)
        self.database = self.database.append(temp_db)

    def scrape(self, url):
        self.collect_links(url, 12)
        _ = 1
        driver = webdriver.Firefox()
        driver.get('https://flippa.com/')
        time.sleep(20)
        for link in self.product_links[:10]:
            if self.debug:
                print('Processing link number', _, ':', link)
                _ += 1
            self.process_link(link, driver)
        self.database.to_csv('Database.csv')

s = Scraper(True)
s.scrape('https://flippa.com/search?filter[property_type]=website&page[size]=250')
