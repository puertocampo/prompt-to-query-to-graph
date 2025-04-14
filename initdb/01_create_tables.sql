-- initdb/01_create_tables.sql

-- 既に存在するテーブルがあれば削除（依存関係のある順にDROP）
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS departments;

-- =============================
-- 1) departments テーブル
-- =============================
CREATE TABLE departments (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL
);

COMMENT ON TABLE departments IS '学部情報を格納するテーブル';
COMMENT ON COLUMN departments.id IS '学部ID (主キー)';
COMMENT ON COLUMN departments.name IS '学部名';

-- =============================
-- 2) students テーブル
-- =============================
CREATE TABLE students (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    year          INT NOT NULL,        -- 1～4(学年)
    department_id INT NOT NULL,
    CONSTRAINT fk_department
        FOREIGN KEY (department_id) REFERENCES departments(id)
);

COMMENT ON TABLE students IS '学生情報を格納するテーブル';
COMMENT ON COLUMN students.id IS '学生ID (主キー)';
COMMENT ON COLUMN students.name IS '学生名';
COMMENT ON COLUMN students.year IS '学年 (1～4)';
COMMENT ON COLUMN students.department_id IS '学部ID (departments.id への外部キー)';

-- =============================
-- 3) professors テーブル
-- =============================
CREATE TABLE professors (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    CONSTRAINT fk_prof_department
        FOREIGN KEY (department_id) REFERENCES departments(id)
);

COMMENT ON TABLE professors IS '教員情報を格納するテーブル';
COMMENT ON COLUMN professors.id IS '教員ID (主キー)';
COMMENT ON COLUMN professors.name IS '教員名';
COMMENT ON COLUMN professors.department_id IS '学部ID (departments.id への外部キー)';

-- =============================
-- 4) courses テーブル
-- =============================
CREATE TABLE courses (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    professor_id  INT NOT NULL,
    credits       INT NOT NULL,        -- 単位数
    CONSTRAINT fk_professor
        FOREIGN KEY (professor_id) REFERENCES professors(id)
);

COMMENT ON TABLE courses IS '講義情報を格納するテーブル';
COMMENT ON COLUMN courses.id IS '講義ID (主キー)';
COMMENT ON COLUMN courses.name IS '講義名';
COMMENT ON COLUMN courses.professor_id IS '担当教員ID (professors.id への外部キー)';
COMMENT ON COLUMN courses.credits IS '単位数';

-- =============================
-- 5) enrollments テーブル
-- =============================
CREATE TABLE enrollments (
    id         SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id  INT NOT NULL,
    term       VARCHAR(10) NOT NULL,   -- "Spring","Fall" 等
    grade      VARCHAR(2),             -- "A","B","C","D","F" など
    CONSTRAINT fk_student
        FOREIGN KEY (student_id) REFERENCES students(id),
    CONSTRAINT fk_course
        FOREIGN KEY (course_id) REFERENCES courses(id)
);

COMMENT ON TABLE enrollments IS '履修情報・成績を格納するテーブル';
COMMENT ON COLUMN enrollments.id IS '履修ID (主キー)';
COMMENT ON COLUMN enrollments.student_id IS '学生ID (students.id への外部キー)';
COMMENT ON COLUMN enrollments.course_id IS '講義ID (courses.id への外部キー)';
COMMENT ON COLUMN enrollments.term IS '学期 (Spring, Fall など)';
COMMENT ON COLUMN enrollments.grade IS '成績 (A, B, C, D, Fなど)';
