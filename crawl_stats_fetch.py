from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import os
import time
import pandas as pd
import numpy as np


class FetchCrawlStats:
    def __init__(self):
        # initialize browser
        print()
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        dir_path = os.path.dirname(os.path.realpath(__file__))  # telling python that driver is located wherever the scirpt is
        chromedriver = dir_path + '/chromedriver'
        driver = webdriver.Chrome(options=options, executable_path=chromedriver)
        self.driver = driver

        # set xpath for tables
        dict = {
            'pages_per_day': '//*[@id="fetches-gviz-chart"]/div/div[1]/div/div/table/tbody',
            'kilobytes_per_day': '//*[@id="bytes-gviz-chart"]/div/div[1]/div/div/table/tbody',
            'time_spent_downloading': '//*[@id="times-gviz-chart"]/div/div[1]/div/div/table/tbody'
        }
        self.tables_path = dict

    def login_to_sc(self, username, password):
        url = 'https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fsearch.google.com%2Fsearch-console%3Fhl%3Dpl%26&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
        self.driver.get(url)
        time.sleep(1)

        action = webdriver.ActionChains(self.driver)
        emailElem = self.driver.find_element_by_id('identifierId')
        emailElem.send_keys(username)
        self.driver.find_element_by_id('identifierNext').click()
        time.sleep(2)

        passwordElem = self.driver.find_element_by_name('password')
        passwordElem.send_keys(password)
        self.driver.find_element_by_id('passwordNext').click()
        time.sleep(10)

    def open_craw_stats(self, website):
        url = 'https://www.google.com/webmasters/tools/crawl-stats?hl=en&siteUrl={0}/'.format(website)
        self.driver.maximize_window()
        self.driver.get(url)
        print('\nFetching stats for {0}'.format(website))

    def fetch_data(self, xpath):
        xpath = xpath
        table = self.driver.find_element_by_xpath(xpath)

        data = []

        for row in table.find_elements_by_xpath('.//tr'):
            date = row.find_element_by_xpath('.//td[1]')
            value = row.find_element_by_xpath('.//td[2]')
            rec = [date.get_attribute('innerHTML'), value.get_attribute('innerHTML')]
            data.append(rec)

        df = pd.DataFrame(data, columns=['date', 'value'])
        return df


