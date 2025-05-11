# DEI in Tech Climate Survey Interactive Report - Python Version

This is a Python implementation of the DEI in Tech Climate Survey Interactive Report, originally built in R Shiny. The application uses Streamlit for the web interface and Plotly for interactive visualizations.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure

```
python_app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── data/              # Data files
├── utils/             # Utility modules
│   ├── data_loader.py    # Data loading and processing
│   └── visualization.py  # Plot creation functions
└── static/            # Static assets
```

## Features

- Interactive data visualization
- Demographic breakdowns
- Survey response analysis
- Build-a-Graph functionality
- Year-over-year comparisons

## Data Processing

The application processes survey data from the original R data files and converts them into a format suitable for Python visualization. The data processing pipeline includes:

1. Loading R data files
2. Converting to pandas DataFrames
3. Processing demographic data
4. Creating visualization-ready datasets

## Visualization Types

- Bar charts for demographic data
- Pie charts for proportion visualization
- Box plots for adjective ratings
- Grouped bar charts for survey responses
- Proportion plots for response breakdowns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 