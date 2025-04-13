-- initdb/01_create_tables.sql

-- 既に同名テーブルが存在する場合を想定して削除
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS departments;

-- 学部情報
CREATE TABLE departments (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL
);

-- 学生情報
CREATE TABLE students (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    year        INT NOT NULL,           -- 1～4(学年)
    department_id INT NOT NULL,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- 教員情報
CREATE TABLE professors (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    CONSTRAINT fk_prof_department
        FOREIGN KEY (department_id) REFERENCES departments(id)
);

-- 講義情報
CREATE TABLE courses (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    professor_id INT NOT NULL,
    credits     INT NOT NULL,           -- 単位数
    CONSTRAINT fk_professor
        FOREIGN KEY (professor_id) REFERENCES professors(id)
);

-- 履修情報
CREATE TABLE enrollments (
    id          SERIAL PRIMARY KEY,
    student_id  INT NOT NULL,
    course_id   INT NOT NULL,
    term        VARCHAR(10) NOT NULL,   -- "Spring", "Fall"など
    grade       VARCHAR(2),             -- "A", "B", "C", "D", "F"など
    CONSTRAINT fk_student
        FOREIGN KEY (student_id) REFERENCES students(id),
    CONSTRAINT fk_course
        FOREIGN KEY (course_id) REFERENCES courses(id)
);
