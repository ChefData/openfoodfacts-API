from typing import List, Dict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class FoodCharts:
    def __init__(self, food_data_df: pd.DataFrame) -> None:
        """
        Initialises FoodCharts instance with food data DataFrame.

        Args:
            food_data_df (pd.DataFrame): DataFrame containing food data.
        """
        self.food_data_df: pd.DataFrame = food_data_df

    def plot_2d_scatter(self) -> None:
        """
        Plots 2D scatter plot of energy against number of ingredients with NOVA score as colours.
        """
        plt.figure(figsize=(10, 8))

        # Define colours for each NOVA score category
        nova_color_map: Dict[str, str] = {
            '1': 'green',
            '2': 'yellow',
            '3': 'orange',
            '4': 'red',
            'unknown': 'gray'
        }

        # Clean up NOVA scores and map to colours
        self.food_data_df['nova'] = self.food_data_df['nova'].astype(str).str.split('.').str[0]
        color_list: List[str] = self.food_data_df['nova'].map(nova_color_map).fillna('gray')

        plt.scatter(self.food_data_df['ingredients_n'], self.food_data_df['energy'], c=color_list, s=80, edgecolors='k', alpha=0.8)

        plt.xlabel('Number of Ingredients')
        plt.ylabel('Energy (kcal/100g)')
        plt.title('Energy vs Number of Ingredients (Coloured by NOVA Score)')

        legend_elements = [plt.Line2D([0], [0], marker='o', color=color, label=nova, markersize=10) for nova, color in nova_color_map.items()]
        plt.legend(handles=legend_elements, title='NOVA Score', loc='upper right')

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_bar_chart(self, x_column: str, y_column: str, title: str, xlabel: str, ylabel: str) -> None:
        """
        Plots a bar chart based on specified columns.

        Args:
            x_column (str): Column name for x-axis.
            y_column (str): Column name for y-axis.
            title (str): Title of the chart.
            xlabel (str): Label for x-axis.
            ylabel (str): Label for y-axis.
        """
        plt.figure(figsize=(12, 8))
        
        # Use seaborn for more aesthetic plots
        sns.set_theme(style="whitegrid")
        bar_plot = sns.barplot(x=self.food_data_df[x_column], y=self.food_data_df[y_column], palette="viridis", hue=self.food_data_df[x_column], legend=False)
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=90)        
        plt.tight_layout()
        plt.show()

    def plot_pie_chart(self, column: str, title: str) -> None:
        """
        Plots a pie chart based on specified column.

        Args:
            column (str): Column name for the pie chart.
            title (str): Title of the chart.
        """
        plt.figure(figsize=(8, 8))

        # Define colours for Nutri-Score categories
        nutri_color_map: Dict[str, str] = {
            'a': 'green',
            'b': 'lightgreen',
            'c': 'yellow',
            'd': 'orange',
            'e': 'red'
        }

        # Calculate value counts and sort them by Nutri-Score order
        value_counts = self.food_data_df[column].str.lower().value_counts()
        labels = ['a', 'b', 'c', 'd', 'e']
        sizes = [value_counts.get(label, 0) for label in labels]
        color_list: List[str] = [nutri_color_map.get(label, 'gray') for label in labels]

        # only "explode" the 1st slice
        explode = (0.1, 0, 0, 0, 0)

        plt.pie(sizes, explode=explode, labels=labels, colors=color_list, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title(title)
        plt.show()

    def plot_histogram(self, column: str, title: str, xlabel: str, ylabel: str) -> None:
        """
        Plots a histogram based on specified column.

        Args:
            column (str): Column name for the histogram.
            title (str): Title of the chart.
            xlabel (str): Label for x-axis.
            ylabel (str): Label for y-axis.
        """
        plt.figure(figsize=(12, 8))

        # Drop NaN values from the column to be plotted
        column_data = self.food_data_df[column].dropna()

        # Use seaborn for more aesthetic plots
        sns.set_theme(style="whitegrid")
        hist_plot = sns.histplot(column_data, bins=10, kde=True, color='blue', edgecolor='black')
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_data(self) -> None:
        """
        Plots based on food data.
        """
        self.plot_2d_scatter()
        self.plot_bar_chart('brand', 'energy', 'Energy Content by Brand', 'Brand', 'Energy (kcal/100g)')
        self.plot_pie_chart('nutri_score', 'Distribution of Nutri-Score')
        self.plot_histogram('energy', 'Energy Content Distribution', 'Energy (kcal/100g)', 'Frequency')
