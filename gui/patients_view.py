import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from database.basic_queries import get_all_patients, add_patient_to_db, update_patient, delete_patient


class PatientsView:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn

        # Configure table styles
        style = tb.Style()
        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=30,
            fieldbackground="white",
            borderwidth=0,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Treeview.Heading",
            background="#f8f9fa",
            foreground="black",
            font=("Segoe UI", 12, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", "#e8f4ff")],
            foreground=[("selected", "black")],
        )

    def show(self, content_frame):
        """Display the Patients view."""
        # Clear the content frame
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Search bar
        search_frame = tb.Frame(content_frame)
        search_frame.pack(side="top", fill="x", pady=10)

        search_label = tb.Label(search_frame, text="Search:")
        search_label.pack(side="left", padx=5)
        search_entry = tb.Entry(search_frame)
        search_entry.pack(side="left", padx=5)

        search_button = tb.Button(
            search_frame,
            text="Search",
            command=lambda: self.search_patients(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame, text="Add Patient", command=self.add_patient, bootstyle=SUCCESS
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying Patients
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("PatientID", "First Name", "Last Name", "DOB", "Address", "Phone Number", "PrimaryHCPID")
        self.tree = tb.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
        self.tree.column("PatientID", anchor="center", width=100)
        self.tree.column("First Name", anchor="w", width=150)
        self.tree.column("Last Name", anchor="w", width=150)
        self.tree.column("DOB", anchor="center", width=120)
        self.tree.column("Address", anchor="w", width=200)
        self.tree.column("Phone Number", anchor="center", width=120)
        self.tree.column("PrimaryHCPID", anchor="center", width=100)

        # Add headers
        self.tree.heading("PatientID", text="Patient ID", anchor="center")
        self.tree.heading("First Name", text="First Name", anchor="w")
        self.tree.heading("Last Name", text="Last Name", anchor="w")
        self.tree.heading("DOB", text="Date of Birth", anchor="center")
        self.tree.heading("Address", text="Address", anchor="w")
        self.tree.heading("Phone Number", text="Phone Number", anchor="center")
        self.tree.heading("PrimaryHCPID", text="Primary HCP ID", anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        actions_frame = tb.Frame(content_frame)
        actions_frame.pack(side="bottom", fill="x", pady=10)

        edit_button = tb.Button(
            actions_frame, text="Edit Patient", command=self.edit_patient, bootstyle=INFO
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame, text="Delete Patient", command=self.delete_patient, bootstyle=DANGER
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_patients()

    def load_patients(self):
        """Load patients from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            patients = get_all_patients(self.db_conn)
            for idx, patient in enumerate(patients):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=patient, tags=(tag,))
            self.tree.tag_configure("evenrow", background="#f9f9f9")
            self.tree.tag_configure("oddrow", background="#ffffff")
        except Exception as e:
            Messagebox.show_error(f"Failed to load patients: {e}", title="Error")

    def search_patients(self, search_entry):
        """Search patients based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            patients = get_all_patients(self.db_conn)
            filtered_patients = [
                p for p in patients if query.lower() in p[1].lower() or query.lower() in p[2].lower()
            ]
            for patient in filtered_patients:
                self.tree.insert("", "end", values=patient)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_patient(self):
        """Open a form to add a new patient."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Patient")
        add_window.geometry("400x400")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["PatientID", "FirstName", "LastName", "DOB", "Address", "PhoneNumber", "PrimaryHCPID"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_patient():
            """Save the patient to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_patient_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_patients()
            except Exception as e:
                Messagebox.show_error(f"Failed to add patient: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_patient, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_patient(self):
        """Edit selected patient."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Patient")
        edit_window.geometry("400x400")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["FirstName", "LastName", "DOB", "Address", "PhoneNumber", "PrimaryHCPID"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Skip PatientID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_patient_record():
            """Update patient in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["PatientID"] = values[0]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_patient(self.db_conn, data["PatientID"], data)
                edit_window.destroy()
                self.load_patients()
            except Exception as e:
                Messagebox.show_error(f"Failed to update patient: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_patient_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_patient(self):
        """Delete selected patient."""
        # Get the selected item
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        # Retrieve the PatientID from the selected row
        values = self.tree.item(selected_item, "values")
        if not values:
            Messagebox.show_error("Failed to retrieve the selected patient's details.", title="Error")
            return

        patient_id = values[0]  # Assuming the first column is the PatientID

        # Confirm deletion with the user
        confirm = Messagebox.okcancel(
            message=f"Are you sure you want to delete the patient with ID '{patient_id}'?",
            title="Confirm Deletion",
            alert=True
        )
        if not confirm:
            return

        try:
            # Call the database method to delete the patient
            delete_patient(self.db_conn, patient_id)
            # Remove the deleted item from the Treeview
            self.tree.delete(selected_item)
            Messagebox.show_info(f"Patient with ID '{patient_id}' deleted successfully.", title="Success")
        except Exception as e:
            Messagebox.show_error(f"Failed to delete patient: {e}", title="Error")
