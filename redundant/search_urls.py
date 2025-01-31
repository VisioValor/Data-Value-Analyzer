import pandas as pd

# Load the input CSV file
file_path = 'data_categories.csv'  # Replace with the actual file name
data = pd.read_csv(file_path)

# Function to create URLs based on the specified format
def create_search_url(category_name):
    keywords = category_name.replace("-", "+").title()
    return f"https://datarade.ai/search/products?keywords={keywords}"

# Generate the new URLs
data['Search URL'] = data['Category Name'].apply(create_search_url)

# Save the updated DataFrame to a new CSV file
output_path = 'all_datasets.csv'  # Replace with desired output file name
data.to_csv(output_path, index=False)

print(f"URLs generated and saved to {output_path}")
