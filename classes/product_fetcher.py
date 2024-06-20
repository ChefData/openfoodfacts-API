from typing import Dict, Any
import numpy as np
import requests


class ProductFetcher:
    @staticmethod
    def get_product(product_number: str) -> Dict[str, Any]:
        """
        Fetches product details from the Open Food Facts API based on the given product number.

        Args:
            product_number (str): The product number or barcode to fetch details for.

        Returns:
            dict: A dictionary containing product details such as barcode, name, brand, nutrition information,
                  ingredients, category, and image URL. Returns NaN for missing data or 'Error' if fetching fails.
        """
        url: str = f'https://world.openfoodfacts.org/api/v3/product/{product_number}/'

        try:
            # Make the GET request to fetch product details
            response: requests.Response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
            # Parse the JSON response
            food_product: Dict[str, Any] = response.json()
            
            # Extract relevant fields from the JSON response
            product_id: str = food_product['code']
            product_name: str = food_product['product'].get('product_name', np.nan)
            brands: str = food_product['product'].get('brands', np.nan)
            nutri_score: str = food_product['product'].get('nutriscore_grade', np.nan)
            nova_groups: str = food_product['product'].get('nova_group', np.nan)
            nova_groups_tags: str = food_product['product'].get('nova_groups_tags', np.nan)
            energy: float = food_product['product']['nutriments'].get('energy-kcal_100g', np.nan)
            fat: str = food_product['product']['nutrient_levels'].get('fat', np.nan)
            salt: str = food_product['product']['nutrient_levels'].get('salt', np.nan)
            saturated: str = food_product['product']['nutrient_levels'].get('saturated-fat', np.nan)
            sugars: str = food_product['product']['nutrient_levels'].get('sugars', np.nan)
            ingredients_n: int = food_product['product'].get('ingredients_n', np.nan)
            ingredients: str = food_product['product'].get('ingredients_text_en', np.nan)
            category: str = food_product['product'].get('categories', np.nan)
            image_url: str = food_product['product'].get('image_front_small_url', np.nan)
            
            # Return a dictionary with extracted product details
            return {
                'barcode': product_id,
                'name': product_name,
                'brand': brands,
                'nutri_score': nutri_score,
                'nova': nova_groups,
                'nova_tag': nova_groups_tags,
                'energy': energy,
                'fat': fat,
                'salt': salt,
                'saturated': saturated,
                'sugars': sugars,
                'ingredients_n': ingredients_n,
                'ingredients': ingredients,
                'category': category,
                'image': image_url
            }
        
        except requests.exceptions.RequestException as e:
            # Handle request exceptions (e.g., network issues, bad request)
            print(f"Error fetching details for product {product_number}: {e}")
            # Return NaN for all fields to indicate an error
            return {
                'barcode': 'Error',
                'name': np.nan,
                'brand': np.nan,
                'nutri_score': np.nan,
                'nova': np.nan,
                'nova_tag': np.nan,
                'energy': np.nan,
                'fat': np.nan,
                'salt': np.nan,
                'saturated': np.nan,
                'sugars': np.nan,
                'ingredients_n': np.nan,
                'ingredients': np.nan,
                'category': np.nan,
                'image': np.nan
            }
