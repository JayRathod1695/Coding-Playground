import mysql.connector
from mysql.connector import errorcode

# Database configuration settings.
# These settings are used to establish a connection to the MySQL database.
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'Coding_playgroung'
}

# Function to establish a database connection.
# This function attempts to connect to the MySQL database using the provided configuration.
def get_db_connection():
    """Establish and return a new database connection."""
    try:
        cnx = mysql.connector.connect(**db_config)
        return cnx
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None



# Functions related to the 'users' table.
# These functions provide methods to retrieve and insert user data.

# Function to retrieve all users from the database.
# It fetches user IDs, usernames, password hashes, and creation timestamps.
def get_users():
    """Retrieve all users from the database."""
    cnx = get_db_connection()
    if not cnx:
        return []
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT id, username, password_hash, created_at FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    cnx.close()
    return users

# Function to insert a new user into the database.
# It takes a username and password hash as input and inserts a new record into the 'users' table.
def post_user(username, password_hash):
    """Insert a new user record into the users table."""
    cnx = get_db_connection()
    if not cnx:
        return None
    cursor = cnx.cursor()
    query = """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
    """
    try:
        cursor.execute(query, (username, password_hash))
        cnx.commit()
        inserted_id = cursor.lastrowid
    except mysql.connector.Error as err:
        print("Error inserting user:", err)
        inserted_id = None
    finally:
        cursor.close()
        cnx.close()
    return inserted_id




# Functions related to project history and autosaving.
# These functions allow retrieval and storage of project history data.

# Function to retrieve project history for a specific user.
# It retrieves project records ordered by the latest timestamp.
def get_project_history(user_id):
    """
    Retrieve all project history records for a given user ordered by the latest timestamp.
    """
    cnx = get_db_connection()
    if not cnx:
        return []
    cursor = cnx.cursor(dictionary=True)
    query = """
        SELECT id, user_id, project_name, data, timestamp 
        FROM project_history 
        WHERE user_id = %s
        ORDER BY timestamp DESC
    """
    cursor.execute(query, (user_id,))
    projects = cursor.fetchall()
    cursor.close()
    cnx.close()
    return projects

# Function to insert a new project history record.
# It stores autosave entries for a given user.
def post_project_history(user_id, project_name, data):
    """
    Insert a new project history record (or autosave entry) for a given user.
    """
    cnx = get_db_connection()
    if not cnx:
        return None
    cursor = cnx.cursor()
    query = """
        INSERT INTO project_history (user_id, project_name, data)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (user_id, project_name, data))
        cnx.commit()
        inserted_id = cursor.lastrowid
    except mysql.connector.Error as err:
        print("Error inserting project history:", err)
        inserted_id = None
    finally:
        cursor.close()
        cnx.close()
    return inserted_id

# Main block for sample usage.
# This block demonstrates how to use the above functions.
if __name__ == "__main__":
    # Sample usage
    # Post a new user
    new_user_id = post_user("alice", "hashed_pw_example")
    print("Inserted new user with ID:", new_user_id)

    # Retrieve users
    users = get_users()
    print("Users:")
    for user in users:
        print(user)

    # Post a project history record
    if new_user_id:
        ph_id = post_project_history(new_user_id, "Project Alpha", '{"blocks": []}')
        print("Inserted project history record with ID:", ph_id)

        # Get project history for user
        projects = get_project_history(new_user_id)
        print("Project History for user", new_user_id, ":", projects)