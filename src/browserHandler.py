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
import time

# Constant var
login_url =                     'https://www.linkedin.com/cap/dashboard/home?recruiterEntryPoint=true&trk=nav_responsive_sub_nav_upgrade'
tag_user_name =                 'session_key-login'
tag_passwd =                    'session_password-login'
user_name =                     'melaniepan@yahoo.com'
passwd =                        'suzhou2016'
login_button =                  'btn-primary'

tag_home_page_search =          'smart-search-header'
tag_advanced_search =           'advanced-search'
tag_years_in_current_company =  'facet-yearsInCurrentCompany'

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
# @brief                Initial the browser handler
#
# @class                BrowserHandler
# ##################################################################################

class BrowserHandler:
    mDriver = 0


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
# @return               Login succeed or not
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
# @brief                Advanced Search
#
# @return               Search succeed or not
# ##################################################################################

    def jumpToAdvancedSearchPage(self):
        btn_adv_search = self.mDriver.find_element_by_id(tag_advanced_search)
        webdriver.ActionChains(self.mDriver).move_to_element(btn_adv_search).perform()
        self.mDriver.find_element_by_id(tag_advanced_search).click()
        return _waitPageLoaded(self.mDriver, tag_years_in_current_company)
