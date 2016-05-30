# ##################################################################################
# Project               Search employers from Companies
# (c) copyright         2016
# Orgnization           University of Utah
# 
# @file                 launch.py
# Description           Launcher the project
# Author                Yongjian Mu
# Date                  5/25/2016
# ##################################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys, csv, re, time, random, os

# import local modules 
import browserHandler as bh
from browserHandler import BrowserHandler
import fileHandler as fh

# ##################################################################################
# Main () 
# ##################################################################################

# Constant var
default_input_file =                        'company.csv'

# Error Code
SUCCESS =                                   0
NO_COMPANY =                                -1
LOGIN_LINKEDIN_HOME_PAGE_FAILED =           -2
JUMP_TO_ADVANCED_SEARCH_PAGE_FAILED =       -3
FILL_LOCATION_FAILED =                      -4
FILL_KEYWORDS_FAILED =                      -5
FILL_YEARS_IN_CURRENT_COMPANY_FAILED =      -6
CLICK_SEARCH_BUTTON_FAILED =                -7
PAGE_REFRESH_FAILED =                       -8
CURRENT_PAGE_INFO_ERROR =                   -9

# Get input company file from local
input_file = fh.getInputFile()
if (None == input_file):
    print("Did not get input file from dialog, use default file")
    input_file = default_input_file

# Judge input file type
input_file_type = fh.parseInputFileType(input_file)

# Get company list
company_list = fh.parseInputFile(input_file_type, input_file)
company_num = len(company_list)
if(0 == company_num):
    print("No company in the list, exit...")
    sys.exit(NO_COMPANY)
else:
    print("Found following companies:")
    print(company_list)

##ToDo: Add a loop for all the companies 
#company = 'AMERICAN ELECTRIC POWER CO'

# Browser
browser = BrowserHandler()

# Login LinkedIn recruiter home page
if(False  == browser.loginLinkedin()):
    print("Login LinkedIn recruiter home page failed, exit...")
    sys.exit(LOGIN_LINKEDIN_HOME_PAGE_FAILED)
else:
    print("Login LinkedIn recruiter home page succeed!")

# Jump to advance search page
if(False == browser.jumpToAdvancedSearchPage()):
    print("Jump to advanced search page failed")
    sys.exit(JUMP_TO_ADVANCED_SEARCH_PAGE_FAILED)
else:
    print("Jump to advanced page succeed!")

# Fill location USA
if(False == browser.filterLocation()):
    print("Fill location failed, exit...")
    sys.exit(FILL_LOCATION_FAILED)
else:
    print("Fill location succeed!")

# Fill keywords 
time.sleep(1)
if(False == browser.filterKeywords(company_list[0])):
    print("Fill keywords failed, exit...")
    sys.exit(FILL_KEYWORDS_FAILED)
else:
    print("Fill keywords succeed!")

# Fill years in current company
time.sleep(1)
if(False == browser.filterYearsInCurrentCompany()):
    print("Fill years in current company failed, exit...")
    sys.exit(FILL_YEARS_IN_CURRENT_COMPANY_FAILED)
else:
    print("Fill years in current company succeed!")

# Click "Search" button
time.sleep(1)
if(False == browser.goAdvSearch()):
    print("Click search button failed, exit...")
    sys.exit(CLICK_SEARCH_BUTTON_FAILED)
else:
    print("Click search button succeed!")

if(False == browser.waitPageRefresh()):
    print("Page refresh failed, exit...")
    sys.exit(PAGE_REFRESH_FAILED)

time.sleep(2)
info_page = {} 
info_page = browser.getEmployerInfo(company_list[0])
if(not info_page):
    print("Current page info error, exit...")
    sys.exit(CURRENT_PAGE_INFO_ERROR)

## Find company addr
#com_link = fc.getAddress(br, company, bing_prefix)
#
## Find the employers' entries
#staff_link = ci.getStaffEntry(br, com_link)
#
## Find employers and next page
#next_page_flag = True # To enter the first loop, set flag = True
#staff_list = []
#while(True == next_page_flag):
#    staff_link, next_page_flag = ci.parseStaffEntry(br, staff_link, staff_list)
#    staff_link = linkedin_prefix + staff_link
#    print (staff_list)

sys.exit(SUCCESS)
