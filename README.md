# School Database Project using SQL connector with Python in Jupyter Notebook within VS Code

## Solution-Oriented Overview
In this project, I designed and implemented a fully operational school database from scratch, aimed at efficiently storing and managing student, teacher, class, and academic data. The goal was to demonstrate my ability to build relational databases, enforce data integrity, and create insightful reports using SQL and Python.

## Tools Used
- **SQLite** – lightweight, file-based database (`school-database.sqlite`)  
- **Python (VS Code / Jupyter Notebook)** – to connect to the database, execute SQL queries, and visualize data  
- **Pandas** – for tabular data representation and analysis  


## Project Highlights
1. **Database Design**
   - Created all core tables: `students`, `teachers`, `classes`, `subjects`, `enrollments`, `grades`, `attendance`, `parents`, `student_parents`, `teacher_subjects`, and `fees`.
   - Defined **primary keys** for unique identification and **foreign keys** to maintain relationships between tables.
   - Implemented **constraints** such as `CHECK` for gender, attendance, and grades, and `UNIQUE` for emails.
     
   ![Tables Creation](https://github.com/Josh-Osas/School-Database-Project-built-with-SQL-and-Python-Jupyter-Notebook-/blob/main/create%20queries%20image.png)

2. **Data Population**
   - Inserted **dummy data for students**, teachers, subjects, classes, parents, and their relationships.
   - Populated enrollment records, teacher-subject assignments, and parent-student links to simulate a real school environment.
     
   ![Data Inserts](https://github.com/Josh-Osas/School-Database-Project-built-with-SQL-and-Python-Jupyter-Notebook-/blob/main/insert%20queries%20image.png)

3. **Views for Reporting**
 
   ![Views](https://github.com/Josh-Osas/School-Database-Project-built-with-SQL-and-Python-Jupyter-Notebook-/blob/main/create%20views%20queries%20image.png)
   
   - **Student Report View**: combines student info, class, parent, and average grades.  
   - **Class Performance View**: calculates average grade per class per term.  
   - **Attendance Summary View**: shows total present, absent, and late days per student.  
 

6. **Data Analysis & Visualization**
   - Queried views directly in Jupyter Notebook using `sqlite3` and `pandas` for clean tabular display.  
  
