# ##################################################################################
# Project               Search employers from Companies
# (c) copyright         2016
# Orgnization           University of Utah
# 
# @file                 fileHandler.py
# Description           Handle file operations
# Author                Yongjian Mu
# Date                  5/25/2016
# ##################################################################################

import tkinter
from tkinter import filedialog
import csv
import os

# Constant var
type_csv =              '.csv'

# ##################################################################################
# @brief                Get the input file fpath rom dialog
#
# @return               Input file name with path
# ##################################################################################

def getInputFile():
    filename = filedialog.askopenfilename()
    return filename

# ##################################################################################
# @brief                Get the file type from the input file    
#
# @param filename       Input file name
# @return               Input file type
# ##################################################################################

def parseInputFileType(filename):
    split_name = os.path.splitext(filename)
    if(1 == len(split_name)):
        return type_csv
    else:
        return split_name[len(split_name) - 1].lower()

# ##################################################################################
# @brief                Get all the company names from the input file
#
# @param file_type      Input file type
# @param file_name      Input file name
# @return               Company list
# ##################################################################################

def parseInputFile(file_type, file_name):
    try:
        company_list = {
            type_csv: _parseCSVInputFile(file_name)
        }[file_type]
    except KeyError:
        print ("No matched file type found")
        return []
    else:
        return company_list

# ##################################################################################
# @brief                CSV file parser
#
# @param file_type      Input file name
# @return               Company list
# ##################################################################################

def _parseCSVInputFile(file_name):
    company_list = []
    count = 0
    for line in open(file_name):
        gvkey, year, uai, logsale, pc_lg, pct1, pct2, group, conm = line.split(',')
        conm = conm.strip('\t\r\n')
        if(0 != count):
            company_list.append(conm)
        count += 1
    return company_list
