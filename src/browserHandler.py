# ##################################################################################
# Project               Search employers from Companies
# (c) copyright         2016
# Orgnization           University of Utah
# 
# @file                 browserHandler.py
# Description           Handle browser operation
# Author                Yongjian Mu / Aaron
# Date                  5/25/2015
# ##################################################################################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys, csv, re, time, random, os

# Constant var
login_url =                     'https://www.linkedin.com/cap/dashboard/home?recruiterEntryPoint=true&trk=nav_responsive_sub_nav_upgrade'
tag_user_name =                 'session_key-login'
tag_passwd =                    'session_password-login'
user_name =                     'melaniepan@yahoo.com'
passwd =                        'suzhou2016'
login_button =                  'btn-primary'

tag_home_page_search =          'smart-search-header'
tag_advanced_search =           'advanced-search'
tag_left_rail =                 'all-facets-left-rail'
tag_li =                        'li'
tag_form =                      'form'
tag_class =                     'class'
tag_facet_wrapper =             'facet-wrapper'
tag_ol =                        'ol'
tag_div =                       'div'
tag_p =                         'p'
tag_a =                         'a'
tag_h3 =                        'h3'
tag_href =                      'href'
tag_span =                      'span'
tag_id =                        'id'

tag_years_in_current_company =  'facet-yearsInCurrentCompany'
tag_suggestions =               'suggestions'
tag_add_button =                'button'
tag_btn_less_than_one_year =    "//button[@data-id='1']"
tag_txt_less_than_one_year =    "//li[@data-id='1']"

tag_location =                  'facet-location'
txt_fill_location =             'United State'
tag_add_pills =                 'add-pills'
tag_add_pills_btn =             'add-pills-btn'
tag_location_hint =             "//p[contains(@title, 'United States')]"
tag_location_label =            "//li[contains(@title, 'United States')]"

tag_keywords =                  'facet-keywords'
tag_keywords_aria_label =           "//li[contains(@aria-label, 'Press backspace to delete selection')]"

tag_search_hearder =            'all-facets-header'
tag_search_go =                 'yes-btn'

tag_search_result =             'search-result'
tag_search_results =            'serach-results'
tag_name =                      'name'
tag_top_card =                  'top-card'
tag_headline =                  'headline'
tag_location_p =                'location'
tag_pagelink =                  'pagelink'
tag_data_range =                'data-range'

profile_company =               'Company'
profile_name =                  'Name'
profile_link =                  'Link'
profile_title =                 'Title'
profile_location =              'Location'
profile_period =                'Period'

timeout =                       60


# ##################################################################################
# @brief                Wait function from http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
#
# @return               Page loaded or not
# ##################################################################################

def _wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 30:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


# ##################################################################################
# @brief                Wait class from from http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
#
# @class                wait_for_page_load
# ##################################################################################

class wait_for_page_load(object):
	def __init__(self, browser):
		self.browser = browser
	def __enter__(self):
		self.old_page = self.browser.find_element_by_tag_name('html')
		self.old_url = self.browser.current_url
	def page_has_loaded(self):
		new_page = self.browser.find_element_by_tag_name('html')
		new_url = self.browser.current_url
		return new_url != self.old_url
	def __exit__(self, *_):
		_wait_for(self.page_has_loaded)


# ##################################################################################
# @brief                Wait for page loaded
#
# @param driver         Current page
# @param next_page_tag  The key words of the page jumped to
# @return               Page loaded success or not
# ##################################################################################

def _waitPageLoaded(driver, next_page_tag):
    try: 
        dr = WebDriverWait(driver, timeout)
        dr.until(lambda the_driver:the_driver.find_element_by_id(next_page_tag).is_displayed())
    except:
        return False

    return True


# ##################################################################################
# @brief                Wait for button loaded
#
# @param driver         Current page
# @param left_rail      Left rail area
# @param group          Curren group area (sub facet)
# @param suggestion     Suggestion segment
# @param button         The button need to be loaded
# @return               Button loaded success or not
# ##################################################################################

def _waitAddButtonLoaded(driver, left_rail, group, suggestion, button):
    try: 
        dr = WebDriverWait(driver, timeout)
        dr.until(lambda the_driver:the_driver.find_element_by_id(left_rail).find_element_by_id(group).find_element_by_class_name(suggestion).find_element_by_tag_name(button).is_displayed())
    except:
        return False

    return True


# ##################################################################################
# @brief                Wait for location hint loaded
#
# @param driver         Current page
# @param left_rail      Left rail area
# @param group          Curren group area (sub facet)
# @param path           The xpath of hint object
# @return               Hint loaded success or not
# ##################################################################################

def _waitLocationHintLoaded(driver, left_rail, group, path):
    try: 
        dr = WebDriverWait(driver, timeout)
        dr.until(lambda the_driver:the_driver.find_element_by_id(left_rail).find_element_by_id(group).find_element_by_xpath(path).is_displayed())
    except:
        return False

    return True


