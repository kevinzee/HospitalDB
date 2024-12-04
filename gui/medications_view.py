import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from database.basic_queries import get_all_medications, add_medication_to_db, update_medication, delete_medication


class MedicationsView:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn

    def show(self, content_frame):
        """Display the Medications view."""
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
            search_frame, text="Search", command=lambda: self.search_medications(search_entry), bootstyle=PRIMARY
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame, text="Add Medication", command=self.add_medication, bootstyle=SUCCESS
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying Medications
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("MedicationID", "Medication Name", "Dosage", "Manufacturer")
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
            actions_frame, text="Edit Medication", command=self.edit_medication, bootstyle=INFO
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame, text="Delete Medication", command=self.delete_medication, bootstyle=DANGER
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_medications()

    def load_medications(self):
        """Load medications from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            medications = get_all_medications(self.db_conn)
            for medication in medications:
                self.tree.insert("", "end", values=medication)
        except Exception as e:
            Messagebox.show_error(f"Failed to load medications: {e}", title="Error")

    def search_medications(self, search_entry):
        """Search medications based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            medications = get_all_medications(self.db_conn)
            filtered_medications = [
                m for m in medications if query.lower() in m[1].lower() or query.lower() in m[3].lower()
            ]
            for medication in filtered_medications:
                self.tree.insert("", "end", values=medication)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_medication(self):
        """Open a form to add a new medication."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Medication")
        add_window.geometry("400x350")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["MedicationID", "MedicationName", "Dosage", "Manufacturer"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_medication():
            """Save the medication to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_medication_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_medications()
            except Exception as e:
                Messagebox.show_error(f"Failed to add medication: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_medication, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_medication(self):
        """Edit selected medication."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Medication")
        edit_window.geometry("400x350")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["MedicationName", "Dosage", "Manufacturer"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Skip MedicationID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_medication_record():
            """Update medication in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["MedicationID"] = values[0]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_medication(self.db_conn, data["MedicationID"], data)
                edit_window.destroy()
                self.load_medications()
            except Exception as e:
                Messagebox.show_error(f"Failed to update medication: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_medication_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_medication(self):
        """Delete selected medication."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        try:
            delete_medication(self.db_conn, values[0])  # MedicationID
            self.load_medications()
        except Exception as e:
            Messagebox.show_error(f"Failed to delete medication: {e}", title="Error")
