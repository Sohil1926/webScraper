from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.ggcatering.com/venues#?venue_type=corporate&page=4")

# wait for the element to be clickable
wait = WebDriverWait(driver, 10)
panel = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "panel")))

panel.click()

venue_name_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "article-heading"))
)
venue_name = venue_name_element.text  


# Output
print(f"Venue Name: {venue_name}")

# Close the browser when done
driver.quit()