import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL for the main categories page
categories_url = "https://datarade.ai/data-categories"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# Send a GET request to the categories page with headers
response = requests.get(categories_url, headers=headers)
if response.status_code != 200:
    print(f"Failed to retrieve the categories page. Status code: {response.status_code}")
    exit()

# Parse the HTML content of the categories page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all category links
category_links = soup.find_all('a', href=True)

# Extract category names and URLs
categories_data = []
for link in category_links:
    href = link.get('href')
    if href and 'data-categories' in href:
        if not href.startswith('http'):
            href = f"https://datarade.ai{href}"
        # Ensure the URL ends with '/datasets'
        if not href.endswith('/datasets'):
            href = f"{href.rstrip('/')}/datasets"
        # Extract category name as the last part of the original URL
        category_name = href.split('/')[-2]  # Get the last part before '/datasets'
        categories_data.append({'Category Name': category_name, 'Category URL': href})

# Create a DataFrame from the category data
df = pd.DataFrame(categories_data)

# Save the DataFrame to a CSV file
df.to_csv('data_categories.csv', index=False)
print("Categories have been saved to data_categories.csv")