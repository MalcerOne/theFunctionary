# Importing useful libraries
from RPA.Browser.Selenium import Selenium
import utils

# Defining some variables about the file
__author__ = "Rafael Malcervelli"
__version__ = "1.0.0"
__email__ = "r.malcervelli@gmail.com"

# Defining global variables
browser_lib = Selenium(auto_close=True)

# ================ Functions ================
def open_the_website(url):
    browser_lib.open_available_browser(url)

def search_for(term):
    input_field = "css:input"
    browser_lib.input_text(input_field, term)
    browser_lib.press_keys(input_field, "ENTER")

def store_screenshot(filename):
    browser_lib.screenshot(filename=filename)
# ===========================================

# ================ Main ================
def main():
    try:
        open_the_website("www.nytimes.com")
        search_for("python")
        store_screenshot("output/screenshot.png")
    finally:
        browser_lib.close_all_browsers()
# ======================================

# Calling the main function
if __name__ == "__main__":
    main()