import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from database.basic_queries import get_all_insurance, add_insurance_to_db, update_insurance, delete_insurance


class InsuranceView:
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
        """Display the Insurance view."""
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
            command=lambda: self.search_insurance(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame,
            text="Add Insurance",
            command=self.add_insurance,
            bootstyle=SUCCESS,
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying Insurance
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("InsuranceID", "Insurance Name", "Email", "Contact Number")
        self.tree = tb.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
        self.tree.column("InsuranceID", anchor="center", width=100)
        self.tree.column("Insurance Name", anchor="w", width=150)
        self.tree.column("Email", anchor="w", width=200)
        self.tree.column("Contact Number", anchor="center", width=120)

        # Add headers
        self.tree.heading("InsuranceID", text="Insurance ID", anchor="center")
        self.tree.heading("Insurance Name", text="Insurance Name", anchor="w")
        self.tree.heading("Email", text="Email", anchor="w")
        self.tree.heading("Contact Number", text="Contact Number", anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        actions_frame = tb.Frame(content_frame)
        actions_frame.pack(side="bottom", fill="x", pady=10)

        edit_button = tb.Button(
            actions_frame, text="Edit Insurance", command=self.edit_insurance, bootstyle=INFO
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame, text="Delete Insurance", command=self.delete_insurance, bootstyle=DANGER
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_insurance()

    def load_insurance(self):
        """Load insurance records from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            insurances = get_all_insurance(self.db_conn)
            for idx, insurance in enumerate(insurances):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=insurance, tags=(tag,))
            self.tree.tag_configure("evenrow", background="#f9f9f9")
            self.tree.tag_configure("oddrow", background="#ffffff")
        except Exception as e:
            Messagebox.show_error(f"Failed to load insurance records: {e}", title="Error")

    def search_insurance(self, search_entry):
        """Search insurance records based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            insurances = get_all_insurance(self.db_conn)
            filtered_insurances = [
                i for i in insurances if query.lower() in i[1].lower() or query.lower() in i[2].lower()
            ]
            for insurance in filtered_insurances:
                self.tree.insert("", "end", values=insurance)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_insurance(self):
        """Open a form to add a new insurance record."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Insurance")
        add_window.geometry("400x300")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["InsuranceID", "InsuranceName", "Email", "ContactNumber"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_insurance():
            """Save the insurance record to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_insurance_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_insurance()
            except Exception as e:
                Messagebox.show_error(f"Failed to add insurance: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_insurance, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_insurance(self):
        """Edit selected insurance record."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Insurance")
        edit_window.geometry("400x300")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["InsuranceName", "Email", "ContactNumber"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Skip InsuranceID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_insurance_record():
            """Update insurance in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["InsuranceID"] = values[0]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_insurance(self.db_conn, data["InsuranceID"], data)
                edit_window.destroy()
                self.load_insurance()
            except Exception as e:
                Messagebox.show_error(f"Failed to update insurance: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_insurance_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_insurance(self):
        """Delete selected insurance record."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            Messagebox.show_error("Failed to retrieve the selected insurance's details.", title="Error")
            return

        insurance_id = values[0]  # Assuming the first column is the InsuranceID

        # Confirm deletion with the user
        confirm = Messagebox.okcancel(
            message=f"Are you sure you want to delete the insurance with ID '{insurance_id}'?",
            title="Confirm Deletion",
            alert=True
        )
        if not confirm:
            return

        try:
            # Call the database method to delete the insurance
            delete_insurance(self.db_conn, insurance_id)
            # Remove the deleted item from the Treeview
            self.tree.delete(selected_item)
            Messagebox.show_info(f"Insurance with ID '{insurance_id}' deleted successfully.", title="Success")
        except Exception as e:
            Messagebox.show_error(f"Failed to delete insurance: {e}", title="Error")