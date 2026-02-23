# %%
import sqlite3
import pandas as pd

conn = sqlite3.connect('school-database.sqlite')
cursor = conn.cursor()

print("Connected to SQLite database.")

# %%
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT CHECK (gender IN ('Male', 'Female')),
    date_of_birth DATE,
    year_group TEXT NOT NULL,
    admission_date DATE,
    status TEXT DEFAULT 'Active'
);
""")

# %%
cursor.execute("""
               CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    hire_date DATE,
    status TEXT DEFAULT 'Active'
);
""")

# %%
cursor.execute("""
CREATE TABLE IF NOT EXISTS classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    year_group TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
);
""")

# %%
# Enable foreign key support (good practice)
conn.execute("PRAGMA foreign_keys = ON;")

# Create the subjects table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL UNIQUE
);
""")

# %%
# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON;")

# Create the enrollments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    academic_year TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (class_id) REFERENCES classes (class_id)
);
""")

# %%
# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON;")

# Create the teacher_subjects table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teacher_subjects (
    teacher_subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id),
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
);
""")

# %%
# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON;")

# Create the grades table
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    term TEXT NOT NULL,
    score INTEGER CHECK (score BETWEEN 0 AND 100),
    grade TEXT,
    academic_year TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
);
""")

# %%

# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON;")

# Create the attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK (status IN ('Present', 'Absent', 'Late')),
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);
""")

# %%

# Create the parents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS parents (
    parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);
""")

# %%
# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON;")

# Create the student_parents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    relationship TEXT,
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (parent_id) REFERENCES parents (parent_id)
);
""")

# %%

# Enable foreign key support
conn.execute("PRAGMA foreign_keys = ON;")

