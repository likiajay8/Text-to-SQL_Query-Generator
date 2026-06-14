import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "employees.db"


def create_database() -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS employees;")
        cursor.execute("DROP TABLE IF EXISTS departments;")

        cursor.execute(
            """
            CREATE TABLE departments (
                department_id INTEGER PRIMARY KEY,
                department_name TEXT NOT NULL,
                manager_name TEXT NOT NULL,
                office_city TEXT NOT NULL,
                annual_budget INTEGER NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE employees (
                employee_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                salary INTEGER NOT NULL,
                city TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                job_title TEXT NOT NULL,
                FOREIGN KEY (department_id) REFERENCES departments (department_id)
            );
            """
        )

        departments = [
            (1, "IT", "Asha Rao", "Bengaluru", 900000),
            (2, "Human Resources", "Vikram Singh", "Mumbai", 420000),
            (3, "Finance", "Neha Sharma", "Delhi", 750000),
            (4, "Sales", "Rahul Mehta", "Pune", 650000),
            (5, "Marketing", "Priya Nair", "Hyderabad", 560000),
        ]

        employees = [
            (101, "Ananya Gupta", 1, 85000, "Bengaluru", "2021-03-15", "Software Engineer"),
            (102, "Rohan Das", 1, 92000, "Bengaluru", "2020-07-21", "Data Engineer"),
            (103, "Meera Iyer", 2, 62000, "Mumbai", "2022-01-10", "HR Executive"),
            (104, "Karan Patel", 3, 78000, "Delhi", "2019-11-05", "Accountant"),
            (105, "Sara Khan", 4, 70000, "Pune", "2023-04-18", "Sales Associate"),
            (106, "Arjun Reddy", 5, 68000, "Hyderabad", "2021-09-12", "Marketing Analyst"),
            (107, "Nisha Verma", 1, 105000, "Chennai", "2018-06-30", "Senior Developer"),
            (108, "Dev Malhotra", 3, 99000, "Delhi", "2020-12-01", "Finance Manager"),
            (109, "Ishita Bose", 4, 73000, "Kolkata", "2022-08-08", "Sales Specialist"),
            (110, "Kabir Menon", 5, 81000, "Hyderabad", "2019-02-25", "Brand Manager"),
        ]

        cursor.executemany(
            """
            INSERT INTO departments (
                department_id,
                department_name,
                manager_name,
                office_city,
                annual_budget
            )
            VALUES (?, ?, ?, ?, ?);
            """,
            departments,
        )

        cursor.executemany(
            """
            INSERT INTO employees (
                employee_id,
                name,
                department_id,
                salary,
                city,
                hire_date,
                job_title
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            employees,
        )

        conn.commit()

    print(f"Database created successfully at {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()
