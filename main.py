# if on unix, change below to your python interpreter, else delete if you plan to run it as
# python3 main.py
#!/path/to/python/venv

import mysql.connector


def main():
    user = "root"
    pw = input(
        "Enter root password (to create privileged user)\n"
    )  # Seems like python handles SQLi, so this isnt unsafe
    host = "127.0.0.1"
    db = "grdbkDB"
    charset = "utf8mb4"  # I needed this, it wouldnt work otherwise
    collation = "utf8mb4_general_ci"  # This too

    # Make user for least-privilege safety
    make_user(user, pw, host, db, charset, collation)

    user = "gradebook-admin"
    pw = "Grad3B$$k!"

    update_table_enrollment(user, pw, host, db, charset, collation)

    create_view(user, pw, host, db, charset, collation)

    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host=host,
        charset=charset,  # I needed this, it wouldnt work otherwise
        collation=collation,  # This too
        database=db,
    )
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM Sections_Enrollment")
    result = cursor.fetchall()  # basically, gets the entire output

    print("------------------------------------------------------")

    # Output fairly short, not a lot of DB entries
    for element in result:
        print(element)


def make_user(user: str, pw: str, hst: str, db: str, charset: str, collation: str):
    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host=hst,
        charset=charset,  # I needed this, it wouldnt work otherwise
        collation=collation,  # This too
    )

    user = "gradebook-admin"
    pw = "Grad3B$$k!"

    cursor = cnx.cursor()
    cursor.execute(f"DROP USER '{user}'@'{hst}'")  # I get error otherwise
    cursor.execute(f"CREATE USER '{user}'@'{hst}' IDENTIFIED BY '{pw}'")
    cursor.execute(f"GRANT ALL PRIVILEGES ON {db}.* TO '{user}'@'{hst}'")
    cursor.execute("FLUSH PRIVILEGES")

    # No output, so just make sure user knows that program did something
    print(f"""
###########################################################
 User {user} Created and granted privs on {db}
###########################################################
    """)
    cnx.close()  # Get rid of root db connection


def update_table_enrollment(
    user: str, pw: str, hst: str, db: str, charset: str, collation: str
):
    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host=hst,
        charset=charset,  # I needed this, it wouldnt work otherwise
        collation=collation,  # This too
        database=db,
    )

    # Apparently, python doesnt like it when you put 2 statements in 1 string, so separate them
    # essentially, when reading an sql file, python complains (unless you plan on doing a sql file per query)
    insTrigger = """
        CREATE TRIGGER update_table_ins        -- No DELIMITER coz python complains about it
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
    """
    updTrigger = """
        CREATE TRIGGER update_table_upd   -- No DELIMITER coz python complains about it
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
    """

    cursor = cnx.cursor()
    cursor.execute("DROP TRIGGER IF EXISTS update_table_ins")
    cursor.execute("DROP TRIGGER IF EXISTS update_table_upd")

    cursor.execute(insTrigger)
    cursor.execute(updTrigger)

    # No output, so just make sure user knows that program did something
    print("""
##################################################
 Triggers for update and inserting the table made
##################################################
     """)


def create_view(user: str, pw: str, hst: str, db: str, charset: str, collation: str):
    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host=hst,
        charset=charset,  # I needed this, it wouldnt work otherwise
        collation=collation,  # This too
        database=db,
    )
    cursor = cnx.cursor()

    view = """
        CREATE VIEW Sections_Enrollment as
        SELECT
            s.SectID as Section,
            s.Course_Id as Course_ID,
            c.Name as Course_Name,
            COUNT(*) as Enrolled_Students
        FROM SECTION s
        JOIN
            COURSE c on s.Course_Id = c.Course_Id
        LEFT JOIN
            ENROLLMENT e on s.Course_Id = e.Course AND s.SectID = e.Section AND e.Status = 'Enrolled'
        GROUP BY
        s.SectID, s.Course_Id, c.Name
    """

    cursor.execute("DROP VIEW IF EXISTS Sections_Enrollment")
    cursor.execute(view)

    # No prints here bc result is printed in main()


if __name__ == "__main__":
    main()