# Create the fees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fees (
    fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    term TEXT NOT NULL,
    academic_year TEXT NOT NULL,
    status TEXT CHECK (status IN ('Paid', 'Partially Paid', 'Unpaid')),
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);
""")

# %%
# Query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# %%

# Load table into a DataFrame
df_students = pd.read_sql_query("SELECT * FROM students;", conn)

# Display the table
df_students

# %%

# List of teacher records to insert
teachers_data = [
    ('0001', 'Alice', 'Johnson', 'alice.johnson@example.com', '0801000001', '2020-01-10'),
    ('0002', 'Michael', 'Smith', 'michael.smith@example.com', '0801000002', '2019-05-15'),
    ('0003', 'Laura', 'Brown', 'laura.brown@example.com', '0801000003', '2021-03-20'),
    ('0004', 'David', 'Wilson', 'david.wilson@example.com', '0801000004', '2018-08-01')
]

# Insert teachers into the table
cursor.executemany("""
INSERT OR IGNORE INTO teachers (teacher_id, first_name, last_name, email, phone, hire_date)
VALUES (?, ?, ?, ?, ?, ?);
""", teachers_data)

# %%
# Load table into a DataFrame
df_teachers = pd.read_sql_query("SELECT * FROM teachers;", conn)

# Display the table
df_teachers

# %%
# List of subject records to insert
subjects_data = [
    ('0001', 'Mathematics'),
    ('0002', 'English'),
    ('0003', 'Science'),
    ('0004', 'History'),
    ('0005', 'Geography'),
    ('0006', 'Art')
]

# Insert subjects into the table
cursor.executemany("""
INSERT OR IGNORE INTO subjects (subject_id, subject_name)
VALUES (?, ?);
""", subjects_data)

# %%
# List of class records to insert
classes_data = [
    ('0001', 'Year 1A', 'Year 1', '0001'),
    ('0002', 'Year 2A', 'Year 2', '0002'),
    ('0003', 'Year 3A', 'Year 3', '0003'),
    ('0004', 'Year 4A', 'Year 4', '0004'),
    ('0005', 'Year 5A', 'Year 5', '0001'),
    ('0006', 'Year 6A', 'Year 6', '0002')
]

# Insert classes into the table
cursor.executemany("""
INSERT OR IGNORE INTO classes (class_id, class_name, year_group, teacher_id)
VALUES (?, ?, ?, ?);
""", classes_data)

# %%

students_data = [
    ('0001', 'James', 'Taylor', 'Male', '2015-03-12', 'Year 1', '2021-09-01', 'Active'),
    ('0002', 'Olivia', 'Anderson', 'Female', '2014-06-25', 'Year 2', '2020-09-01', 'Active'),
    ('0003', 'Liam', 'Thomas', 'Male', '2013-11-03', 'Year 3', '2019-09-01', 'Active'),
    ('0004', 'Emma', 'Jackson', 'Female', '2012-02-17', 'Year 4', '2018-09-01', 'Active'),
    ('0005', 'Noah', 'White', 'Male', '2011-08-21', 'Year 5', '2017-09-01', 'Active'),
    ('0006', 'Ava', 'Harris', 'Female', '2010-12-30', 'Year 6', '2016-09-01', 'Active'),
    ('0007', 'William', 'Martin', 'Male', '2015-05-14', 'Year 1', '2021-09-01', 'Active'),
    ('0008', 'Sophia', 'Thompson', 'Female', '2014-07-19', 'Year 2', '2020-09-01', 'Active'),
    ('0009', 'Benjamin', 'Garcia', 'Male', '2013-09-27', 'Year 3', '2019-09-01', 'Active'),
    ('0010', 'Isabella', 'Martinez', 'Female', '2012-01-05', 'Year 4', '2018-09-01', 'Active'),
    ('0011', 'Elijah', 'Robinson', 'Male', '2011-03-11', 'Year 5', '2017-09-01', 'Active'),
    ('0012', 'Mia', 'Clark', 'Female', '2010-06-08', 'Year 6', '2016-09-01', 'Active'),
    ('0013', 'James', 'Rodriguez', 'Male', '2015-04-22', 'Year 1', '2021-09-01', 'Active'),
    ('0014', 'Charlotte', 'Lewis', 'Female', '2014-09-30', 'Year 2', '2020-09-01', 'Active'),
    ('0015', 'Alexander', 'Lee', 'Male', '2013-12-17', 'Year 3', '2019-09-01', 'Active'),
    ('0016', 'Amelia', 'Walker', 'Female', '2012-03-23', 'Year 4', '2018-09-01', 'Active'),
    ('0017', 'Daniel', 'Hall', 'Male', '2011-07-02', 'Year 5', '2017-09-01', 'Active'),
    ('0018', 'Harper', 'Allen', 'Female', '2010-11-15', 'Year 6', '2016-09-01', 'Active'),
    ('0019', 'Matthew', 'Young', 'Male', '2015-01-28', 'Year 1', '2021-09-01', 'Active'),
    ('0020', 'Evelyn', 'Hernandez', 'Female', '2014-05-13', 'Year 2', '2020-09-01', 'Active'),
    ('0021', 'David', 'King', 'Male', '2013-08-19', 'Year 3', '2019-09-01', 'Active'),
    ('0022', 'Abigail', 'Wright', 'Female', '2012-12-25', 'Year 4', '2018-09-01', 'Active'),
    ('0023', 'Joseph', 'Lopez', 'Male', '2011-02-14', 'Year 5', '2017-09-01', 'Active'),
    ('0024', 'Emily', 'Hill', 'Female', '2010-07-07', 'Year 6', '2016-09-01', 'Active'),
    ('0025', 'Samuel', 'Scott', 'Male', '2015-09-09', 'Year 1', '2021-09-01', 'Active'),
    ('0026', 'Ella', 'Green', 'Female', '2014-11-11', 'Year 2', '2020-09-01', 'Active'),
    ('0027', 'Anthony', 'Adams', 'Male', '2013-01-16', 'Year 3', '2019-09-01', 'Active'),
    ('0028', 'Lily', 'Baker', 'Female', '2012-04-20', 'Year 4', '2018-09-01', 'Active'),
    ('0029', 'Christopher', 'Gonzalez', 'Male', '2011-06-30', 'Year 5', '2017-09-01', 'Active'),
    ('0030', 'Grace', 'Nelson', 'Female', '2010-10-12', 'Year 6', '2016-09-01', 'Active')
]

cursor.executemany("""
INSERT OR IGNORE INTO students (student_id, first_name, last_name, gender, date_of_birth, year_group, admission_date, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", students_data)

# %%
parents_data = [
    ('0001', 'Robert Taylor', '0802000001', 'robert.taylor@example.com'),
    ('0002', 'Linda Anderson', '0802000002', 'linda.anderson@example.com'),
    ('0003', 'Charles Thomas', '0802000003', 'charles.thomas@example.com'),
    ('0004', 'Patricia Jackson', '0802000004', 'patricia.jackson@example.com'),
    ('0005', 'Mark White', '0802000005', 'mark.white@example.com')
]

cursor.executemany("""
INSERT OR IGNORE INTO parents (parent_id, full_name, phone, email)
VALUES (?, ?, ?, ?);
""", parents_data)

# %%
student_parents_data = [
    ('0001', '0001', '0001', 'Father'),
    ('0002', '0002', '0002', 'Mother'),
    ('0003', '0003', '0003', 'Father'),
    ('0004', '0004', '0004', 'Mother'),
    ('0005', '0005', '0005', 'Father')
    # You can extend this pattern for all 30 students
]

cursor.executemany("""
INSERT OR IGNORE INTO student_parents (id, student_id, parent_id, relationship)
VALUES (?, ?, ?, ?);
""", student_parents_data)

# %%
teacher_subjects_data = [
    ('0001','0001','0001'),
    ('0002','0001','0002'),
    ('0003','0002','0003'),
    ('0004','0002','0004'),
    ('0005','0003','0005'),
    ('0006','0003','0006'),
    ('0007','0004','0001'),
    ('0008','0004','0002')
]

cursor.executemany("""
INSERT OR IGNORE INTO teacher_subjects (teacher_subject_id, teacher_id, subject_id)
VALUES (?, ?, ?);
""", teacher_subjects_data)

# %%
# Full enrollments for 30 students across 6 classes
enrollments_data = [
    ('0001','0001','0001','2025'),
    ('0002','0002','0002','2025'),
    ('0003','0003','0003','2025'),
    ('0004','0004','0004','2025'),
    ('0005','0005','0005','2025'),
    ('0006','0006','0006','2025'),
    ('0007','0007','0001','2025'),
    ('0008','0008','0002','2025'),
    ('0009','0009','0003','2025'),
    ('0010','0010','0004','2025'),
    ('0011','0011','0005','2025'),
    ('0012','0012','0006','2025'),
    ('0013','0013','0001','2025'),
    ('0014','0014','0002','2025'),
    ('0015','0015','0003','2025'),
    ('0016','0016','0004','2025'),
    ('0017','0017','0005','2025'),
    ('0018','0018','0006','2025'),
    ('0019','0019','0001','2025'),
    ('0020','0020','0002','2025'),
    ('0021','0021','0003','2025'),
    ('0022','0022','0004','2025'),
    ('0023','0023','0005','2025'),
    ('0024','0024','0006','2025'),
    ('0025','0025','0001','2025'),
    ('0026','0026','0002','2025'),
    ('0027','0027','0003','2025'),
    ('0028','0028','0004','2025'),
    ('0029','0029','0005','2025'),
    ('0030','0030','0006','2025')
]

# Insert all enrollments
cursor.executemany("""
INSERT OR IGNORE INTO enrollments (enrollment_id, student_id, class_id, academic_year)
VALUES (?, ?, ?, ?);
""", enrollments_data)

# %%
# Create the student_report view
cursor.execute("""
CREATE VIEW IF NOT EXISTS student_report AS
SELECT 
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    s.year_group,
    c.class_name,
    p.full_name AS parent_name,
    ROUND(AVG(g.score), 2) AS avg_score
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
LEFT JOIN classes c ON e.class_id = c.class_id
LEFT JOIN student_parents sp ON s.student_id = sp.student_id
LEFT JOIN parents p ON sp.parent_id = p.parent_id
LEFT JOIN grades g ON s.student_id = g.student_id
GROUP BY s.student_id;
""")


# %%
# Create the class_performance view
cursor.execute("""
CREATE VIEW IF NOT EXISTS class_performance AS
SELECT
    c.class_name,
    s.year_group,
    g.term,
    ROUND(AVG(g.score), 2) AS avg_score
FROM classes c
JOIN enrollments e ON c.class_id = e.class_id
JOIN students s ON e.student_id = s.student_id
JOIN grades g ON s.student_id = g.student_id
GROUP BY c.class_id, g.term;
""")

# %%
# Create the attendance_summary view
cursor.execute("""
CREATE VIEW IF NOT EXISTS attendance_summary AS
SELECT
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS total_present,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) AS total_absent,
    SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) AS total_late
FROM students s
LEFT JOIN attendance a ON s.student_id = a.student_id
GROUP BY s.student_id;
""")

# %%
# Load the view into a Pandas DataFrame
df = pd.read_sql_query("SELECT * FROM student_report;", conn)

# Display as a nice table in Jupyter Notebook
df


