-- initdb/02_insert_seed_data.sql

-- departments: まず5学部を作成
INSERT INTO departments (name)
VALUES
  ('文学部'),
  ('理学部'),
  ('工学部'),
  ('経済学部'),
  ('法学部');

-- professors: departmentは1〜5の範囲でランダム
INSERT INTO professors (name, department_id)
SELECT
  'Prof_' || i AS name,
  (floor(random() * 5) + 1)::int AS department_id
FROM generate_series(1, 100) AS i;

-- students: departmentは1〜5, yearは1〜4
INSERT INTO students (name, year, department_id)
SELECT
  'Student_' || i AS name,
  (floor(random() * 4) + 1)::int AS year,
  (floor(random() * 5) + 1)::int AS department_id
FROM generate_series(1, 100) AS i;

-- courses: professor_idは1～100, creditsは1～4
INSERT INTO courses (name, professor_id, credits)
SELECT
  'Course_' || i AS name,
  (floor(random() * 100) + 1)::int AS professor_id,
  (floor(random() * 4) + 1)::int AS credits
FROM generate_series(1, 100) AS i;

-- enrollments: student, courseは1〜100からランダム, termは"Spring"/"Fall", gradeはA,B,C,D,F
WITH term_values AS (
    SELECT unnest(array['Spring','Fall']) AS term
),
grade_values AS (
    SELECT unnest(array['A','B','C','D','F']) AS grade
)
INSERT INTO enrollments (student_id, course_id, term, grade)
SELECT
  (floor(random() * 100) + 1)::int AS student_id,
  (floor(random() * 100) + 1)::int AS course_id,
  (SELECT term FROM term_values ORDER BY random() LIMIT 1) AS term,
  (SELECT grade FROM grade_values ORDER BY random() LIMIT 1) AS grade
FROM generate_series(1, 100) AS i;
