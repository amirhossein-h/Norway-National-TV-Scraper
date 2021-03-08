###########################################################################################################
#                                                                                                         #
#                                   -Import packages and Libraries-                                       #
#                                                                                                         #
###########################################################################################################

import scrapy
import argparse
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from time import sleep

###########################################################################################################
#Construct the argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument('starturl', help= 'starting url for scrapping')
args = ap.parse_args()


chrome_options = Options()
chrome_options.add_argument("--headless")

###########################################################################################################
#                                                                                                         #
#                                            -Classes-                                                    #
#                                                                                                         #
###########################################################################################################

# class UrlSpider(scrapy.Spider):
#     name = 'nrk.no/skole'
#     start_urls = ['https://www.nrk.no/skole/']#list(args['starturl'])

#     def __init__(self):
#         self.full_list = {}

#     def parse(self, response):
#         print('[Info]: Scrapping process started')
#         mainP = response.xpath('//div[@class = "g100 col fc s12 sl18 sg6 sg9 group-reference"]')
#         partOne = mainP.xpath('//div[@class = "g33 col fc s4 sl6 sl9 sl12 sl18 plug-reference relation flow-relation"]/div[@class = " widget lean plug lp_plug cf"]/a/@href').getall()
#         partOne = list(set(partOne))
#         partTwo = mainP.xpath('//div[@class = "g33 col fc s4 sl6 sl9 sl12 sl18 plug-reference relation flow-relation"]/div[@class = " widget brief plug lp_plug cf"]/a/@href').getall()
#         partTwo = list(set(partTwo))
#         allstartLinks = partOne + partTwo
        
#         for url in allstartLinks:
#             driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
#             sleep(5)
#             print("[Info]: Loading {}".format(url))
#             driver.get(url)
#             print("[Info]: Waiting to load {}".format(url))
#             sleep(15)
#             anchores = driver.find_elements_by_xpath('//a[@class = "media-result-card"]')
#             links = [link.get_attribute('href') for link in anchores]
#             print("[Info]: Links in {} extracted".format(url))
#             self.full_list[url] = links
#             driver.quit()
#             sleep(5)
        
#         print(self.full_list)

###########################################################################################################

class UrlExtractor():

    def __init__(self, mainUrl):
        self.full_list = {}
        self.url_counter = {}
        self.startUrl = mainUrl

    def extractor(self):
        print('**********--[Info]: Scraping process started--**********')
        driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
        sleep(2)
        print('**********--[Info]: Requesting MainUrl --> {}--**********'.format(self.startUrl))
        driver.get(self.startUrl)
        sleep(12)
        print('**********--[Info]: Extracting Mainpage urls--**********')
        partOne = driver.find_elements_by_xpath('//div[@class = "g33 col fc s4 sl6 sl9 sl12 sl18 plug-reference relation flow-relation"]/div[@class = " widget lean plug lp_plug cf"]/a')
        partOneLinks = [link.get_attribute('href') for link in partOne]
        partTwo = driver.find_elements_by_xpath('//div[@class = "g33 col fc s4 sl6 sl9 sl12 sl18 plug-reference relation flow-relation"]/div[@class = " widget brief plug lp_plug cf"]/a')
        partTwoLinks = [link.get_attribute('href') for link in partTwo]
        allMainUrls = partOneLinks + partTwoLinks
        driver.quit()
        print('**********--[Info]: Mainpage urls extracted--**********')
        sleep(2)

        for url in allMainUrls:
            driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
            sleep(2)
            print("**********--[Info]: Requesting {}--**********".format(url))
            driver.get(url)
            print("**********--[Info]: Waiting to load {}--**********".format(url))
            sleep(12)
            print('**********--[Info]: Extracting page urls--**********')
            anchores = driver.find_elements_by_xpath('//a[@class = "media-result-card"]')
            links = [link.get_attribute('href') for link in anchores]
            print("**********--[Info]: Urls in {} extracted--**********".format(url))
            self.full_list[url] = links
            self.url_counter[url] = len(links)
            driver.quit()
            sleep(2)

        return self.full_list, len(allMainUrls), self.url_counter


###########################################################################################################

# class QueryResultSpider(scrapy.Spider):
#     name = 'nrk.no/skole/#'

#     def __init__(self, mainurls):
#         self.urls = mainurls
#         self.full_list = {}

#     for url in self.urls:
#         driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
#         driver.get(url)
#         anchores = driver.find_elements_by_xpath('//a[@class = "media-result-card"]')
#         links = [link.get_attribute('href') for link in anchores]
#         self.full_list[url] = links

#     def parse(self, response):
#         mainP = response.xpath('//div[@class = "main-page"]/div[@class = "search-results page"]/div[@class = "search-results--content"]/div[@class = "search-results--content-clip-view"]/div[@class = "query-result"]/div[@class = "media-results--media-list"]')
#         contentsurls = mainP.xpath('//a[@class = "media-result-card"]/@href').getall()


###########################################################################################################
#                                                                                                         #
#                                         -Driver script-                                                 #
#                                                                                                         #
###########################################################################################################

videoUrl, number_of_mainUrl, number_of_subUrl = UrlExtractor(str(args.starturl)).extractor()
# with open('result.txt', 'w') as f:
#     f.write(str(videoUrl))
print('#######---extracted Urls---#######')
print(videoUrl)
print('\n')
print('#######---Number of main Urls---#######')
print(number_of_mainUrl)
print('\n')
print('#######---Number of sub Urls---#######')
print(number_of_subUrl)