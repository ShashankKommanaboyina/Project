import requests
import streamlit as st

def get_product_info(barcode):
    """Fetches comprehensive product information from Open Food Facts API (v2).

    Args:
        barcode (str): The barcode of the product to retrieve information for.

    Returns:
        dict (or None): A dictionary containing product details if found, or None
                         if the API request fails or product is not found.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
    """

    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()

        if data['status'] == 1:  # Product found
            product = data['product']

            # Extract product details
            product_info = {
                "product_name": product.get('product_name', 'No name available'),
                "brand": product.get('brands', 'No brand available'),
                "generic_name": product.get('generic_name', 'No description available'),
                "image_url": product.get('image_url', None),
                "ingredients": product.get('ingredients', None),
                "allergens": product.get('allergens', None),
                "categories": product.get('categories', None),
                "labels": product.get('labels', None),
                # Include additional fields as needed
                # ...
            }

            # Extract all nutritional values dynamically
            nutrients = product.get('nutriments', {})
            product_info["nutritional_info"] = {}
            for key, value in nutrients.items():
                if '_100g' in key:
                    formatted_key = key.replace('_100g', '').replace('_', ' ').capitalize()
                    product_info["nutritional_info"][formatted_key] = value

            return product_info

        else:
            print(f"Product not found in Open Food Facts database.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def generate_insight(product_info, user_preferences):
    """Generates insights about a product based on its nutritional data and user preferences.

    Args:
        product_info (dict): A dictionary containing product information, as returned by get_product_info().
        user_preferences (str): A string representing user preferences.

    Returns:
        str: A string containing the generated insights.
    """

    # Extract product name and nutritional data from product_info
    product_name = product_info.get('product_name', 'No name available')
    nutritional_data = product_info.get('nutritional_info', {})

    # Combine the product name and nutritional data into a prompt
    prompt = f"The product '{product_name}' has the following nutritional information:\n"
    for key, value in nutritional_data.items():
        prompt += f"{key}: {value}\n"
   


    # Add user preferences
    if user_preferences:
        prompt += f"\nBased on the following preferences: {user_preferences}, can you provide insights on whether this product is a good choice for health and sustainability?"

    # Use the LLaMA model to generate insights
    insights = pipe(prompt, max_length=2000)

    # Return the generated text
    return insights[0]['generated_text']

# # Example usage
# barcode = "YOUR_BARCODE_HERE"  # Replace with the actual barcode
product_data = get_product_info(barcode)

if product_data:
    user_preferences = "I prefer low-sugar, low-sodium products and want to avoid high-sugar drinks."
    insight_text = generate_insight(product_data, user_preferences)
    print(insight_text)
else:
    print("\nNo product data retrieved.")