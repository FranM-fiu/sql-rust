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
    cursor.execute("DROP TRIGGER update_table")
    cursor.execute("""
DELIMETER ||

CREATE TRIGGER update_table
BEFORE INSERT ON ENROLLMENT 
FOR EACH ROW
BEGIN
    DECLARE total_points DECIMAL(5,2) DEFAULT 0;

END ||
DELIMETER ;
    """)


if __name__ == "__main__":
    main()
