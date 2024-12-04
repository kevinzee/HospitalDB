import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from database.basic_queries import (
    get_all_patient_insurance,
    add_patient_insurance_to_db,
    update_patient_insurance,
    delete_patient_insurance,
)


class PatientInsuranceView:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn

    def show(self, content_frame):
        """Display the Patient Insurance view."""
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
            command=lambda: self.search_patient_insurance(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame,
            text="Add Patient Insurance",
            command=self.add_patient_insurance,
            bootstyle=SUCCESS,
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying Patient Insurance
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("PatientID", "InsuranceID", "Coverage Start Date", "Coverage End Date")
        self.tree = tb.Treeview(tree_frame, columns=columns, show="headings", bootstyle=INFO)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        actions_frame = tb.Frame(content_frame)
        actions_frame.pack(side="bottom", fill="x", pady=10)

        edit_button = tb.Button(
            actions_frame,
            text="Edit Patient Insurance",
            command=self.edit_patient_insurance,
            bootstyle=INFO,
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame,
            text="Delete Patient Insurance",
            command=self.delete_patient_insurance,
            bootstyle=DANGER,
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_patient_insurance()

    def load_patient_insurance(self):
        """Load patient insurance from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            patient_insurance = get_all_patient_insurance(self.db_conn)
            for entry in patient_insurance:
                self.tree.insert("", "end", values=entry)
        except Exception as e:
            Messagebox.show_error(f"Failed to load patient insurance: {e}", title="Error")

    def search_patient_insurance(self, search_entry):
        """Search patient insurance based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            patient_insurance = get_all_patient_insurance(self.db_conn)
            filtered_entries = [
                entry for entry in patient_insurance if query.lower() in str(entry).lower()
            ]
            for entry in filtered_entries:
                self.tree.insert("", "end", values=entry)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_patient_insurance(self):
        """Open a form to add a new patient insurance record."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Patient Insurance")
        add_window.geometry("400x400")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["PatientID", "InsuranceID", "CoverageStartDate", "CoverageEndDate"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_patient_insurance():
            """Save the patient insurance to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_patient_insurance_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_patient_insurance()
            except Exception as e:
                Messagebox.show_error(f"Failed to add patient insurance: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_patient_insurance, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_patient_insurance(self):
        """Edit selected patient insurance."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Patient Insurance")
        edit_window.geometry("400x400")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["CoverageStartDate", "CoverageEndDate"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 2])  # Skip PatientID and InsuranceID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_patient_insurance_record():
            """Update patient insurance in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["PatientID"] = values[0]
            data["InsuranceID"] = values[1]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_patient_insurance(self.db_conn, data["PatientID"], data["InsuranceID"], data)
                edit_window.destroy()
                self.load_patient_insurance()
            except Exception as e:
                Messagebox.show_error(f"Failed to update patient insurance: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_patient_insurance_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_patient_insurance(self):
        """Delete selected patient insurance."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        try:
            delete_patient_insurance(self.db_conn, values[0], values[1])  # PatientID, InsuranceID
            self.load_patient_insurance()
        except Exception as e:
            Messagebox.show_error(f"Failed to delete patient insurance: {e}", title="Error")
