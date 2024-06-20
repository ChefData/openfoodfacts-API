from classes.barcode_fetcher import BarcodeFetcher
from classes.product_fetcher import ProductFetcher
from IPython.display import HTML, display
from typing import List, Dict, Any
import pandas as pd


class FoodDataFrame:
    @staticmethod
    def path_to_image_html(path: str) -> str:
        """
        Converts a file path to HTML image tag.

        Args:
            path (str): The file path of the image.

        Returns:
            str: HTML image tag.
        """
        return f'<img src="{path}" style="max-height:124px;"/>'

    def __init__(self, num_barcodes: int = 10) -> None:
        """
        Initialises FoodDataFrame instance with a number of barcodes to fetch.

        Args:
            num_barcodes (int): Number of barcodes to fetch. Default is 10.
        """
        self.num_barcodes: int = num_barcodes
        self.barcodes: List[str] = BarcodeFetcher(num_barcodes).get_random_barcodes()
        self.food_data: List[Dict[str, Any]] = self._fetch_food_data()

    def _fetch_food_data(self) -> List[Dict[str, Any]]:
        """
        Fetches product information for each barcode.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing product information.
        """
        food_data_list: List[Dict[str, Any]] = []
        for product_number in self.barcodes:
            product_info: Dict[str, Any] = ProductFetcher.get_product(product_number)
            food_data_list.append(product_info)
        return food_data_list

    def create_dataframe(self) -> pd.DataFrame:
        """
        Creates a Pandas DataFrame from food data and applies image HTML formatting.

        Returns:
            pd.DataFrame: DataFrame containing food data.
        """
        food_data_df: pd.DataFrame = pd.DataFrame(self.food_data, columns=['barcode', 'name', 'brand', 'nutri_score', 'nova', 'nova_tag', 'energy', 'fat', 'salt', 'saturated', 'sugars', 'ingredients_n', 'ingredients', 'category', 'image'])
        food_data_df['image'] = food_data_df['image'].apply(self.path_to_image_html)
        return food_data_df
    
    @staticmethod
    def path_to_image_html(path: str) -> str:
        """
        Converts a file path to HTML image tag.

        Args:
            path (str): The file path of the image.

        Returns:
            str: HTML image tag.
        """
        return f'<img src="{path}" style="max-height:124px;"/>'

    @staticmethod
    def highlight_column(s: pd.Series) -> List[str]:
        """
        Highlights columns based on specified conditions.

        Args:
            s (pd.Series): Series representing a column in the DataFrame.

        Returns:
            List[str]: List of CSS strings for each cell in the column.
        """
        def column_color(val: Any) -> str:
            if val in [1, 'low', 'a']:
                return 'green'
            elif val == 'b':
                return 'lightgreen'
            elif val in [2, 'c']:
                return 'yellow'
            elif val in [3, 'moderate', 'd']:
                return 'orange'
            elif val in [4, 'high', 'e']:
                return 'red'
            else:
                return ''

        if s.name in ['nutri_score', 'nova', 'fat', 'salt', 'saturated', 'sugars']:
            return [f'background-color: {column_color(val)}' for val in s]
        return [''] * len(s)

    def display_table(self) -> None:
        """
        Displays the styled HTML table of food data.
        """
        styled_fooddex = self.create_dataframe().style.apply(self.highlight_column, axis=0)
        display(HTML(styled_fooddex.to_html(escape=False)))
