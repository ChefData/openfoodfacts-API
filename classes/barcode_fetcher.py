from typing import List, Dict
import random
import requests


class BarcodeFetcher:
    def __init__(self, num_barcodes: int = 10) -> None:
        """
        Initialise the BarcodeFetcher with the number of barcodes to fetch.

        Args:
            num_barcodes (int): The number of barcodes to fetch. Default is 10.
        """
        self.num_barcodes: int = num_barcodes

    def get_random_barcodes(self) -> List[str]:
        """
        Fetches random barcodes from the Open Food Facts API.

        Returns:
            List[str]: A list of randomly selected barcodes. If the request fails
                       or not enough barcodes are available, returns an empty list or 
                       all available barcodes respectively.
        """
        # Define the URL for the Open Food Facts API
        url: str = "https://world.openfoodfacts.org/cgi/search.pl"
        
        # Set the parameters for the API request
        params: Dict[str, str | int | bool] = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "page_size": 1000,  # Maximum page size to get more variety
            "json": True  # Request JSON response
        }

        try:
            # Make the GET request to the API
            response: requests.Response = requests.get(url, params=params)
            # Raise an HTTPError for bad responses (4xx and 5xx status codes)
            response.raise_for_status()
        except requests.RequestException as e:
            # Print the error message and return an empty list if the request fails
            print(f"Failed to retrieve data: {e}")
            return []

        # Parse the JSON response and extract the list of products
        products: List[Dict[str, any]] = response.json().get('products', [])
        # Extract barcodes from products that have a 'code' field
        barcodes: List[str] = [product['code'] for product in products if 'code' in product]

        # Check if there are enough barcodes to sample the requested number
        if len(barcodes) < self.num_barcodes:
            # Print a message if not enough barcodes are found and return all available barcodes
            print(f"Not enough barcodes found. Only {len(barcodes)} available.")
            return barcodes

        # Randomly sample the requested number of barcodes from the list
        return random.sample(barcodes, self.num_barcodes)