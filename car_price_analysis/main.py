from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime

today_date = datetime.today().date()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://autogidas.lt/")

actions = ActionChains(driver)

wait10 = WebDriverWait(driver, 10)

# Accept cookies if the popup is present
try:
    cookies = wait10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
    cookies.click()
except:
    pass

brand = input("Select the car brand: ").lower()
model = input("Select the car model: ").lower()
year_from = input("Enter the starting year: ")
ending_year = input("Enter the ending year: ")

# Select brand
brand_x = wait10.until(EC.presence_of_element_located((By.XPATH, '//*[@id="f_1"]/div[2]')))
brand_x.click()

looking_brands = wait10.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'value-title')))
auto_x = [i.text.lower() for i in looking_brands]

index = 0
if brand in auto_x :
    index = auto_x.index(brand)

driver.execute_script("arguments[0].scrollIntoView(true);", looking_brands[index])
wait10.until(EC.element_to_be_clickable((By.CLASS_NAME, 'value-title')))
looking_brands[index].click()

# Select model
time.sleep(2) # Add a delay to allow the page to load
model_elements = driver.find_elements(By.CSS_SELECTOR, ".main.value.simple.show .value-title")
models = [element.text.lower() for element in model_elements]

index_x = 0
if model in models:
    index_x = models.index(model)

model_elements[index_x].click()

# Select starting year
year_elements = driver.find_element(By.ID, "f_41")
options = [option.get_attribute('value') for option in year_elements.find_elements(By.TAG_NAME, 'option')]

if year_from in options:
    index_y = options.index(year_from)
year_elements.find_elements(By.TAG_NAME, 'option')[index_y].click()

# Select ending year
ending_year_elements = driver.find_element(By.ID, "f_42")
options_x = [option.get_attribute('value') for option in ending_year_elements.find_elements(By.TAG_NAME, 'option')]

if ending_year in options_x:
    index_z = options_x.index(ending_year)
ending_year_elements.find_elements(By.TAG_NAME, 'option')[index_z].click()

# Click search button
search = driver.find_element(By.CLASS_NAME, "submit-button-container ")
search.click()

# Scroll to the end of the page
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
time.sleep(2)


price_list = []
more_pages = True
while more_pages:
    # Wait for car price elements to load
    car_price_elements = wait10.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-price")))

    for i in car_price_elements:
        price_list.append(i.text)

    try:
        # Check if the "forward" button is present
        forward_button = driver.find_element(By.XPATH, "//a[@rel='next']")
        # Use JavaScript to click the "next" button
        driver.execute_script("arguments[0].click();", forward_button)
        # Wait for a bit to let the new page load
        time.sleep(3)
    except:
        # If the "forward" button is not present, set the flag to False to exit the loop
        more_pages = False
        break

# Check if there are cars to scrape
if not price_list:
    print("No cars found for the given criteria.")
else:
    # Convert prices to integers
    price_list = [int(price.replace(" ", "").replace("€", "")) for price in price_list]
    # Find the largest, smallest, and average prices
    largest_price = max(price_list)
    smallest_price = min(price_list)
    average_price = sum(price_list) / len(price_list)

    with open("car_prices.txt", "w") as file:
        file.write(f"Date: {today_date}\n\n")
        file.write("Car Information:\n")
        file.write(f"  Brand: {brand.capitalize()}\n")
        file.write(f"  Model: {model.capitalize()}\n")
        file.write(f"  Starting Year: {year_from}\n")
        file.write(f"  Ending Year: {ending_year}\n\n")
        file.write("Price Statistics:\n")
        file.write(f"  Largest Price: € {largest_price}\n")
        file.write(f"  Smallest Price: € {smallest_price}\n")
        file.write(f"  Average Price: € {round(average_price, 2)}")

driver.quit()




