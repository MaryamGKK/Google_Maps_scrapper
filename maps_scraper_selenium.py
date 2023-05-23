#Importing libraries 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time 
import os

class MapsScraper():
    
    def __init__(self):
        # Universal storage path
        self.__storage_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'data', 'scraped_data').replace('\\scrapers', '')
        # Specify the path to chromedriver.exe
        self.__webdriver_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'chromedriver.exe')
        # Drivers options
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(self.__webdriver_path, options=self.chrome_options)
        #Loading Selenium Webdriver 
        wait = WebDriverWait(self.driver, 5)

    def get_address(self, location = 'Egypt', query = "el sallam shopping center", n_results=None):
        
        '''
        parameters: location, name of the place, num_results
        return : list of first 6 search results from google maps [[name, longitude, latitude, address]]
        '''
        #Opening Google maps 
        self.driver.get("https://www.google.com/maps")
        time.sleep(5)
        
        searchBox=self.driver.find_element('xpath', '/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/form/input[1]')
        searchBox.send_keys(location)
        searchBox.send_keys(Keys.ENTER)
        time.sleep(2)

        cancelButton=self.driver.find_element('xpath', '/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/div[3]/button')
        cancelButton.click()

        searchBox.send_keys(query)
        searchBox.send_keys(Keys.ENTER)
        time.sleep(3)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        SCROLL_PAUSE_TIME = 5
        number = 1

        time.sleep(2)
        while True:
            number = number+1

            # Scroll down to bottom
            xpath = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
            element = self.driver.find_element('xpath', xpath)
            self.driver.execute_script('arguments[0].scrollBy(0, 5000);', element)

            # Wait to load page

            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            print(f'last height: {last_height}')

            element = self.driver.find_element('xpath', xpath)

            new_height = self.driver.execute_script("return arguments[0].scrollHeight", element)

            print(f'new height: {new_height}')
            
            if n_results:

                if number == n_results//7:
                    break

            if new_height == last_height:
                break

            print('cont')
            last_height = new_height

        entries = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')[:-1]
        result = [] 
        
        #Extracting the information from the results  
        for entry in entries:

            place_link = entry.get_attribute('href')
            link_data = str(place_link).split('!')
            long = float([s for s in link_data if s.startswith('3d')][0][2:])
            lat = float([s for s in link_data if s.startswith('4d')][0][2:])

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(place_link)
            time.sleep(3)
            try:
                name = self.driver.find_element('xpath', '/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div/div[2]/form/input[1]').text
            except:
                pass

            button = None
            address = None

            try:
                button = self.driver.find_element('xpath', '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button')
            except:
                pass
            try:
                button = self.driver.find_element('xpath', '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[5]/div[1]/button')
            except:
                pass
            if button:
                button.click()
                time.sleep(5)
                try:
                    address = self.driver.find_element('xpath', '/html/body/div[3]/div[9]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input').get_attribute('aria-label')
                except:
                    pass

            place = []
            place.append(name)
            place.append(address)
            place.append(long)
            place.append(lat)
            result.append(place)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        print(len(result))
        return result
    
def main():
    
    mScraper = MapsScraper()
    print(mScraper.get_address())

if __name__ == "__main__":
    main()