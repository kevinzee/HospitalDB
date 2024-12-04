from gui.app_gui import HospitalAppGUI
from database.db_connection import connect_to_db, close_connection
import tkinter as tk

def main():
    # Establish database connection
    db_connection = connect_to_db()

    # Initialize the GUI and pass the database connection
    root = tk.Tk()
    app = HospitalAppGUI(root, db_connection)

    try:
        root.mainloop()
    finally:
        # Ensure the database connection is closed when the app exits
        close_connection(db_connection)

if __name__ == "__main__":
    main()
