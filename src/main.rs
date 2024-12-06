use mysql::prelude::*;
use mysql::*;
use std::io;

fn main() -> std::result::Result<(), Box<dyn std::error::Error>> {
    // Start admin connection (To create and grant privs to user)
    let mut admin_passwd: String = String::new();
    println!("What is the admin password? (to create a user)");
    io::stdin().read_line(&mut admin_passwd).unwrap(); // Fix error handling here

    let mysql_admin_url: String = format!("mysql://root:{}@localhost:3306/grdbkDB", admin_passwd);

    let pool = Pool::new(mysql_admin_url)?;
    let mut conn = pool.get_conn()?;

    let new_username = "gradebook-admin";
    let new_pass = "Grad3BOOk!";

    let create_user = format!(
        "\
CREATE USER '{}'@'localhost' IDENTIFIED BY '{}';
GRANT ALL PRIVILEGES ON *.* TO '{}'@'localhost';
FLUSH PRIVILEGES;
        ",
        new_username, new_pass, new_username
    );

    conn.query_drop(create_user);
    println!("User {new_username} created with all privs");
    // End admin connection
    //
    Ok(())
}
