import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Airtable setup
personal_access_token = 'patVnh56FVKpYUssq.46c740675ec2caf3ada99151efac8cb7870fa823fd67b2ee1d5bf3ce0fe257b4'
base_id = 'app11Wk2b9AkAnoLx'
table_name = 'Table 1'
airtable_url = f"https://api.airtable.com/v0/app11Wk2b9AkAnoLx/Table%201"

headers = {
    "Authorization": f"Bearer {personal_access_token}",
    "Content-Type": "application/json"
}

def setup_selenium_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.ggcatering.com/venues#?venue_type=corporate&page=4")
    return driver


def fetch_venue_details(driver, panel):
    try:
        panel.click()
        wait = WebDriverWait(driver, 10)

        # Scrape venue details
        venue_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "article-heading"))).text
        short_description = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "markdown-content"))).text
        venue_stats_elements = driver.find_elements(By.CLASS_NAME, "venue-stat-number")
        stats = [int(element.text.replace(',', '')) for element in venue_stats_elements if element.text.isdigit()]

        reception_capacity = stats[0] if len(stats) > 0 else 0
        seated_capacity = stats[1] if len(stats) > 1 else 0
        theatre_capacity = stats[2] if len(stats) > 2 else 0

        address_container = driver.find_element(By.CLASS_NAME, "venue-info-item-content")
        address_full = address_container.text.split('\n')
        address = " ".join(address_full[1:3])

        info_items = driver.find_elements(By.CLASS_NAME, "venue-info-item-content")
        contact_name = "Contact name not found"
        if len(info_items) >= 2:
            contact_name_element = info_items[1]
            contact_name = contact_name_element.text.strip().split('\n')[0]

        email_link_element = driver.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
        email_address = email_link_element.get_attribute('href').replace('mailto:', '')

        phone_number = "Phone number not found"
        if contact_name != "Contact name not found":
            contact_info_lines = contact_name_element.text.split('\n')
            phone_number = contact_info_lines[1].strip() if len(contact_info_lines) > 1 else phone_number

        long_description = "Long description not found"
        description_elements = driver.find_elements(By.CLASS_NAME, "markdown-content")
        if len(description_elements) >= 2:
            long_description_element = description_elements[1]
            long_description = long_description_element.text

        venue_website_link_element = driver.find_element(By.XPATH, "//div[contains(., 'Venue Website')]/following-sibling::div/a")
        website = venue_website_link_element.get_attribute('href')

        image_elements = driver.find_elements(By.CSS_SELECTOR, "div.gallery-slide img")
        formatted_image_urls = [{"url": img.get_attribute('src')} for img in image_elements]

        return {
            "Name": venue_name,
            "Short Description": short_description,
            "Reception Capacity": reception_capacity,
            "Seated Capacity": seated_capacity,
            "Theatre Capacity": theatre_capacity,
            "Address": address,
            "Contact Name": contact_name,
            "Phone Number": phone_number,
            "Longer Description": long_description,
            "Website": website,
            "Contact Email": email_address,
            "Images": formatted_image_urls
        }

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error fetching details for a panel: {e}")
        return None

def post_to_airtable(data):
    response = requests.post(airtable_url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully added {data['fields']['Name']} to Airtable.")
    else:
        print(f"Failed to add {data['fields']['Name']} to Airtable. Status Code: {response.status_code}, Response: {response.text}")

def main():
    driver = setup_selenium_driver()
    wait = WebDriverWait(driver, 10)
    try:
        panels = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel")))
        for panel in panels:
            venue_data = fetch_venue_details(driver, panel)
            if venue_data:
                post_to_airtable({"fields": venue_data})
            driver.back()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()