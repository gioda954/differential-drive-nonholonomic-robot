# Simple Calculator Web App

This project contains a lightweight Flask web application that provides a simple calculator. Users can perform addition, subtraction, multiplication, and division directly from their browser.

## Getting started

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   flask --app app run
   ```

   The calculator will be available at <http://127.0.0.1:5000>.

## Running tests

Execute the unit tests with:

```bash
pytest
```

## Project structure

```
app/
├── __init__.py        # Flask application factory
├── routes.py          # Calculator routes and logic
├── static/
│   └── styles.css     # Styling for the calculator UI
└── templates/
    └── calculator.html  # HTML template for the calculator page
requirements.txt        # Python dependencies
app.py                  # Local development entry point
```