# ##################################################################################
# @brief                Wait for location label loaded
#
# @param driver         Current page
# @param left_rail      Left rail area
# @param group          Curren group area (sub facet)
# @param pill           Class pill
# @param path           The xpath of label object
# @return               Label loaded success or not
# ##################################################################################

def _waitLocationLabelLoaded(driver, left_rail, group, path):
    try: 
        dr = WebDriverWait(driver, timeout)
        dr.until(lambda the_driver:the_driver.find_element_by_id(left_rail).find_element_by_id(group).find_element_by_xpath(path).is_displayed())
    except:
        return False

    return True


# ##################################################################################
# @brief                Wait for button loaded
#
# @param driver         Current page
# @param left_rail      Left rail area
# @param group          Curren group area (sub facet)
# @param text           Loaded text tag
# @return               Button loaded success or not
# ##################################################################################

def _waitTextFilled(driver, left_rail, group, text):
    try: 
        dr = WebDriverWait(driver, timeout)
        dr.until(lambda the_driver:the_driver.find_element_by_id(left_rail).find_element_by_id(group).find_element_by_xpath(text).is_displayed())
    except:
        return False

    return True


# ##################################################################################
# @brief                Get the text field from the HTML section
# @param text_variable  The tag of HTML section
#
# @return               Text info
# ##################################################################################

def get_text_from_tag(text_variable):	
	try:
		temp_variable = text_variable.text
	except Exception:
		temp_variable = ""
	return temp_variable


# ##################################################################################
# @brief                Initial the browser handler
#
# @class                BrowserHandler
# ##################################################################################

class BrowserHandler:
    mDriver = None
    mAdvLeftRail = None


# ##################################################################################
# @brief                Constructor, open FireFox to initial the browser handler 
#
# @return               
# ##################################################################################

    def __init__(self):
        self.mDriver = webdriver.Firefox()


# ##################################################################################
# @brief                Login LinkedIn Recruiter home page
#
# @return               Login success or not
# ##################################################################################

    def loginLinkedin(self):
        self.mDriver.get(login_url)
    
        loginid = self.mDriver.find_element_by_id(tag_user_name)
        if(None != loginid):
    	    loginid.send_keys(user_name)
        else:
            return False
        
        loginpassword = self.mDriver.find_element_by_id(tag_passwd)
        if(None != loginpassword):
            loginpassword.send_keys(passwd)
        else:
            return False

        loginbutton =  self.mDriver.find_element_by_id(login_button)
        if(None != loginbutton):
            loginbutton.click()
        else:
            return False

        return _waitPageLoaded(self.mDriver, tag_home_page_search)


# ##################################################################################
# @brief                Jump to advanced search Page
#
# @return               Jump success or not
# ##################################################################################

    def jumpToAdvancedSearchPage(self):
        btn_adv_search = self.mDriver.find_element_by_id(tag_advanced_search)
        webdriver.ActionChains(self.mDriver).move_to_element(btn_adv_search).perform()
        self.mDriver.find_element_by_id(tag_advanced_search).click()

        return _waitPageLoaded(self.mDriver, tag_years_in_current_company)


# ##################################################################################
# @brief                Fill the filter "Years in current company"
#
# @return               Filled success or not
# ##################################################################################

    def filterYearsInCurrentCompany(self):
        # Click add button
        driver = self.mDriver
        advLeftRail = driver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_years_in_current_company = None
        group_years_in_current_company = advLeftRail.find_element_by_id(tag_years_in_current_company)
        if(None == group_years_in_current_company):
            return False

        btn_years_in_current_comany = None
        btn_years_in_current_comany = group_years_in_current_company.find_element_by_tag_name(tag_add_button)
        if(None == btn_years_in_current_comany):
            return False

        btn_years_in_current_comany.click()
        if(False == _waitAddButtonLoaded(driver, tag_left_rail, tag_years_in_current_company, tag_suggestions, tag_add_button)):
            return False

        # Click first button
        time.sleep(1)
        advLeftRail = None
        advLeftRail = driver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_years_in_current_company = None
        group_years_in_current_company = advLeftRail.find_element_by_id(tag_years_in_current_company)
        if(None == group_years_in_current_company):
            return False

        group_suggestions = None
        group_suggestions = group_years_in_current_company.find_element_by_class_name(tag_suggestions)
        if(None == group_suggestions):
            return False

        btn_list = None
        btn_list = group_suggestions.find_element_by_tag_name(tag_li)
        if(None == btn_list):
            return False

        btn_less_than_one_year = None
        btn_less_than_one_year = btn_list.find_element_by_xpath(tag_btn_less_than_one_year)
        if(None == btn_less_than_one_year):
            return False

        btn_less_than_one_year.click()
        if(False == _waitTextFilled(driver, tag_left_rail, tag_years_in_current_company, tag_txt_less_than_one_year)):
            return False

        return True


