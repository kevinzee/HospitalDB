import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from database.basic_queries import get_all_visits, add_visit_to_db, update_visit, delete_visit


class VisitsView:
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
        """Display the Visits view."""
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
            command=lambda: self.search_visits(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame,
            text="Add Visit",
            command=self.add_visit,
            bootstyle=SUCCESS,
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying Visits
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("PatientID", "VisitDate", "HCPID", "Reason", "Notes")
        self.tree = tb.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
        self.tree.column("PatientID", anchor="center", width=100)
        self.tree.column("VisitDate", anchor="center", width=120)
        self.tree.column("HCPID", anchor="center", width=100)
        self.tree.column("Reason", anchor="w", width=200)
        self.tree.column("Notes", anchor="w", width=250)

        # Add headers
        self.tree.heading("PatientID", text="Patient ID", anchor="center")
        self.tree.heading("VisitDate", text="Visit Date", anchor="center")
        self.tree.heading("HCPID", text="HCP ID", anchor="center")
        self.tree.heading("Reason", text="Reason", anchor="w")
        self.tree.heading("Notes", text="Notes", anchor="w")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
                # Action buttons
        actions_frame = tb.Frame(content_frame)
        actions_frame.pack(side="bottom", fill="x", pady=10)

        edit_button = tb.Button(
            actions_frame, text="Edit Visit", command=self.edit_visit, bootstyle=INFO
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame, text="Delete Visit", command=self.delete_visit, bootstyle=DANGER
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_visits()

    def load_visits(self):
        """Load visits from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            visits = get_all_visits(self.db_conn)
            # Ensure the data matches the order of Treeview columns: PatientID, VisitDate, HCPID, Reason, Notes
            for idx, visit in enumerate(visits):
                patient_id, visit_date, hcp_id, reason, notes = visit  # Adjust to match your query results
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(patient_id, visit_date, hcp_id, reason, notes), tags=(tag,))
            self.tree.tag_configure("evenrow", background="#f9f9f9")
            self.tree.tag_configure("oddrow", background="#ffffff")
        except Exception as e:
            Messagebox.show_error(f"Failed to load visits: {e}", title="Error")


    def search_visits(self, search_entry):
        """Search visits based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            visits = get_all_visits(self.db_conn)
            filtered_visits = [
                v for v in visits if query.lower() in str(v).lower()
            ]
            for visit in filtered_visits:
                self.tree.insert("", "end", values=visit)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_visit(self):
        """Open a form to add a new visit."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Visit")
        add_window.geometry("400x400")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["PatientID", "VisitDate", "HCPID", "Reason", "Notes"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_visit():
            """Save the visit to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_visit_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_visits()
            except Exception as e:
                Messagebox.show_error(f"Failed to add visit: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_visit, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_visit(self):
        """Edit selected visit."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            Messagebox.show_error("Failed to retrieve the selected visit's details.", title="Error")
            return

        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Visit")
        edit_window.geometry("400x400")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["VisitDate", "HCPID", "Reason", "Notes"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Start from index 1 to skip PatientID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_visit_record():
            """Update visit in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_visit(self.db_conn, values[0], values[1], data)  # PatientID, VisitDate, and data
                edit_window.destroy()
                self.load_visits()
                Messagebox.show_info(f"Visit on '{values[1]}' updated successfully.", title="Success")
            except Exception as e:
                Messagebox.show_error(f"Failed to update visit: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_visit_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)


    def delete_visit(self):
        """Delete selected visit."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            Messagebox.show_error("Failed to retrieve the selected visit details.", title="Error")
            return

        patient_id = values[0]  # Patient ID
        visit_date = values[1]  # Visit Date

        # Confirm deletion with the user
        confirm = Messagebox.okcancel(
            message=f"Are you sure you want to delete patient {patient_id}'s visit on '{visit_date}'?",
            title="Confirm Deletion",
            alert=True
        )
        if not confirm:
            return

        try:
            delete_visit(self.db_conn, patient_id, visit_date)
            self.tree.delete(selected_item)
            Messagebox.show_info(f"Visit on '{visit_date}' deleted successfully.", title="Success")
        except Exception as e:
            Messagebox.show_error(f"Failed to delete visit: {e}", title="Error")
