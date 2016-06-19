Introduction

This program is used to scrape the basic info from the LinkedIn.

To get the best performance, Linux system is strongly recommended. It would take 3 to 4 seconds for open one individual page. For Windows, it would take 8 to 10 seconds, while for Mac OS, it would take 15 to 20 seconds. Because the webdriver libaray is well supported in Linux. 


Installation

Step 1:

Install Firefox:   https://www.mozilla.org/en-US/firefox/new/

Install Python 3.5.1:  https://www.python.org/downloads/

Strongly recommended install packages above from the listed links!


Step 2:

Install Python packages:

pip install -U selenium

pip install beautifulsoup4

pip install html5lib

pip install slugify

pip install unicode-slugify

These can be installed via pip command: "pip install -r requirements.txt"

You may need root (Linux/Mac) or administrator(Windows) privilege to install the packages.

Step 3:

Install Python GUI package:

If you installed Python from Step 1, then do nothing.

If not (I think the easiest way is that go back to Step 1, but you can still find the solutions below):

For Mac OS X, install port from https://www.macports.org/install.php, then type:

sudo port -v selfupdate

sudo port install py35-tkinter

For Windows, install tkinter from https://wiki.python.org/moin/TkInter


How to run

Step 1:

Disable the system automatic sleep, screensaver, screen dim, screen lock, and any program which would be on the top of the screen.

This is very important, since the program will simulate the mouse event. Make sure that firefox is running at the top level of the screen.

Do NOT move or click the mouse while the program is running, just leave the PC there.


Step 2:

For Windows, open a cmd window.

For Mac OS / Linux, open a shell terminal.


Step 3:

Enter the "src" subdirector.

Type "python launch.py" or "python3.5 launch.py".


Step 4:

When the program starts to run, there will be a windows pop up, select the input file.

Sample input file is in the "sample" directory.

Output file is named "result.csv". If you already have a file named this, it will change the original file name to "result.csv_bak".


Step 5:

Leave the PC there and when the program finished, the output file "result.csv" will be in the same directory as the input file.


Error handleing:

If the browser stopped and the program is still running, please check the standard output from the terminal, and manually input the missing filter. Then input something like "a" in the terminal and press "Enter" key, and switch back to the browser. The program would run continuously. Since sometimes the company keywords cannot match any company, or sometimes the server does not response the http request.

If something unexpected happended like network down or kicked out by the server, and program is terminated, please rename the result.csv to another file name like result_1.csv (please also do this to log.txt), then delete the companies which has already been parsed from the input file (you can find the parsed companies from the terminal standard output), and run the program again.

