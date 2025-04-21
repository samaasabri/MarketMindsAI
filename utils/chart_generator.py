import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO

sns.set(style="darkgrid")

def generate_bar_chart(data, title="Bar Chart", xlabel="", ylabel=""):
    """
    Generates a bar chart based on the provided data.

    Parameters:
    - data (dict or pd.DataFrame): The data to plot. If a dictionary is provided, it is 
      assumed to be in the format {'label': value}.
    - title (str): Title of the bar chart (default is 'Bar Chart').
    - xlabel (str): Label for the x-axis (default is the column name).
    - ylabel (str): Label for the y-axis (default is the column name).

    Returns:
    - matplotlib.figure.Figure: The generated figure object containing the bar chart.

    Raises:
    - ValueError: If the data is not a dictionary or DataFrame.
    """
    try:
        # Handle dict input
        if isinstance(data, dict):
            df = pd.DataFrame(list(data.items()), columns=["Company", "Score"])
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError("Input data must be either a dictionary or a pandas DataFrame.")

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=df.columns[0], y=df.columns[1], data=df, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(xlabel or df.columns[0])
        ax.set_ylabel(ylabel or df.columns[1])

        return fig
    except Exception as e:
        raise ValueError(f"Error generating bar chart: {e}")

def generate_line_chart(data, title="Line Chart", xlabel="", ylabel=""):
    """
    Generates a line chart based on the provided data.

    Parameters:
    - data (pd.DataFrame or dict): The data to plot. Data should be in a DataFrame format or 
      a dictionary format where keys represent the x-values and values represent the y-values.
    - title (str): Title of the line chart (default is 'Line Chart').
    - xlabel (str): Label for the x-axis (default is 'Time').
    - ylabel (str): Label for the y-axis (default is 'Value').

    Returns:
    - matplotlib.figure.Figure: The generated figure object containing the line chart.

    Raises:
    - ValueError: If the data is not a pandas DataFrame or dictionary.
    """
    try:
        if isinstance(data, dict):
            data = pd.DataFrame(list(data.items()))

        elif not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be either a dictionary or a pandas DataFrame.")

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.lineplot(data=data, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(xlabel or "Time")
        ax.set_ylabel(ylabel or "Value")

        return fig
    except Exception as e:
        raise ValueError(f"Error generating line chart: {e}")

def generate_pie_chart(data, title="Pie Chart"):
    """
    Generates a pie chart based on the provided data.

    Parameters:
    - data (dict): A dictionary where keys are the labels and values are the sizes.
    - title (str): Title of the pie chart (default is 'Pie Chart').

    Returns:
    - matplotlib.figure.Figure: The generated figure object containing the pie chart.

    Raises:
    - ValueError: If the data is not a dictionary.
    """
    try:
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary.")

        labels = list(data.keys())
        sizes = list(data.values())
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.set_title(title)

        return fig
    except Exception as e:
        raise ValueError(f"Error generating pie chart: {e}")
