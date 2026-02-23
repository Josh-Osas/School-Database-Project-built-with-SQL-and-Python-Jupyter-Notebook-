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

