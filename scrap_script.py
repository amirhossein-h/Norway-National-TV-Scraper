###########################################################################################################
#                                                                                                         #
#                                   -Import packages and Libraries-                                       #
#                                                                                                         #
###########################################################################################################

import argparse
from seleniumwire import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from time import sleep

#####################################|||||----SET UP----|||||##############################################
#Construct the argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument('starturl', help= 'starting url for scrapping')
args = ap.parse_args()


chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--no-sandbox')

###########################################################################################################
#                                                                                                         #
#                                            -Classes-                                                    #
#                                                                                                         #
###########################################################################################################

# class UrlExtractor():

#     def __init__(self, mainUrl):
#         self.full_list = {}
#         self.url_counter = {}
#         self.startUrl = mainUrl

#     def extractor(self):
#         print('**********--[Info]: Scraping process started--**********')
#         driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
#         sleep(2)
#         print('**********--[Info]: Requesting MainUrl --> {}--**********'.format(self.startUrl))
#         driver.get(self.startUrl)
#         sleep(12)
#         print('**********--[Info]: Extracting Mainpage urls--**********')
#         partOne = driver.find_elements_by_xpath('//div[@class = "g33 col fc s4 sl6 sl9 sl12 sl18 plug-reference relation flow-relation"]/div[@class = " widget lean plug lp_plug cf"]/a')
#         partOneLinks = [link.get_attribute('href') for link in partOne]
#         partTwo = driver.find_elements_by_xpath('//div[@class = "g33 col fc s4 sl6 sl9 sl12 sl18 plug-reference relation flow-relation"]/div[@class = " widget brief plug lp_plug cf"]/a')
#         partTwoLinks = [link.get_attribute('href') for link in partTwo]
#         allMainUrls = partOneLinks + partTwoLinks
#         driver.quit()
#         print('**********--[Info]: Mainpage urls extracted--**********')
#         sleep(2)

#         for url in allMainUrls:
#             driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
#             sleep(2)
#             print("**********--[Info]: Requesting {}--**********".format(url))
#             driver.get(url)
#             print("**********--[Info]: Waiting to load {}--**********".format(url))
#             sleep(12)
#             print('**********--[Info]: Extracting page urls--**********')
#             anchores = driver.find_elements_by_xpath('//a[@class = "media-result-card"]')
#             links = [link.get_attribute('href') for link in anchores]
#             print("**********--[Info]: Urls in {} extracted--**********".format(url))
#             self.full_list[url] = links
#             self.url_counter[url] = len(links)
#             driver.quit()
#             sleep(2)

#         return self.full_list, len(allMainUrls), self.url_counter



###########################################################################################################

class UrlExtractor():

    def __init__(self, mainUrl):
        self.full_list = {}
        self.url_counter = {}
        self.failedMainUrls = []
        self.failedSubUrls = []
        self.links = []
        self.startUrl = mainUrl

    def mainUrlExtractor(self):
        try:
            #Stage one- extracting url on the main page
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
            return allMainUrls
        except ValueError as e:
            print(e)

    def subUrlExtractor(self, MainUrls, path, attr , level = 'One'):
        #Stage two- extracting suburls in each main url
        for url in MainUrls:
            try:
                driver = webdriver.Chrome(executable_path = binary_path, options = chrome_options)
                sleep(2)
                print("**********--[Info]: Requesting {}--**********".format(url))
                driver.get(url)
                print("**********--[Info]: Waiting to load {}--**********".format(url))
                sleep(12)
                print('**********--[Info]: Extracting page urls--**********')
                if level == 'One':
                    anchores = driver.find_elements_by_xpath(path)
                    links = [link.get_attribute(attr) for link in anchores]
                    print("**********--[Info]: Urls in {} extracted--**********".format(url))
                    self.full_list[url] = links
                    driver.quit()
                    sleep(2)
                elif level == 'Two':
                    li = {}
                    print('**********--[Info]: Extracting page url--**********')
                    elem = driver.find_element_by_xpath(path)
                    media_link = elem.get_attribute(attr)
                    for request in driver.requests:
                        if request.response:
                            if request.url.endswith('.vtt'):
                                subtitle_link = str(requst.url)
                            else:
                                subtitle_link = 'Not Found'
                    li[media_link] = subtitle_link
                    print("**********--[Info]: Urls in {} extracted--**********".format(url))
                    self.links.append(li)
                    driver.quit()
                    sleep(2)
            except ValueError as e:
                print('\n**********--[Warning]: {}--**********\n'.format(e))
                print('**********--[Notice]: Unsusccessfull extraction of related url(s) to {}--**********'.format(url))
                if level == 'One':
                    self.failedMainUrls.append(url)
                elif level == 'Two':
                    self.failedSubUrls.append(url)
                driver.quit()
                continue

        if level == 'One':
            return self.full_list
        elif level == 'Two':
            return self.links

    def statistics(self):
        numberOfMainUrls = len(self.full_list)
        for k, v in self.full_list.items():
            self.url_counter[k] = len(v)

        return numberOfMainUrls, self.url_counter, self.failedMainUrls, self.failedSubUrls


###########################################################################################################
#                                                                                                         #
#                                         -Driver script-                                                 #
#                                                                                                         #
###########################################################################################################
#Making a url extractor object
E = UrlExtractor(str(args.starturl))
#Extracting urls on the mainpage
mainUrls = E.mainUrlExtractor()
#Extracting first level sub urls for each url on the mainpage
path = '//a[@class = "media-result-card"]'
attr = 'href'
subUrlsLevelOne = E.subUrlExtractor(mainUrls, path, attr, level = 'One')
#Extracting permanent link to the extracted urls in previous step
pathTwo = '/html/body/div/div[3]/div/div/div/t-3-0-7/div/div/div[2]/div/div[1]/div/label/input'
attrTwo = 'value'
#Dcitionary that holds each url on the mainpage as key and its related urls as values
full_list = {}
#List that holds urls that their sub urls could not be extracted
problematic = []
print('**********--[Info]: Extracting permanent urls--**********')
#Itereate on dictionary from second step to obtain permanent link to each url
for k, v in subUrlsLevelOne.items():
    if v:
        subUrlLevelTwo = E.subUrlExtractor(v, pathTwo, attrTwo, level = 'Two')
        full_list[k] = subUrlLevelTwo
    else:
        problematic.append(k)


numberOfMainUrls, numberofSubUrls, mainfailed, subfailed = E.statistics()
# with open('result.txt', 'w') as f:
#     f.write(str(videoUrl))
print('#######---extracted Urls---#######')
print(full_list)
print('\n')
print('#######---Problematic Urls---#######')
print(problematic)
print('\n')
print('#######---Mainfailed Urls---#######')
print(mainfailed)
print('\n')
print('#######---Subfailed Urls---#######')
print(subfailed)
print('\n')
print('#######---Number of main Urls---#######')
print(numberOfMainUrls)
print('\n')
print('#######---Number of sub Urls---#######')
print(numberOfSubUrls)