# Importing useful libraries
from datetime import datetime
from dateutil import relativedelta
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files

# Defining some variables about the file
__author__ = "Rafael Malcervelli"
__version__ = "1.0.0"
__email__ = "r.malcervelli@gmail.com"

# Class definition
class Robot:
    def __init__(self):
        self.url = "www.nytimes.com"
        self.browser_lib = Selenium(auto_close=True, )
        self.http = HTTP()

    def open_the_website(self):
        self.browser_lib.open_available_browser(self.url, maximized=True)

    def search_for(self, phrase):
        self.phrase = phrase
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
            self.browser_lib.click_element("//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[2]/div/div/button")
            ul_element = self.browser_lib.find_element("//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/ul")

            for i in range(0, len(ul_element.text.split("\n"))):
                if section.lower() in ul_element.text.split("\n")[i].lower():
                    self.browser_lib.click_element(f"//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[{i+1}]/label")
                    break

            # Selecting the date range
            self.browser_lib.click_element("//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[1]/div/div/button")
            self.browser_lib.click_element("//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button")

            if n_of_months <= 1:
                date_format = '%m/%d/%Y'

                start_date = datetime.now().replace(day=1)
                final_date = start_date + relativedelta.relativedelta(months=1)

                start_date = start_date.strftime(date_format)
                final_date = final_date.strftime(date_format)
            else:
                final_date, start_date = self.get_date_range(n_of_months)

            xpath_form1 = "//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div/label[1]/input"
            xpath_form2 = "//html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div/label[2]/input"
            
            try:
                print(start_date, final_date)
                self.browser_lib.input_text(xpath_form1, start_date)
                self.browser_lib.input_text(xpath_form2, final_date)
                self.browser_lib.press_keys(xpath_form2, "ENTER")
            except Exception as e:
                print(e)
                print("Invalid date range")

    def count_in_title_description(self, title, description):
        count = 0
        for word in title.split(" "):
            if word.lower() in self.phrase.lower() and len(word) > 2:
                count += 1
        
        for word in description.split(" "):
            if word.lower() in self.phrase.lower() and len(word) > 2:
                count += 1
        
        return count

    def check_money(self, title, description):
        for word in title.split(" "):
            if word.lower() in ["$", "dollars", "USD"]:
                return True
        
        for word in description.split(" "):
            if word.lower() in ["$", "dollars", "USD"]:
                return True
        
        return False

    def get_all_articles(self):
        dic_art = {}

        # Accepting cookies
        self.browser_lib.click_button_when_visible("//html/body/div/div[2]/main/div[2]/div[2]/div/div[2]/button[1]")

        # Clicking on the show more button until there is no more `pages`
        while True:
            try:
                self.browser_lib.click_button_when_visible("//html/body/div/div[2]/main/div/div[2]/div[3]/div/button")

            except Exception as e:
                break

        try:
            for i in range(1, 1000):
                item = self.browser_lib.find_elements(f"//html/body/div/div[2]/main/div[1]/div[2]/div[2]/ol/li[{i}]/div/div")
                
                if item == []:
                    break
                elif item == [""]:
                    continue

                list_items = item[0].text.split("\n")
                
                if len(list_items) > 1:
                    item_date = self.browser_lib.find_element(f"//html/body/div/div[2]/main/div[1]/div[2]/div[2]/ol/li[{i}]/div/span").text
                    filename = f"article_{i}.jpg"
                    
                    self.http.download(self.browser_lib.find_element(f"//html/body/div/div[2]/main/div[1]/div[2]/div[2]/ol/li[{i}]/div/div/figure/div/img").get_attribute("src"), f"output/{filename}")

                    dic_art[i] = {"title": list_items[1], "date": item_date,"description": list_items[2], "picture_filename": filename, "count_search": self.count_in_title_description(list_items[1], list_items[2]), "money": self.check_money(list_items[1], list_items[2])}
                else:
                    continue
            
            self.dict_articles = dic_art
            self.got_all_articles = True
        except Exception as e:
            print(e)
            if e == "list index out of range":
                print("No more articles to show")
                pass
        
    def export_to_excel(self):
        if self.got_all_articles:
            files = Files()
            filename = "articles.xlsx"
            excel_file = files.create_workbook(filename)

            excel_file.set_cell_value(1, 1, "Title")
            excel_file.set_cell_value(1, 2, "Date")
            excel_file.set_cell_value(1, 3, "Description")
            excel_file.set_cell_value(1, 4, "Picture filename")
            excel_file.set_cell_value(1, 5, "Count of search phrases")
            excel_file.set_cell_value(1, 6, "Contains money")

            row = 2
            for article_id, article in self.dict_articles.items():
                excel_file.set_cell_value(row, 1, article["title"])
                excel_file.set_cell_value(row, 2, article["date"])
                excel_file.set_cell_value(row, 3, article["description"])
                excel_file.set_cell_value(row, 4, article["picture_filename"])
                excel_file.set_cell_value(row, 5, article["count_search"])
                excel_file.set_cell_value(row, 6, article["money"])
                row += 1
            
            excel_file.save(filename)
        else:
            print("You need to get all articles first")

if __name__ == "__main__":
    print("[X] You are running this module file directly (and not importing it).")
    