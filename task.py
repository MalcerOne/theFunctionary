# Importing useful libraries
import time, os
from utils import Robot
from dotenv import load_dotenv, find_dotenv

# Defining some variables about the file
__author__ = "Rafael Malcervelli"
__version__ = "1.0.0"
__email__ = "r.malcervelli@gmail.com"

# ================ Main ================
def main():
    load_dotenv(find_dotenv())
    robot = Robot()
    try:
        robot.open_the_website()
        robot.search_for(os.environ.get("PHRASE"))
        time.sleep(1)
        robot.apply_filters(os.environ.get("SECTION"), int(os.environ.get("NUMBER_OF_MONTHS")))
        time.sleep(2)
        robot.get_all_articles()
        robot.export_to_excel()
        print("[+] Done! :)")

    except Exception as e:
        print(e)
        print("Something went wrong")
    finally:
        robot.browser_lib.close_all_browsers()
# ======================================

# Calling the main function
if __name__ == "__main__":
    main()