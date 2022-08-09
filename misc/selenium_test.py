# Import Selenium and select function for dropdowns
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# Infinite loop
while True:

    # Try / except in case the page doesn't properly load
    try:

        # Set driver (Chrome 104 driver must be in PATH environment variable)
        driver = webdriver.Chrome()

        # Print Status
        print("Opening page...")

        # Open the target website
        driver.get("https://amazon.com")

        # Pause driver for a moment to let the site load
        driver.implicitly_wait(10)

        # Print Status
        print("Entering Search Info...")

        # Select the "Electronics" category
        select_element = driver.find_element(By.ID,'searchDropdownBox')
        select_object = Select(select_element)
        select_object.select_by_value('search-alias=electronics')

        # Enter Text in Search Box
        search_box = driver.find_element(by=By.ID, value="twotabsearchtextbox")
        search_box.send_keys("Dope Watches")

        # Click the search button
        search_button = driver.find_element(by=By.ID, value="nav-search-submit-button")
        search_button.click()

        # Sleep three seconds to show the result
        time.sleep(3)

        # Print Status
        print("Closing Current Session.  Next Session will begin in 5 seconds.\n")

        # Close the driver
        driver.quit()

    except:

        # Print Status
        print("Error in main loop.  Restarting...\n")

    # Put python to sleep until it's time to check again
    # Set the frequency the loop will run in seconds
    time.sleep(5)
