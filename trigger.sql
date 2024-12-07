CREATE TRIGGER update_table_ins
AFTER INSERT ON GRADED_COMPONENTS
FOR EACH ROW
BEGIN
    DECLARE total_points FLOAT;
    DECLARE grade CHAR(1);
    DECLARE a_min FLOAT;
    DECLARE b_min FLOAT;
    DECLARE c_min FLOAT;
    DECLARE d_min FLOAT;

    SELECT SUM(g.Points * c.Weight)
    INTO total_points
    FROM COMPONENT c
    JOIN GRADED_COMPONENTS g
    ON c.Course_Id = g.Course AND c.Name = g.Comp_Name
    WHERE g.Student = NEW.Student AND g.Course = NEW.Course;

    SELECT A_Min, B_Min, C_Min, D_Min
    INTO a_min, b_min, c_min, d_min
    FROM COURSE
    WHERE Course_Id = NEW.Course;

    IF total_points >= a_min THEN
        SET grade = 'A';
    ELSEIF total_points >= b_min THEN
        SET grade = 'B';
    ELSEIF total_points >= c_min THEN
        SET grade = 'C';
    ELSEIF total_points >= d_min THEN
        SET grade = 'D';
    ELSE
        SET grade = 'F';
    END IF;

    -- Update ENROLLMENT table with the final grade
    UPDATE ENROLLMENT
    SET Final_Grade = grade
    WHERE Course = NEW.Course AND Panther_ID = NEW.Student;

END;


CREATE TRIGGER update_table_upd
AFTER UPDATE ON GRADED_COMPONENTS
FOR EACH ROW
BEGIN
    DECLARE total_points FLOAT;
    DECLARE grade CHAR(1);
    DECLARE a_min FLOAT;
    DECLARE b_min FLOAT;
    DECLARE c_min FLOAT;
    DECLARE d_min FLOAT;

    SELECT SUM(g.Points * c.Weight)
    INTO total_points
    FROM COMPONENT c
    JOIN GRADED_COMPONENTS g
    ON c.Course_Id = g.Course AND c.Name = g.Comp_Name
    WHERE g.Student = NEW.Student AND g.Course = NEW.Course;
    
    SELECT A_Min, B_Min, C_Min, D_Min
    INTO a_min, b_min, c_min, d_min
    FROM COURSE
    WHERE Course_Id = NEW.Course;

    IF total_points >= a_min THEN
        SET grade = 'A';
    ELSEIF total_points >= b_min THEN
        SET grade = 'B';
    ELSEIF total_points >= c_min THEN
        SET grade = 'C';
    ELSEIF total_points >= d_min THEN
        SET grade = 'D';
    ELSE
        SET grade = 'F';
    END IF;

    -- Update ENROLLMENT table with the final grade
    UPDATE ENROLLMENT
    SET Final_Grade = grade
    WHERE Course = NEW.Course AND Panther_ID = NEW.Student;

END;
