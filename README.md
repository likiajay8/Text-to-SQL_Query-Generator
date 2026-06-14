# Text-to-SQL Converter

A simple beginner-friendly Streamlit web application that converts plain English questions into SQLite SQL queries using the Google Gemini API.

The app uses:

- Python
- Streamlit
- SQLite
- Pandas
- Google Gemini API
- Google Gen AI Python SDK
- Environment variables for the API key

## Project Files

- `app.py` - Streamlit web application.
- `create_database.py` - Creates and populates the sample SQLite database.
- `requirements.txt` - Python dependencies.
- `.env.example` - Example environment variable file.
- `employees.db` - Generated SQLite database after running `create_database.py`.

## Sample Database

The database contains 2 tables:

- `employees`
- `departments`

The tables include columns such as:

- `employee_id`
- `name`
- `department_id`
- `department_name`
- `salary`
- `city`
- `manager_name`
- `office_city`
- `annual_budget`

Because employees are linked to departments using `department_id`, you can ask questions that require joins.

Example questions:

- Show all employees from the IT department
- List employee names with their department names
- Which employees earn more than 80000?
- Show employees, salaries, and department managers
- List employees who work in departments based in Hyderabad

## Step-by-Step Setup Instructions

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

Copy `.env.example` and rename the copy to `.env`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

On macOS or Linux:

```bash
cp .env.example .env
```

### 4. Add your Gemini API key

Open the new `.env` file and replace the placeholder value with your real Gemini API key.

### 5. Create the sample SQLite database

```bash
python create_database.py
```

This creates an `employees.db` file in the project folder.

### 6. Run the Streamlit app

```bash
streamlit run app.py
```

Streamlit will show a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

## How to Use the App

1. Enter a plain English question in the text box.
2. Click **Generate SQL Query**.
3. Review the generated SQL query.
4. Click **Run Query** to run the generated query.
5. View the results in the table below the query.

The **Run Query** button is disabled until a SQL query has been generated.

For safety, the app can generate SQL such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, or `PRAGMA`, but it will not run those queries. Only safe `SELECT` queries are allowed to run against the database.

## Error Handling Included

The app handles:

- Empty user input
- Missing database file
- Missing Gemini API key
- Gemini API errors
- Empty Gemini responses
- Unsafe non-SELECT SQL queries are displayed but blocked from running
- SQLite query errors
- Empty query results

## Where to Paste Your Gemini API Key

Edit this file:

```text
.env
```

If `.env` does not exist yet, create it by copying `.env.example`.

In `.env`, modify line 1:

```text
GEMINI_API_KEY=paste_your_gemini_api_key_here
```

Replace only the text after the equals sign with your real Gemini API key.

For example:

```text
GEMINI_API_KEY=YOUR_REAL_GEMINI_API_KEY
```

Do not paste your API key into `app.py`, `create_database.py`, or `README.md`.
