from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.ggcatering.com/venues#?venue_type=corporate&page=4")

wait = WebDriverWait(driver, 10)
venue_names = []

# initial list of panels
panels = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel")))

for i in range(len(panels)):
    panels = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel")))
    panels[i].click()

    # wait for the venue name to load on the new page
    venue_name_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "article-heading")))
    venue_names.append(venue_name_element.text)

    # navigate back to main page
    driver.back()

# Output 
for name in venue_names:
    print(f"Venue Name: {name}")

driver.quit()
