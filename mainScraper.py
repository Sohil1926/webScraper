import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Airtable setup
personal_access_token = 'patVnh56FVKpYUssq.46c740675ec2caf3ada99151efac8cb7870fa823fd67b2ee1d5bf3ce0fe257b4'
base_id = 'app11Wk2b9AkAnoLx'
table_name = 'Table 1'
airtable_url = f"https://api.airtable.com/v0/app11Wk2b9AkAnoLx/Table%201"

headers = {
    "Authorization": f"Bearer {personal_access_token}",
    "Content-Type": "application/json"
}

# Selenium setup
driver = webdriver.Chrome()
driver.get("https://www.ggcatering.com/venues#?venue_type=corporate&page=4")

wait = WebDriverWait(driver, 10)

# click only the first panel
first_panel = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "panel")))
first_panel.click()

# scrape the venue name
venue_name_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "article-heading")))
venue_name = venue_name_element.text

# insert venue name into Airtable
data = {
    "fields": {
        "Name": venue_name  # Ensure this matches the exact field label in Airtable
    }
}
response = requests.post(airtable_url, headers=headers, json=data)
if response.status_code == 200:
    print(f"Successfully added {venue_name} to Airtable.")
else:
    print(f"Failed to add {venue_name} to Airtable. Status Code: {response.status_code}, Response: {response.text}")

# Navigate back if necessary, or close the driver if done
driver.quit()

# Output the venue name
print(f"Venue Name: {venue_name}")
