-- CREATE DATABASE grdbkDB;
-- USE grdbkDB;

INSERT INTO COURSE (Course_Id, Name, A_Min, B_Min, C_Min, D_Min, Credits) VALUES
('DST-69', 'Data Structures', 90.0, 80.0, 70.0, 60.0, 3),
('DBM-420', 'Database Management', 83.0, 63.0, 43.0, 23.0, 35);

INSERT INTO TERM (Term_Id, Name, Start_Date, End_Date) VALUES
('1245', 'Summer 2024', '2024-05-01', '2024-07-31'),
('1248', 'Fall 2024', '2024-08-15', '2024-12-15');

INSERT INTO SECTION (Course_Id, SectID, Online, Schedule, Room_No, Term) VALUES
('DST-69', 'U01', FALSE, 'MW 10:00-11:50', 'PG-240', '1245'),
('DST-69', 'U02', TRUE, 'ONLINE', 'VIRTUAL', '1248'),
('DBM-420', 'U01', FALSE, 'TR 14:00-15:50', 'PG-220', '1245'),
('DBM-420', 'U02', FALSE, 'MW 15:00-16:50', 'PG-230', '1248');

INSERT INTO STUDENT (Panther_ID, First_Name, Last_Name, Email) VALUES
('1234567', 'John', 'Smith', 'jsmith001@pleaseDontStealMyData.prettyPlease.com'),
('1234568', 'Maria', 'Garcia', 'mgarc023@pleaseDontStealMyData.prettyPlease.com'),
('1234569', 'David', 'Johnson', 'djohn045@pleaseDontStealMyData.prettyPlease.com'),
('1234570', 'Sarah', 'Williams', 'swill089@pleaseDontStealMyData.prettyPlease.com'),
('1234571', 'Michael', 'Brown', 'mbrow067@pleaseDontStealMyData.prettyPlease.com'),
('1234572', 'Jennifer', 'Davis', 'jdavi134@pleaseDontStealMyData.prettyPlease.com'),
('1234573', 'Robert', 'Miller', 'rmill078@pleaseDontStealMyData.prettyPlease.com'),
('1234574', 'Lisa', 'Anderson', 'land0156@pleaseDontStealMyData.prettyPlease.com'),
('1234575', 'James', 'Wilson', 'jwils198@pleaseDontStealMyData.prettyPlease.com'),
('1234576', 'Emily', 'Taylor', 'etayl234@pleaseDontStealMyData.prettyPlease.com'),
('1234577', 'Daniel', 'Martinez', 'dmart345@pleaseDontStealMyData.prettyPlease.com'),
('1234578', 'Michelle', 'Thomas', 'mthom432@pleaseDontStealMyData.prettyPlease.com');

INSERT INTO ENROLLMENT (Course, Section, Panther_ID, Status) VALUES
-- DST-69 U01 (Summer 2024)
('DST-69', 'U01', '1234567', 'Enrolled'),
('DST-69', 'U01', '1234568', 'Enrolled'),
('DST-69', 'U01', '1234569', 'Enrolled'),
-- DBM-420 U01 (Summer 2024)
('DBM-420', 'U01', '1234573', 'Enrolled'),
('DBM-420', 'U01', '1234574', 'Enrolled'),
('DBM-420', 'U01', '1234575', 'Enrolled'),
-- DST-69 U02 (Fall 2024)
('DST-69', 'U02', '1234570', 'Enrolled'),
('DST-69', 'U02', '1234571', 'Enrolled'),
('DST-69', 'U02', '1234572', 'Enrolled'),
-- DBM-420 U02 (Fall 2024)
('DBM-420', 'U02', '1234576', 'Enrolled'),
('DBM-420', 'U02', '1234577', 'Enrolled'),
('DBM-420', 'U02', '1234578', 'Enrolled');

INSERT INTO COMPONENT (Course_Id, Name, Max_Points, Weight) VALUES
('DST-69', 'Midterm Exam', 100.0, 0.30),
('DST-69', 'Final Project', 100.0, 0.40),
('DBM-420', 'Database Design', 100.0, 0.35),
('DBM-420', 'Final Exam', 100.0, 0.45);

INSERT INTO GRADED_COMPONENTS (Course, Comp_Name, Student, Points) VALUES
-- DST-69 Grades for U01 students
('DST-69', 'Midterm Exam', '1234567', 88.5),
('DST-69', 'Final Project', '1234567', 92.0),
('DST-69', 'Midterm Exam', '1234568', 95.0),
('DST-69', 'Final Project', '1234568', 89.5),
('DST-69', 'Midterm Exam', '1234569', 78.5),
('DST-69', 'Final Project', '1234569', 85.0),
-- DST-69 Grades for U02 students
('DST-69', 'Midterm Exam', '1234570', 91.0),
('DST-69', 'Final Project', '1234570', 88.0),
('DST-69', 'Midterm Exam', '1234571', 87.5),
('DST-69', 'Final Project', '1234571', 90.0),
('DST-69', 'Midterm Exam', '1234572', 82.0),
('DST-69', 'Final Project', '1234572', 84.5),
-- DBM-420 Grades for U01 students
('DBM-420', 'Database Design', '1234573', 89.0),
('DBM-420', 'Final Exam', '1234573', 94.5),
('DBM-420', 'Database Design', '1234574', 92.5),
('DBM-420', 'Final Exam', '1234574', 88.0),
('DBM-420', 'Database Design', '1234575', 86.0),
('DBM-420', 'Final Exam', '1234575', 91.5),
-- DBM-420 Grades for U02 students
('DBM-420', 'Database Design', '1234576', 93.0),
('DBM-420', 'Final Exam', '1234576', 95.0),
('DBM-420', 'Database Design', '1234577', 85.5),
('DBM-420', 'Final Exam', '1234577', 88.5),
('DBM-420', 'Database Design', '1234578', 90.0),
('DBM-420', 'Final Exam', '1234578', 87.0);
