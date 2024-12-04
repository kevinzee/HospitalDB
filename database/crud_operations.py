from database.db_connection import get_cursor, close_connection


# Execute a query (INSERT, UPDATE, DELETE)
def execute_query(conn, query, values):
    """
    Execute a SQL query with parameters.
    :param conn: Database connection
    :param query: SQL query string
    :param values: Parameters for the query
    :return: None
    """
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()  # Save the changes to the database
        print("Query executed successfully.")
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cur.close()


# Create - Insert data into a table
def insert_data(conn, query, values):
    """Insert data into the specified table."""
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()  # Save the changes to the database
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cur.close()


# Read - Fetch data from the database
def fetch_data(conn, query, values=None):
    """Fetch data from the specified table."""
    try:
        cur = conn.cursor()
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        rows = cur.fetchall()  # Fetch all results
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        cur.close()


# Update - Update data in the database
def update_data(conn, query, values):
    """Update data in the specified table."""
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()  # Save the changes to the database
        print("Data updated successfully.")
    except Exception as e:
        print(f"Error updating data: {e}")
    finally:
        cur.close()


# Example: Insert a new healthcare professional into the database
def add_healthcare_professional(conn):
    query = """
    INSERT INTO HealthCareProfessionals (HCPID, FirstName, LastName, ContactNumber, Department)
    VALUES (?, ?, ?, ?, ?)
    """
    values = ("00000006", "Emily", "Brown", "212-555-6677", "Pediatrics")
    execute_query(conn, query, values)


# Example: Fetch all healthcare professionals from the database
def list_all_healthcare_professionals(conn):
    query = "SELECT * FROM HealthCareProfessionals"
    hcp_records = fetch_data(conn, query)
    if hcp_records:
        print(f"{'HCPID':<10} {'FirstName':<12} {'LastName':<12} {'ContactNumber':<15} {'Department':<20}")
        print("-" * 70)
        for hcp in hcp_records:
            print(f"{hcp[0]:<10} {hcp[1]:<12} {hcp[2]:<12} {hcp[3]:<15} {hcp[4]:<20}")


# Example: Update a healthcare professional's contact number
def update_healthcare_professional_contact(conn):
    query = "UPDATE HealthCareProfessionals SET ContactNumber = ? WHERE HCPID = ?"
    values = ("212-555-7890", "00000002")  # Updating Laura Taylor's contact number
    execute_query(conn, query, values)


# Example function to test CRUD operations
def test_crud_operations():
    conn = get_cursor()[1]  # Get the database connection
    try:
        # Add a healthcare professional
        add_healthcare_professional(conn)

        # List all healthcare professionals
        print("Healthcare Professionals:")
        list_all_healthcare_professionals(conn)

        # Update a healthcare professional's contact number
        update_healthcare_professional_contact(conn)
    finally:
        close_connection(conn)  # Pass only the connection here


if __name__ == "__main__":
    test_crud_operations()
