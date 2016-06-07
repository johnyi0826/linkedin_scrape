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

If you installed Python from Step 1, then do nothing

If not (I think the easiest way is that go back to Step 1, but you can still find the solutions below):

For Mac OS X, install port from https://www.macports.org/install.php, then type:

sudo port -v selfupdate

sudo port install py35-tkinter

For Windows, install tkinter from https://wiki.python.org/moin/TkInter


How to run

Step 1:

Disable the system automatic sleep, screensaver, screen dim and screen lock

This is very important, since the program will simulate the mouse event

Do NOT move or click the mouse while the program is running, just leave the PC there


Step 2:

For Windows, open a cmd window

For Mac OS / Linux, open a shell terminal


Step 3:

Enter the "src" subdirector

Type "python launch.py" or "python3.5 launch.py"


Step 4:

When the program starts to run, there will be a windows pop up, select the input file.

Sample input file is in the "sample" directory.

Output file is named "result.csv". If you already have a file named this, it will change the original file name to "result.csv_bak".


Step 5:

Leave the PC there and when the program finished, the output file "result.csv" will be in the same directory as the input file

If there is more than one title for a person in current company, the the different info of "Title" and "Period" field will be divided by ";"
