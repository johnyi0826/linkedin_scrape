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
import sys, csv, re, time, random, os, platform

# import local modules 
import browserHandler as bh
from browserHandler import BrowserHandler
import fileHandler as fh

# Constant var
default_input_file =                        'company.csv'
default_output_file =                       'result.csv'
default_log_file =                          'log.txt'

profile_number =                            'Count'
profile_origial_company =                   'Original Company from Input File'
profile_keywords =                          'Keywords'
profile_company =                           'Company'
profile_is_current =                        'Is Current'
profile_name =                              'Name'
profile_link =                              'Link'
profile_title =                             'Title'
profile_location =                          'Current Location'
profile_period =                            'Period'

profile_fields =                            [profile_number, profile_origial_company, profile_keywords, profile_company, profile_is_current, profile_name, profile_link, profile_title, profile_location, profile_period]

sys_windows =                               "Windows"

# Error Code
SUCCESS =                                   0
NO_COMPANY =                                -1
LOGIN_LINKEDIN_HOME_PAGE_FAILED =           -2
JUMP_TO_ADVANCED_SEARCH_PAGE_FAILED =       -3
FILL_LOCATION_FAILED =                      -4
FILL_KEYWORDS_FAILED =                      -5
FILL_CURRENT_COMPANY_FAILED =               -6
FILL_YEARS_IN_CURRENT_COMPANY_FAILED =      -7
FILL_YEARS_IN_CURRENT_POSITION_FAILED =     -8
CLICK_SEARCH_BUTTON_FAILED =                -9
PAGE_REFRESH_FAILED =                       -10
CURRENT_PAGE_INFO_ERROR =                   -11
JUMP_TO_HOME_PAGE_FAILED =                  -12


# ##################################################################################
# Main () 
# ##################################################################################

# Get system type
current_system = platform.system()

# Get input company file from local
print("Please choose your input file. The output file will be in the same directory as the input file.")
input_file = fh.getInputFile()
# Open output file
output_path = os.path.dirname(input_file)
if (None == input_file):
    print("Did not get input file from dialog, use default file")
    input_file = default_input_file
    output_path = "."

# Open output file and write header
output_filename = ""
output_log_file = ""
if(sys_windows == current_system):
    output_path = output_path.replace("/", "\\")
    output_filename = output_path + "\\" + default_output_file
    output_log_file = output_path + "\\" + default_log_file
else:
    output_filename = output_path + "/" + default_output_file
    output_log_file = output_path + "/" + default_log_file

# If output file exist, rename it with "_bak" suffix
if(True == os.path.exists(output_filename)):
    os.rename(output_filename, output_filename + "_bak")

fd = fh.openFile(output_filename)
fw = fh.getFileWriter(fd, profile_fields)
fh.writeFileHeader(fw)

log_fd = fh.openLogFile(output_log_file)
fh.writeLogRow(log_fd, "Start program")

# Judge input file type
input_file_type = fh.parseInputFileType(input_file)

# Get company list
company_list, keywords_list = fh.parseInputFile(input_file_type, input_file)
company_num = len(company_list)
if(0 == company_num):
    print("No company in the list, exit...")
    sys.exit(NO_COMPANY)
else:
    print("Found following companies:")
    print(company_list)

# Open outputfile
output_file = fh.openFile(output_filename)

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

