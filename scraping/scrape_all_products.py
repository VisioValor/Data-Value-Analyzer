import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Load the CSV file containing the search URLs
file_path = 'all_datasets.csv'  # Adjust the file name if necessary
urls_data = pd.read_csv(file_path)

# List to hold the metadata for each dataset
all_data = []

# Add headers to simulate a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# Iterate through each search URL
for index, row in urls_data.iterrows():
    base_url = row['Search URL']
    page_number = 1

    print(f"Processing category: {row['Category Name']}")

    while True:
        # Construct the URL for the current page
        url = f"{base_url}&page={page_number}"
        
        # Send a GET request to fetch the page content with headers
        response = requests.get(url, headers=headers)
        time.sleep(4)  # Wait to avoid overloading the server
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product cards
        product_cards = soup.find_all('a', class_='product-card--horizontal')
        
        # If no products are found, break the loop
        if not product_cards:
            print(f"No more products found for {row['Category Name']}.")
            break

        # Extract product details
        for card in product_cards:
            product_url = card['href']
            if not product_url.startswith('http'):
                product_url = f"https://datarade.ai{product_url}"
            
            product_response = requests.get(product_url, headers=headers)
            time.sleep(2)  # Wait to avoid overloading the server
            product_soup = BeautifulSoup(product_response.content, 'html.parser')

            # Extract dataset metadata
            title = product_soup.find('h1', class_='product-hero__header-content-title-name').text.strip() if product_soup.find('h1', class_='product-hero__header-content-title-name') else 'N/A'

            volume = product_soup.find('div', class_='dataset__fact-name', string=lambda text: text and text.strip() == 'Volume')
            volume = volume.find_next('div', class_='dataset__fact-value').text.strip() if volume else 'N/A'

            data_quality = product_soup.find('div', class_='dataset__fact-name', string=lambda text: text and text.strip() == 'Data Quality')
            data_quality = data_quality.find_next('div', class_='dataset__fact-value').text.strip() if data_quality else 'N/A'

            avail_formats = product_soup.find('div', class_='dataset__fact-name', string=lambda text: text and text.strip() == 'Avail. Formats')
            avail_formats = avail_formats.find_next('div', class_='dataset__fact-value').text.strip() if avail_formats else 'N/A'

            coverage = product_soup.find('div', class_='dataset__fact-name', string=lambda text: text and text.strip() == 'Coverage')
            coverage = coverage.find_next('div', class_='dataset__fact-value').text.strip() if coverage else 'N/A'

            history = product_soup.find('div', class_='dataset__fact-name', string=lambda text: text and text.strip() == 'History')
            history = history.find_next('div', class_='dataset__fact-value').text.strip() if history else 'N/A'

            pricing = product_soup.find('div', class_='pricing-plan__quote')
            pricing = pricing.text.strip() if pricing else 'N/A'

            # Append the metadata to the list
            all_data.append({
                'Category': row['Category Name'],
                'Title': title,
                'Volume': volume,
                'Data Quality': data_quality,
                'Available Formats': avail_formats,
                'Coverage': coverage,
                'History': history,
                'Pricing': pricing
            })
            print(f"Processed: {title}")

        # Move to the next page
        page_number += 1
        print(f"Page {page_number - 1} done.")

        # Check for pagination to stop at the last page
        pagination = soup.find('div', class_='dtrd-menu pagination')
        if pagination:
            max_page_number = int(pagination.find_all('a')[-2].text)
            if page_number > max_page_number:
                print(f"End of pages for {row['Category Name']}.")
                break

# Save the data to a CSV file
output_file = 'datasets_metadata_all_categories.csv'
df = pd.DataFrame(all_data)
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")
