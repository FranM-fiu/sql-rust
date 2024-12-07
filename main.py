#!/home/fmart/Code/rust/sql-rust/.venv/bin/python

import mysql.connector


def main():
    user = "root"
    pw = input("Enter root password (to create privileged user)\n")
    host = "127.0.0.1"
    db = "grdbkDB"
    charset = "utf8mb4"  # I needed this, it wouldnt work otherwise
    collation = "utf8mb4_general_ci"  # This too

    make_user(user, pw, host, db, charset, collation)
    update_table_enrollment(user, pw, host, db, charset, collation)


def make_user(user: str, pw: str, hst: str, db: str, charset: str, collation: str):
    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host=hst,
        charset=charset,  # I needed this, it wouldnt work otherwise
        collation=collation,  # This too
    )

    user = "gradebook-admin"
    pw = "Grad3B00k!"

    cursor = cnx.cursor()
    cursor.execute(f"DROP USER '{user}'@'{hst}'")  # I get error otherwise
    cursor.execute(f"CREATE USER '{user}'@'{hst}' IDENTIFIED BY '{pw}'")
    cursor.execute(f"GRANT ALL PRIVILEGES ON {db}.* TO '{user}'@'{hst}'")
    cursor.execute("FLUSH PRIVILEGES")

    print(f"User {user} Created and granted privs on {db}")
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

    cursor = cnx.cursor()
    # cursor.execute("DROP TRIGGER IF EXISTS update_table_ins")
    cursor.execute("DROP TRIGGER IF EXISTS update_table_upd")
    cursor.execute("""
        DELIMETER ||
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

        END ||
        DELIMETER ;
    """)
    # For update
    cursor.execute("""
        DELIMETER ||
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

        END ||
        DELIMETER ;
    """)

    print("Triggers for update and inserting the table made")


if __name__ == "__main__":
    main()
