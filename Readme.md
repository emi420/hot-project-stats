# HOT Priority Regions and Impact Areas Stats

This is a Streamlit application that fetches and displays statistics related to HOT (Humanitarian OpenStreetMap Team) priority regions and impact areas. The application allows users to select hashtags, date ranges, intervals, priority regions, and impact areas, and then retrieves the corresponding data from the Ohsome API. https://stats.now.ohsome.org/

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- Python 3.x
- pandas
- streamlit
- requests

You can install the required Python packages using pip:
```bash
pip install pandas streamlit requests
```
This will start the Streamlit server and open the application in your default web browser.

## Using the Application

1. **Hashtag Input**: Enter one or more hashtags separated by commas (e.g., `hotosm,missingmaps`). These hashtags will be used to filter the data. Currently one hashtag per project is supported

2. **Date and Time Range**: Select the start and end dates for the desired date range.

3. **Interval**: Choose the desired interval for the data (hourly, daily, weekly, monthly, quarterly, or yearly).

4. **HOT-Priority-Regions**: Select one or more HOT priority regions from the dropdown menu. By default, the first region in the list is selected.

5. **HOT-Impact-Areas**: Select one or more HOT impact areas from the dropdown menu. By default, the first impact area in the list is selected.

6. **Get Statistics**: Click the "Get Statistics" button to fetch the data from the Ohsome API based on the selected options.

The application will display two sections:

- **Summary**: This section shows a summary of the data for the selected hashtags, date range, regions, and impact areas.
- **Interval Detail**: This section displays detailed data for the selected interval (e.g., hourly, daily, weekly) and other selected options.

## Customization

If you need to customize the application or the data sources, you can modify the `process.py` file, which contains the functions for fetching data from the Ohsome API. The file also includes dictionaries for the available HOT priority regions and impact areas.

## Contributing

Contributions to improve the application are welcome. If you find any issues or have suggestions for enhancements, please open an issue or submit a pull request.

## Author 
Kshitij Raj Sharma