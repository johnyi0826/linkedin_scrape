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
from slugify import slugify


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

tag_search_results_region =     'search-results-region'

tag_years_in_current_company =  'facet-yearsInCurrentCompany'
tag_suggestions =               'suggestions'
tag_add_button =                'button'
tag_btn_years =                 "//button[@data-id='3']"
tag_txt_years =                 "//li[@data-id='3']"

tag_location =                  'facet-location'
txt_fill_location =             'United State'
tag_add_pills =                 'add-pills'
tag_add_pills_btn =             'add-pills-btn'
tag_location_hint =             "//p[contains(@title, 'United States')]"
tag_location_label =            "//li[contains(@title, 'United States')]"

tag_keywords =                  'facet-keywords'
tag_keywords_aria_label =       "//li[contains(@aria-label, 'Press backspace to delete selection')]"


tag_current_company =           'facet-currentCompany'
tag_current_company_hint =      "//p[contains(@role, 'option')]"
tag_current_company_label =     "//li[contains(@aria-label, 'Press backspace to delete selection.')]"

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

profile_number =                'Count'
profile_origial_company =       'Original Company from Input File'
profile_keywords =              'Keywords'
profile_company =               'Company'
profile_is_current =            'Is Current'
profile_name =                  'Name'
profile_link =                  'Link'
profile_title =                 'Title'
profile_location =              'Current Location'
profile_period =                'Period'

timeout =                       60
min_wait = 1 
max_wait = 5 
linkedin_prefix =               "www.linkedin.com"


# ##################################################################################
# @brief                        Wait function from http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
#
# @param condition_function     Callback function
# @return                       Page loaded or not
# ##################################################################################

def _wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 60:
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
# @param browser        Current browser
# @return               Page loaded success or not
# ##################################################################################

def _wait_for_next_page_loaded(browser):
    start_time = time.time()
    old_page = browser.find_element_by_tag_name('html')
    old_url = browser.current_url
    while time.time() < start_time + 60:
        new_page = browser.find_element_by_tag_name('html')
        new_url = browser.current_url
        if(new_url != old_url):
            return True
        else:
            time.sleep(0.1)
    return False

    
                

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
    mCounter = 0

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
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
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
        if(False == _waitAddButtonLoaded(self.mDriver, tag_left_rail, tag_years_in_current_company, tag_suggestions, tag_add_button)):
            return False

        # Click first button
        time.sleep(1)
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
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
        btn_less_than_one_year = btn_list.find_element_by_xpath(tag_btn_years)
        if(None == btn_less_than_one_year):
            return False

        btn_less_than_one_year.click()
        if(False == _waitTextFilled(self.mDriver, tag_left_rail, tag_years_in_current_company, tag_txt_years)):
            return False

        return True


# ##################################################################################
# @brief                Fill the filter "Locations"
#
# @return               Filled success or not
# ##################################################################################

    def filterLocation(self):
        # Click add button
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
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
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
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
        
        action = webdriver.ActionChains(self.mDriver)
        action.send_keys(txt_fill_location)
        action.perform()
        
        if(False == _waitLocationHintLoaded(self.mDriver, tag_left_rail, tag_location, tag_location_hint)):
            return False

        # Click the hint (send "TAB" key)
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
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
        
        action = webdriver.ActionChains(self.mDriver)
        action.send_keys(Keys.TAB)
        action.perform()
        
        if(False == _waitLocationLabelLoaded(self.mDriver, tag_left_rail, tag_location, tag_location_label)):
            return False

        return True


# ##################################################################################
# @brief                Fill the filter "Keywords" field
#
# @param company_name   One of the names in the company list
# @return               Filled success or not
# ##################################################################################

    def filterKeywords(self, company_name):
        # Click add button
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
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
        action = webdriver.ActionChains(self.mDriver)
        action.send_keys(company_name + Keys.ENTER)
        action.perform()

        if(False == _waitLocationLabelLoaded(self.mDriver, tag_left_rail, tag_keywords, tag_keywords_aria_label)):
            return False

        return True


# ##################################################################################
# @brief                Fill the filter "Current Company" field
#
# @param company_name   One of the names in the company list
# @return               Filled success or not
# ##################################################################################
    def filterCurrentCompany(self, company_name):
        # Click add button
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_keywords = None
        group_keywords = advLeftRail.find_element_by_id(tag_current_company)
        if(None == group_keywords):
            return False

        btn_keywords = None
        btn_keywords = group_keywords.find_element_by_class_name(tag_facet_wrapper).find_element_by_class_name(tag_add_pills).find_element_by_class_name(tag_add_pills_btn)
        if(None == btn_keywords):
            return False

        btn_keywords.click()
        time.sleep(1)

        # Enter text form to trigger the hint
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_location = None
        group_location = advLeftRail.find_element_by_id(tag_current_company)
        if(None == group_location):
            return False

        form_location = None
        form_location = group_location.find_element_by_tag_name(tag_form)
        if(None == form_location):
            return False
        
        action = webdriver.ActionChains(self.mDriver)
        action.send_keys(company_name)
        action.perform()
        
        if(False == _waitLocationHintLoaded(self.mDriver, tag_left_rail, tag_current_company, tag_current_company_hint)):
            return False

        # Click the hint (send "Arrown Down" key and "Enter" key)
        advLeftRail = None
        advLeftRail = self.mDriver.find_element_by_id(tag_left_rail)
        if(None == advLeftRail):
            return False

        group_location = None
        group_location = advLeftRail.find_element_by_id(tag_current_company)
        if(None == group_location):
            return False

        form_location = None
        form_location = group_location.find_element_by_tag_name(tag_form)
        if(None == form_location):
            return False
        
        action = webdriver.ActionChains(self.mDriver)
        action.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
        action.perform()
        
        while(False == _waitLocationLabelLoaded(self.mDriver, tag_left_rail, tag_current_company, tag_current_company_label)):
            print("Something wrong happened with company" + company_name + ", You can input manually")
            time.sleep(1)
            #return False

        return True




