# Review Evaluation Tool

A review application web app that analyzes reviews for authenticity and possible policy violations

## Features

- **Single Review Analysis**: Analyze individual reviews for legitimacy, sentiment, and policy violations.
- **CSV Dashboard Analysis**: Upload CSV files to generate comprehensive dashboards with insights on companies, ratings, classifications, and reviews.

## Project Structure

```
├── main.py                 # Main Flask application entry point
├── src/                    # Backend source code
│   ├── models/             # Database models and business logic
│   └── routes/             # API routes (review, user, dashboard)
├── static/                 # Frontend files (HTML, CSS, JavaScript)
├── database/               # SQLite database directory
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Installation & Setup

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    ```bash
    python main.py
    ```

## Usage

### Single Review Analysis
1.  Enter review text and optional details.
2.  Click "Analyze Review" to get insights.

### CSV Dashboard Analysis
1.  Navigate to the "CSV Dashboard" tab.
2.  Upload the provided CSV file (e.g., `sample_classifications.csv`) with columns like `review_text`, `rating`, `company`, `author`, `classification`.
3.  Click "Generate Dashboard" to view analytics.

## Technical Details

-   **Backend**: Flask (Python) for API and data processing.
-   **Frontend**: HTML, CSS, and JavaScript for the user interface.
-   **Database**: SQLite for local data storage.
-   **Data Analysis**: Pandas for CSV processing and dashboard insights.



