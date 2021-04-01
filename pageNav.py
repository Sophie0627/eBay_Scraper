from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import TimeoutException
import requests
import re
from re import sub
from decimal import Decimal
import time
# threading import Timer

"""
class Watchdog(Exception):
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self
"""

class pageNavigation:
    def __init__(self, url):
        self.main_url = url
        self.delay = 100
        self.browser = webdriver.Chrome()
        self.browser.get(self.main_url)
        WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.ID, 'gf-norton'))
        )

        elem = self.browser.find_element_by_tag_name("body")

        no_of_pagedowns = 20

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns -= 1

        WebDriverWait(self.browser, self.delay).until(
            EC.presence_of_element_located((By.ID, 'gf-norton'))
        )

        r = requests.get(self.main_url)
        data = r.text
        data = re.sub("<!--(.*?)-->", "", data)
        self.soup_original = BeautifulSoup(data)
        self.main_page_item_tags_classnames = [("a", "b-tile"), ("a", "item-tile"), ("a", "mfe-reco-link"), ("abcde_random", "abcde_random")]

        # lists
        self.datalist = [[]]
        self.href_list = []
        self.panel_namelist = ("#CenterPanelInternal", "#LeftSummaryPanel", "abcde_random")
        self.title_tagnamelist = ("#itemTitle", "abcde_random")
        self.description_tagnamelist = ("#vi-itm-cond", "abcde_random")
        self.quantity_tagnamelist = ("#qtySubTxt", "abcde_random")
        self.price_tagnamelist = ("#prcIsum", "#prcIsum_bidPrice", "abcde_random")
        self.image_tagnamelist = ("img#icImg", "abcde_random")
        self.selection_name_tagnamelist = (".vi-msku-cntr", "abcde_random")
        self.selection_body_tagnamelist = (".msku-sel", "abcde_random")

    def get_href_list(self, item_list):
        for single_item in item_list:
            # if single_item["href"][0:20] == "https://www.ebay.com":
            self.href_list.append(single_item["href"])

    def search_item_in_namelist(self, soup, namelist):
        for name in namelist:
            temp_soup = soup.select_one(name)
            if temp_soup is not None:
                break
        return temp_soup

    def get_tagname(self, soup, namelist):
        for name in namelist:
            temp_soup = soup.select_one(name)
            if temp_soup is not None:
                break
        return name

    def get_details(self):
        html = self.browser.page_source
        if html:
            one_soup = BeautifulSoup(html)
            panel_soup = self.search_item_in_namelist(one_soup, self.panel_namelist)
            if panel_soup is None:
                return "No panel item found."

            temp_row = []
            sku = "None"
            temp_row.append(sku)

            title = "None"
            title_item = self.search_item_in_namelist(panel_soup, self.title_tagnamelist)
            if title_item is not None:
                title = title_item.text
            temp_row.append(title)

            description = "None"
            description_item = self.search_item_in_namelist(panel_soup, self.description_tagnamelist)
            if description_item is not None:
                description = description_item.text
            temp_row.append(description)

            quantity = 0
            quantity_item = self.search_item_in_namelist(panel_soup, self.quantity_tagnamelist)
            if quantity_item is not None:
                quantity = Decimal(sub(r'[^\d.]', '', quantity_item.text))
            temp_row.append(quantity)

            price = "None"
            price_item = self.search_item_in_namelist(panel_soup, self.price_tagnamelist)
            if price_item is not None:
                price = price_item.text
            temp_row.append(price)

            image = "None"
            image_item = self.search_item_in_namelist(panel_soup, self.image_tagnamelist)
            if image_item is not None:
                image = image_item["src"]
            temp_row.append(image)

            product_identifier = "None"
            temp_row.append(product_identifier)

            product_identifier_type = "None"
            temp_row.append(product_identifier_type)

            brand = "None"
            temp_row.append(brand)

            cost = "None"
            cost_item = panel_soup.find(string="cost")
            if cost_item is not None:
                cost = cost_item.text
            
            selection_pane_no = len(panel_soup.find_all("select"))

            optionname1 = "None"
            optionname2 = "None"
            optionname3 = "None"
            optionname4 = "None"
            optionname5 = "None"
            option1 = "None"
            option2 = "None"
            option3 = "None"
            option4 = "None"
            option5 = "None"
            if selection_pane_no != 0:
                optionname1_obj = self.search_item_in_namelist(panel_soup.select_one('div.nonActPanel'), self.selection_name_tagnamelist)
                optionname1 = optionname1_obj.select_one('label').text
                selected_tag_name = self.get_tagname(panel_soup.select_one('div.nonActPanel'), self.selection_name_tagnamelist)
                
                optionname2_obj = optionname1_obj.find_next_sibling(selected_tag_name)
                if optionname2_obj is not None:
                    optionname2 = optionname2_obj.select_one('label').text
                    optionname3_obj = optionname2_obj.find_next_sibling(selected_tag_name)
                    if optionname3_obj is not None:
                        optionname3 = optionname3_obj.select_one('label').text
                        optionname4_obj = optionname3_obj.find_next_sibling(selected_tag_name)
                        if optionname4_obj is not None:
                            optionname4 = optionname4_obj.select_one('label').text
                            optionname5_obj = optionname4_obj.find_next_sibling(selected_tag_name)
                            if optionname5_obj is not None:
                                optionname5 = optionname5_obj.select_one('label').text
                
                option_objs = panel_soup.select_one('div.nonActPanel').find_all('select', class_='msku-sel')
                option1 = option_objs[0].find('option', attrs={'selected' : 'selected'})
                if len(option_objs) > 1:
                    option2 = option_objs[1].find_next_sibling(attrs={'selected' : 'selected'})
                if len(option_objs) > 2:
                    option3 = option_objs[2].find_next_sibling(attrs={'selected' : 'selected'})
                if len(option_objs) > 3:
                    option4 = option_objs[3].find_next_sibling(attrs={'selected' : 'selected'})
                if len(option_objs) > 4:
                    option5 = option_objs[4].find_next_sibling(attrs={'selected' : 'selected'})
                
            temp_row.append(optionname1)
            temp_row.append(optionname2)
            temp_row.append(optionname3)
            temp_row.append(optionname4)
            temp_row.append(optionname5)
            temp_row.append(option1)
            temp_row.append(option2)
            temp_row.append(option3)
            temp_row.append(option4)
            temp_row.append(option5)

            self.datalist.append(temp_row)

    def main_page_navigation(self):
        for tagname, classname in self.main_page_item_tags_classnames:
            item_list = self.soup_original.find_all(tagname, class_=classname)

            if len(item_list):
                self.get_href_list(item_list)
                i = 0
                for one_url in self.href_list:
                    i = i + 1
                    response = requests.get(one_url)
                    if response:
                        self.browser.get(one_url)
                        message = self.get_details()
                    else:
                        continue

        return self.datalist