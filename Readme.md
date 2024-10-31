# HOT Projects Stats

This is a Streamlit application that fetches and displays statistics related to HOT (Humanitarian OpenStreetMap Team) projects and hashtagss. The application allows users to select a date range and then copy&paste Id, Name and Hashtag directly from a spreadsheet table, receiving corresponding data from [Ohsome API](https://stats.now.ohsome.org/). Other sources, like HOT Tasking Manager, will be added soon.

<img width="692" alt="Screenshot 2024-10-31 at 12 12 47" src="https://github.com/user-attachments/assets/f9ce9aa9-63f3-4418-b0da-d0055c0461ca">

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

## Start

```bash
streamlit run streamlit_app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Using the Application

1. **Date and Time Range**: Select the start and end dates for the desired date range.

2. **Table**: Input Id, Name and Hashtag (required). You can copy&past your data directly from a spreadsheet table.

3. **Get Statistics**: Click the "Get Statistics" button to fetch the data from the APIs based on the selected options.

The application will display two sections:

- **Summary**: This section shows a summary of the data for the selected options.

## Contributing

Contributions to improve the application are welcome. If you find any issues or have suggestions for enhancements, please open an issue or submit a pull request.

## Authors 

Emilio Mariscal, based on the [HOT Priority Regions and Impact Areas Stats](https://github.com/kshitijrajsharma/ohsome-now-stats-multiple-hashtags) app by Kshitij Raj Sharma.

