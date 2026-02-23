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