# Start loop
for i in range(company_num):

    # Jump to advance search page
    if(False == browser.jumpToAdvancedSearchPage()):
        print("Jump to advanced search page failed")
        #sys.exit(JUMP_TO_ADVANCED_SEARCH_PAGE_FAILED)
        tmp = input("You can manually click advance search button")
        time.sleep(2)
    else:
        print("Jump to advanced page succeed!")

    # Fill location USA
    if(False == browser.filterLocation()):
        print("Fill location failed, exit...")
        #sys.exit(FILL_LOCATION_FAILED)
        tmp = input("You can manually fill location")
        time.sleep(2)
    else:
        print("Fill location succeed!")
    
    # Fill keywords 
    #time.sleep(1)
    #if(False == browser.filterKeywords(keywords_list[i])):
    #    print("Fill keywords failed, exit...")
    #    sys.exit(FILL_KEYWORDS_FAILED)
    #else:
    #    print("Fill keywords succeed!")
    
    # Fill current company 
    time.sleep(1)
    if(False == browser.filterCurrentCompany(keywords_list[i])):
        print("Fill current company failed")
        #sys.exit(FILL_CURRENT_COMPANY_FAILED)
        print("Company: " + keywords_list[i])
        tmp = input("You can manually input current company")
        time.sleep(2)
    else:
        print("Fill current company succeed!")
    
    # Fill years in current company
    time.sleep(1)
    if(False == browser.filterYearsInCurrentCompany()):
        print("Fill years in current company failed")
        #sys.exit(FILL_YEARS_IN_CURRENT_COMPANY_FAILED)
        tmp = input("You can manually fill years in current company")
        time.sleep(2)
    else:
        print("Fill years in current company succeed!")
    
    # Click "Search" button
    time.sleep(1)
    if(False == browser.goAdvSearch()):
        print("Click search button failed")
        #sys.exit(CLICK_SEARCH_BUTTON_FAILED)
        tmp = input("You can manually click advance search button")
        time.sleep(2)
    else:
        print("Click search button succeed!")
    
    if(False == browser.waitPageRefresh()):
        print("Page refresh failed")
        #sys.exit(PAGE_REFRESH_FAILED)
        tmp = input("You can manually refresh page")
        time.sleep(2)

    # Is limitation?
    total_candidates = browser.isLimitation()
    if(0 != total_candidates):
        fh.writeLogRow(log_fd, "Company: " + company_list[i] + " has reached limitation, total: " + str(total_candidates) + " candidates, split into 3 parts.")

        for k in range(1, 4):
            time.sleep(1)

            # Jump to advance search page
            if(False == browser.jumpToHomePage()):
                print("Jump to home page failed")
                #sys.exit(JUMP_TO_HOME_PAGE_FAILED)
                tmp = input("You can manually jump to home page")
                time.sleep(2)

            if(False == browser.jumpToAdvancedSearchPage()):
                print("Jump to advanced search page failed")
                #sys.exit(JUMP_TO_ADVANCED_SEARCH_PAGE_FAILED)
                tmp = input("You can manually click advance search button")
                time.sleep(2)
            else:
                print("Jump to advanced page succeed!")

            # Fill location USA
            if(False == browser.filterLocation()):
                print("Fill location failed")
                #sys.exit(FILL_LOCATION_FAILED)
                tmp = input("You can manually fill location")
                time.sleep(5)
            else:
                print("Fill location succeed!")
            
            # Fill current company 
            time.sleep(1)
            if(False == browser.filterCurrentCompany(keywords_list[i])):
                print("Fill current company failed")
                #sys.exit(FILL_CURRENT_COMPANY_FAILED)
                print("Company: " + keywords_list[i])
                tmp = input("You can manually input current company")
                time.sleep(2)
            else:
                print("Fill current company succeed!")
            
            # Fill years in current company
            time.sleep(1)
            if(False == browser.filterYearsInCurrentCompany()):
                print("Fill years in current company failed")
                #sys.exit(FILL_YEARS_IN_CURRENT_COMPANY_FAILED)
                tmp = input("You can manually fill years in current company")
                time.sleep(2)
            else:
                print("Fill years in current company succeed!")
           
            # Fill years in current position
            if(False == browser.filterYearsInCurrentPosition(k)):
                print("Fill years in current position failed, id = " + str(k))
                #sys.exit(FILL_YEARS_IN_CURRENT_POSITION_FAILED)
                print("id = " + str(k))
                tmp = input("You can manually input years in current position")
                time.sleep(2)

            # Click "Search" button
            time.sleep(1)
            if(False == browser.goAdvSearch()):
                print("Click search button failed")
                #sys.exit(CLICK_SEARCH_BUTTON_FAILED)
                tmp = input("You can manually click advance search button")
                time.sleep(2)

            else:
                print("Click search button succeed!")
            
            if(False == browser.waitPageRefresh()):
                print("Page refresh failed")
                #sys.exit(PAGE_companyREFRESH_FAILED)
                tmp = input("You can manually refresh page")
                time.sleep(2)

            # Is limitation?
            total_candidates = browser.isLimitation()
            if(0 != total_candidates):
                fh.writeLogRow(log_fd, "Company: " + company_list[i] + " with split id = " + str(k) + " still has reached limitation, total: " + str(total_candidates) + " candidates.")

            while(True):
                time.sleep(2)
                info_page = {} 
                info_page = browser.getEmployerInfo(company_list[i], keywords_list[i])
                if(not info_page):
                    print("No candidate, break...")
                    fh.writeLogRow(log_fd, "Company: " + company_list[i] + " has no candidates, split id = " + str(k))
                    #sys.exit(CURRENT_PAGE_INFO_ERROR)
                    break
            
                for x in range(len(info_page)):
                    fh.writeRow(fw, info_page[str(x)])
            
                if(False == browser.clickNextPage()):
                    break
    
    else:
    
        while(True):
            time.sleep(2)
            info_page = {} 
            info_page = browser.getEmployerInfo(company_list[i], keywords_list[i])
            if(not info_page):
                print("No candidate, break...")
                fh.writeLogRow(log_fd, "Company: " + company_list[i] + " has no candidates.")
                #sys.exit(CURRENT_PAGE_INFO_ERROR)
                break
        
            for x in range(len(info_page)):
                fh.writeRow(fw, info_page[str(x)])
        
            if(False == browser.clickNextPage()):
                break
    
    time.sleep(1)
    if(False == browser.jumpToHomePage()):
        print("Jump to home page failed")
        #sys.exit(JUMP_TO_HOME_PAGE_FAILED)
        tmp = input("You can manually jump to home page")
        time.sleep(2)
    else:
        print("Current finished: " + company_list[i] + " , ratio: " + str(i + 1) + " of " + str(company_num))
        time.sleep(1)

fh.writeLogRow(log_fd, "Finished successfully")
# Close output file
fh.closeFile(fd)
fh.closeFile(log_fd)

print("Scrape prgrogram finished success!")
sys.exit(SUCCESS)