# ##################################################################################
# @brief                Fill the filter "Locations"
#
# @return               Filled success or not
# ##################################################################################

    def filterLocation(self):
        # Click add button
        driver = self.mDriver
        advLeftRail = None
        advLeftRail = driver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_location = None
        group_location = advLeftRail.find_element_by_id(tag_location)
        if(None == group_location):
            return False

        btn_location = None
        btn_location = group_location.find_element_by_class_name(tag_facet_wrapper).find_element_by_class_name(tag_add_pills).find_element_by_class_name(tag_add_pills_btn)
        if(None == btn_location):
            return False

        btn_location.click()
        time.sleep(1)

        # Enter text form to trigger the hint
        advLeftRail = None
        advLeftRail = driver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_location = None
        group_location = advLeftRail.find_element_by_id(tag_location)
        if(None == group_location):
            return False

        form_location = None
        form_location = group_location.find_element_by_tag_name(tag_form)
        if(None == form_location):
            return False
        
        action = webdriver.ActionChains(driver)
        action.send_keys(txt_fill_location)
        action.perform()
        
        if(False == _waitLocationHintLoaded(driver, tag_left_rail, tag_location, tag_location_hint)):
            return False

        # Click the hint (send "TAB" key)
        advLeftRail = None
        advLeftRail = driver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_location = None
        group_location = advLeftRail.find_element_by_id(tag_location)
        if(None == group_location):
            return False

        form_location = None
        form_location = group_location.find_element_by_tag_name(tag_form)
        if(None == form_location):
            return False
        
        action = webdriver.ActionChains(driver)
        action.send_keys(Keys.TAB)
        action.perform()
        
        if(False == _waitLocationLabelLoaded(driver, tag_left_rail, tag_location, tag_location_label)):
            return False

        return True


# ##################################################################################
# @brief                Fill the filter "Company"
#
# @param company_name   One of the names in the company list
# @return               Filled success or not
# ##################################################################################

    def filterKeywords(self, company_name):
        # Click add button
        driver = self.mDriver
        advLeftRail = None
        advLeftRail = driver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_keywords = None
        group_keywords = advLeftRail.find_element_by_id(tag_keywords)
        if(None == group_keywords):
            return False

        btn_keywords = None
        btn_keywords = group_keywords.find_element_by_class_name(tag_facet_wrapper).find_element_by_class_name(tag_add_pills).find_element_by_class_name(tag_add_pills_btn)
        if(None == btn_keywords):
            return False

        btn_keywords.click()
        time.sleep(1)

        # Fill the company name
        action = webdriver.ActionChains(driver)
        action.send_keys(company_name + Keys.ENTER)
        action.perform()

        if(False == _waitLocationLabelLoaded(driver, tag_left_rail, tag_keywords, tag_keywords_aria_label)):
            return False

        return True


# ##################################################################################
# @brief                Click the "Search" button
#
# @return               Button clicked or not
# ##################################################################################

    def goAdvSearch(self):
        driver = self.mDriver

        header = None
        header = driver.find_element_by_id(tag_search_hearder)
        if(None == header):
            return False

        btn_search = None
        btn_search = header.find_element_by_class_name(tag_search_go)
        if(None == btn_search):
            return False

        btn_search.click()

        return True


# ##################################################################################
# @brief                Wait for current page loaded
#
# @return               Refreshed or not
# ##################################################################################

    def waitPageRefresh(self):
        with wait_for_page_load(self.mDriver):
            return True
        return False


# ##################################################################################
# @brief                Get the employers' info in current page
#
# @param company        Current company
# @return               Employers' info
# ##################################################################################

    def getEmployerInfo(self, company):
        profile_list= {}
        profile_counter = 0

        html = self.mDriver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        print(soup)
        search_results = soup.find("ol", { "id" : "search-results" })
        employee_cards = search_results.findAll('li', { "class" : "search-result" })

        for card in employee_cards:
            profile = {}
            top_card = card.find('div', {"class": "top-card"})
            try:
                name = get_text_from_tag(top_card.find_all('h3', {"class" : "name"})[0])
                pagelink = (top_card.find_all('h3', {"class" : "name"})[0]).find('a')['href']
            except Exception:
                name = ""
            try:
                headline_title = get_text_from_tag(top_card.find_all('p', {"class" : "headline"})[0])
            except Exception:
                headline_title = ""
            try:
                location = get_text_from_tag(top_card.find_all('p', {"class" : "location"})[0])
            except Exception:
                location = ""

            profile[profile_company], profile[profile_name], profile[profile_link], profile[profile_title], profile[profile_location] = company, name, pagelink, headline_title, location

            profile_list[str(profile_counter)] = profile
            profile_counter += 1

            print(profile[profile_name])

        return profile_list