# ##################################################################################
# @brief                Click the "Search" button
#
# @return               Button clicked or not
# ##################################################################################

    def goAdvSearch(self):
        header = None
        header = self.mDriver.find_element_by_id(tag_search_hearder)
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
        if(False == _wait_for_next_page_loaded(self.mDriver)):
                time.sleep(1)
                self.mDriver.refresh()
                time.sleep(1)
        return True 


# ##################################################################################
# @brief                Get the employers' info in current page
#
# @param company        Current company
# @return               Employers' info
# ##################################################################################

    def getEmployerInfo(self, company, keywords):
        profile_list= {}
        profile_counter = 0

        html = self.mDriver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        search_results = soup.find("ol", { "id" : "search-results" })
        employee_cards = search_results.findAll('li', { "class" : "search-result" })

        for card in employee_cards:
            self.mCounter += 1
            is_current = True
            top_card = card.find('div', {"class": "top-card"})
            try:
                name = get_text_from_tag(top_card.find_all('h3', {"class" : "name"})[0])
                pagelink = (top_card.find_all('h3', {"class" : "name"})[0]).find('a')['href']
            except Exception:
                name = ""
                pagelink = ""
            pagelink  = linkedin_prefix + pagelink

            try:
                location = get_text_from_tag(top_card.find_all('p', {"class" : "location"})[0])
            except Exception:
                location = ""

            current_postions_container = None
            current_positions = None
            past_positions_container = None
            past_positions = None

            info_rows = card.find('div', {"class": "info"})
            spliter = ' at '
            if(None != info_rows):
                # Current Company
                current_postions_container = info_rows.find('ol', {"aria-label": "Current positions"})
                if(None != current_postions_container):
                    current_positions = current_postions_container.findAll('li')
                if(None != current_positions):
                    is_current = True
                    for position in current_positions:
                        profile = {}
                        current_position = ""
                        current_period = ""
                        current_company = ""

                        date_range = position.find('span', {"class" : "date-range"})
                        thedate = get_text_from_tag(date_range)
                        if(None != date_range):
                            date_range.replace_with('')
                        position_text = get_text_from_tag(position)

                        # Get company name
                        if(-1 != position_text.find(spliter)):
                                current_company += position_text.split(spliter)[1]
                                current_position += position_text.split(spliter)[0]
                        else: 
                                current_position += position_text

                        current_period += thedate
                        current_period = slugify(current_period)

                        profile[profile_number], profile[profile_origial_company], profile[profile_is_current], profile[profile_keywords], profile[profile_company], profile[profile_name], profile[profile_link], profile[profile_title], profile[profile_location], profile[profile_period] = self.mCounter, company, is_current, keywords, current_company, name, pagelink, current_position, location, current_period

                        profile_list[str(profile_counter)] = profile
                        profile_counter += 1

                # Past Companies
                past_positions_container = info_rows.find('ol', {"aria-label": "Past positions"})
                if(None != past_positions_container):
                    past_positions = past_positions_container.findAll('li')
                if(None != past_positions):
                    is_current = False
                    for position in past_positions:
                        profile = {}
                        past_position = ""
                        past_period = ""
                        past_company = ""

                        date_range = position.find('span', {"class" : "date-range"})
                        thedate = get_text_from_tag(date_range)
                        if(None != date_range):
                            date_range.replace_with('')
                        position_text = get_text_from_tag(position)
                        
                        # Get company name
                        if(-1 != position_text.find(spliter)):
                                past_company += position_text.split(spliter)[1]
                                past_position += position_text.split(spliter)[0]
                        else: 
                                past_position += position_text

                        past_period += thedate
                        past_period = slugify(past_period)

                        profile[profile_number], profile[profile_origial_company], profile[profile_is_current], profile[profile_keywords], profile[profile_company], profile[profile_name], profile[profile_link], profile[profile_title], profile[profile_location], profile[profile_period] = self.mCounter, company, is_current, keywords, past_company, name, pagelink, past_position, location, past_period

                        profile_list[str(profile_counter)] = profile
                        profile_counter += 1

        return profile_list


# ##################################################################################
# @brief                Click next page button
#
# @return               Clicked or no next page button
# ##################################################################################

    def clickNextPage(self):
        pagination_nav = self.mDriver.find_element_by_id("pagination")
        nextpagebutton = None
        if(None != pagination_nav):
            nextpagecontainer = pagination_nav.find_elements_by_class_name("next")
            if(nextpagecontainer):
                nextpagebutton = nextpagecontainer[0].find_element_by_tag_name("a")
        if(None == nextpagebutton):
            return False
        nextpagebutton.click()
        if(False == _wait_for_next_page_loaded(self.mDriver)):
                time.sleep(random.randint(min_wait, max_wait))
                while(True): # Protect link down
                    self.mDriver.refresh()
                    time.sleep(random.randint(min_wait, max_wait))
                    if(True == _waitPageLoaded(self.mDriver, tag_search_results_region)):
                        break
        return True 


# ##################################################################################
# @brief                Click recruiter home page button
#
# @return               Jumped to home page or not
# ##################################################################################

    def jumpToHomePage(self):
        html = self.mDriver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        home_page_container = soup.find("nav")
        home_page_suffix = home_page_container.find("a", { "title" : "Recruiter" })
        home_page_link = linkedin_prefix + home_page_suffix['href']

        self.mDriver.get(home_page_link)
        return _waitPageLoaded(self.mDriver, tag_home_page_search)


