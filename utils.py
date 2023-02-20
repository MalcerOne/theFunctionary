# Importing useful libraries
import time
from datetime import datetime
from dateutil import relativedelta
from RPA.Browser.Selenium import Selenium

# Class definition
class Robot:
    def __init__(self):
        self.url = "www.nytimes.com"
        self.browser_lib = Selenium(auto_close=True)

    def open_the_website(self):
        self.browser_lib.open_available_browser(self.url, maximized=True)

    def search_for(self, phrase):
        self.browser_lib.click_element("//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/button")

        input_form = "//html/body/div[1]/div[2]/div/header/section[1]/div[1]/div[2]/div/form/div/input"
        self.browser_lib.input_text(input_form, phrase)
        self.browser_lib.press_keys(input_form, "ENTER")

        self.new_search = True

    def get_date_range(self, n_of_months):
        date_format = '%m/%d/%Y'
        date_start = datetime.now() + relativedelta.relativedelta(months=1)
        date_start = date_start.replace(day=1)

        if n_of_months >= 2:
            date_end = date_start - relativedelta.relativedelta(months=n_of_months)
        
        date_start = date_start.strftime(date_format)
        date_end = date_end.strftime(date_format)

        return date_start, date_end

    def apply_filters(self, section, n_of_months):
        if self.new_search:
            # Clicking on the filter button to select the section
            self.browser_lib.click_element("//html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/button")
            ul_element = self.browser_lib.find_element("//html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul")

            for i in range(0, len(ul_element.text.split("\n"))):
                if section.lower() in ul_element.text.split("\n")[i].lower():
                    self.browser_lib.click_element(f"//html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[{i+1}]/label")
                    break
            
            # Sorting by Newest
            self.browser_lib.select_from_list_by_label("//html/body/div/div[2]/main/div/div[1]/div[1]/form/div[2]/div/select", "Sort by Newest")

            # Selecting the date range
            self.browser_lib.click_element("//html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/button")
            self.browser_lib.click_element("//html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button")

            if n_of_months == 0 or n_of_months == 1:
                start_date = "{}/{}/{}".format(datetime.now().month, "01", datetime.now().year)
                final_date = "{}/{}/{}".format(datetime.now().month + 1, "01", datetime.now().year)
            else:
                final_date, start_date = self.get_date_range(n_of_months)

            xpath_form = "//html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div/label[2]/input"
            self.browser_lib.input_text(xpath_form, start_date)
            self.browser_lib.input_text(xpath_form, final_date)
            self.browser_lib.press_keys(xpath_form, "ENTER")
            
    def get_all_articles(self):
        articles = self.browser_lib.find_elements("//html/body/div/div[2]/main/div/div[2]/div/ol")
        print(articles[1].text.split("\n"))
        # /html/body/div/div[2]/main/div/div[2]/div/ol/li[1]


        
def main():
    robot = Robot()
    robot.open_the_website()
    robot.search_for("python")
    robot.apply_filters("arts", 2)
    robot.get_all_articles()

if __name__ == "__main__":
    main()
    