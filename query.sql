-- Create the database
CREATE DATABASE edusentiment;

-- Select the database
USE edusentiment;

-- Create the students table
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    enrollment_year INT
);

-- Create the departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- Create the feedback table
CREATE TABLE feedback (
    feedback_id INT PRIMARY KEY,
    student_id VARCHAR(10),
    department_id INT,
    date DATE,
    feedback_text TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


CREATE TABLE feedback_enriched AS
SELECT 
    f.feedback_id,
    d.department_name,
    f.student_id,
    f.date,
    f.feedback_text
FROM feedback f
JOIN departments d ON f.department_id = d.department_id
JOIN students s ON f.student_id = s.student_id;

select * from feedback_enriched;