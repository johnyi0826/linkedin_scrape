1. Installation

Step 1:

Install Firefox:   https://www.mozilla.org/en-US/firefox/new/
Install Python 3.5.1:  https://www.python.org/downloads/

Strongly recommended install packages above from the listed linkes!

Step 2:

Install Python packages:
pip install -U selenium
pip install beautifulsoup4
pip install html5lib

These can be installed via pip: `pip install -r requirements.txt`

Step 3:

Install Python GUI package:

If you installed Python from Step 1, then do nothing

If not (I think the easiest way is that go back to Step 1, but you can still find the solutions below):

For Mac OS X, install port from https://www.macports.org/install.php, then type:
sudo port -v selfupdate
sudo port install py35-tkinter

For Windows, install tkinter from https://wiki.python.org/moin/TkInter
