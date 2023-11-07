from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")


wait10 = WebDriverWait(driver, 10)

# Click the language select button
language = wait10.until(EC.presence_of_element_located((By.CLASS_NAME, "langSelectButton")))
language.click()

# Click the personal data button
try:
    personal_data = driver.find_element(By.CLASS_NAME, "fc-button-label")
    personal_data.click()
except NoSuchElementException:
    pass

# Click the big cookie
cookie = wait10.until(EC.presence_of_element_located((By.ID, "bigCookie")))


bool = True


def function():
    while bool:

        # How many cookies do we have
        cookies_string = driver.find_element(By.ID, 'cookies').text
        if "," in cookies_string:
            cookies_string = cookies_string.replace(",", "")
        cookies_number = re.search(r'\d+', cookies_string).group()


        # Price of the upgrades
        price = driver.find_elements(By.CLASS_NAME, 'price')
        price_list = price_f(price)

        #Buys every upgrade if it has enought money
        for i in range(len(price_list)):
            if int(cookies_number) >= price_list[i]:
                buy = driver.find_element(By.XPATH, f'//*[@id="product{i}"]')
                buy.click()

            else:
                end_time = time.time() + 5
                clicker(end_time)



# Function for price of the upgrades
def price_f(price):
    price_txt_list = []
    for i in price:
        text = i.text
        if "," in text:
            text = text.replace(",", "")
        price_txt_list.append(text)
    price_txt_list = list(filter(None, price_txt_list))
    price_list = [int(i) for i in price_txt_list]

    return price_list


# Runs the program to check for upgrades to buy every 5 seconds.
end_time = time.time() + 5
def clicker(end_time):
    while time.time() < end_time:
        cookie.click()
    function()

clicker(end_time)





