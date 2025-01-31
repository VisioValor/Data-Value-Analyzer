from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# URL for the main data products page (replace with the correct URL)
data_products_url = "https://datarade.ai/data-products"

# Initialize the WebDriver (ensure chromedriver is in your PATH)
driver = webdriver.Chrome()

# Open the data products page
driver.get(data_products_url)

# Allow time for the page to load
time.sleep(5)  # Adjust this as necessary

# Find all product links (adjust the selector based on actual page structure)
product_links = driver.find_elements(By.CSS_SELECTOR, 'a.product-link')  # Replace with correct selector if needed

# Extract URLs for each data product
product_urls = []
for link in product_links:
    href = link.get_attribute('href')
    product_urls.append({'Product URL': href})

# Close the WebDriver
driver.quit()

# Create a DataFrame from the product URLs
df = pd.DataFrame(product_urls)

# Save the DataFrame to a CSV file
df.to_csv('all_data_products.csv', index=False)
print("All data product URLs have been saved to all_data_products.csv")