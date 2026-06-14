import os
import re
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "employees.db"


def load_database_schema() -> str:
    """Return table and column details for the Gemini prompt."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            "employees.db was not found. Run `python create_database.py` first."
        )

    with sqlite3.connect(DATABASE_PATH) as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
            conn,
        )

        schema_lines = []
        for table_name in tables["name"]:
            columns = pd.read_sql_query(f"PRAGMA table_info({table_name});", conn)
            column_list = ", ".join(
                f"{row['name']} {row['type']}" for _, row in columns.iterrows()
            )
            schema_lines.append(f"{table_name}({column_list})")

    return "\n".join(schema_lines)


def build_prompt(question: str, schema: str) -> str:
    return f"""
You are a helpful Text-to-SQL assistant.
Convert the user's plain English question into one valid SQLite query.

Database schema:
{schema}

Rules:
- Return only one SQL query.
- Use SQLite syntax.
- Do not wrap the answer in markdown or code fences.
- Use clear JOINs when data from multiple tables is needed.
- If the user asks to add, update, delete, create, alter, or drop data, generate the matching SQL query only.
- Do not explain the query.

User question:
{question}
""".strip()


def clean_sql_response(response_text: str) -> str:
    cleaned = response_text.strip()
    cleaned = re.sub(r"^```sql\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def is_safe_select_query(sql_query: str) -> bool:
    query = sql_query.strip().lower()
    forbidden_words = (
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "pragma",
        "attach",
        "detach",
    )

    if not query.startswith("select"):
        return False

    return not any(re.search(rf"\b{word}\b", query) for word in forbidden_words)


def generate_sql(question: str, schema: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=build_prompt(question, schema),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return clean_sql_response(response.text)


def run_sql_query(sql_query: str) -> pd.DataFrame:
    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql_query(sql_query, conn)


def main() -> None:
    load_dotenv()

    st.set_page_config(page_title="Text-to-SQL Converter", page_icon=":material/database:")
    st.title("Text-to-SQL Converter")
    st.write(
        "Ask a question about the sample employees database, and Gemini will turn it into SQL."
    )

    try:
        schema = load_database_schema()
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    with st.expander("Database schema"):
        st.code(schema, language="text")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: Show all employees from the IT department",
    )

    if "generated_sql" not in st.session_state:
        st.session_state.generated_sql = ""
    if "generated_question" not in st.session_state:
        st.session_state.generated_question = ""

    if st.button("Generate SQL Query"):
        if not question.strip():
            st.warning("Please enter a question before clicking the button.")
            st.stop()

        try:
            with st.spinner("Generating SQL with Gemini..."):
                sql_query = generate_sql(question, schema)

            st.session_state.generated_sql = sql_query
            st.session_state.generated_question = question

        except (ValueError, RuntimeError) as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"API failure or unexpected error: {error}")

    st.subheader("Generated SQL Query")
    if st.session_state.generated_sql:
        st.code(st.session_state.generated_sql, language="sql")
    else:
        st.info("Generate a SQL query first.")

    run_disabled = not bool(st.session_state.generated_sql)
    if st.button("Run Query", disabled=run_disabled):
        if question != st.session_state.generated_question:
            st.warning("The question changed. Generate the SQL query again before running it.")
            st.stop()

        if not is_safe_select_query(st.session_state.generated_sql):
            st.error(
                "This query was generated but not run. For safety, only SELECT queries can be executed."
            )
            st.stop()

        try:
            with st.spinner("Running query on SQLite database..."):
                results = run_sql_query(st.session_state.generated_sql)

            st.subheader("Query Results")
            if results.empty:
                st.info("The query ran successfully, but no matching rows were found.")
            else:
                st.dataframe(results, use_container_width=True)

        except sqlite3.Error as error:
            st.error(f"SQLite error: {error}")
        except Exception as error:
            st.error(f"Unexpected error while running the query: {error}")


if __name__ == "__main__":
    main()
