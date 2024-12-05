import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from database.basic_queries import (
    get_all_hcp_departments,
    add_hcp_department_to_db,
    update_hcp_department,
    delete_hcp_department,
)


class HCPDepartmentsView:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn

    def show(self, content_frame):
        """Display the HCP Departments view."""
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
            command=lambda: self.search_hcp_departments(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame,
            text="Add HCP Department",
            command=self.add_hcp_department,
            bootstyle=SUCCESS,
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying HCP Departments
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("HCPID", "Department Name")
        self.tree = tb.Treeview(
            tree_frame, columns=columns, show="headings", style="Treeview"
        )

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
        self.tree.column("HCPID", anchor="center", width=150)
        self.tree.column("Department Name", anchor="w", width=300)

        # Add headers
        self.tree.heading("HCPID", text="HCP ID", anchor="center")
        self.tree.heading("Department Name", text="Department Name", anchor="w")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        actions_frame = tb.Frame(content_frame)
        actions_frame.pack(side="bottom", fill="x", pady=10)

        edit_button = tb.Button(
            actions_frame,
            text="Edit HCP Department",
            command=self.edit_hcp_department,
            bootstyle=INFO,
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame,
            text="Delete HCP Department",
            command=self.delete_hcp_department,
            bootstyle=DANGER,
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_hcp_departments()

    def load_hcp_departments(self):
        """Load HCP departments from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            hcp_departments = get_all_hcp_departments(self.db_conn)
            for idx, department in enumerate(hcp_departments):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=department, tags=(tag,))
            self.tree.tag_configure("evenrow", background="#f9f9f9")
            self.tree.tag_configure("oddrow", background="#ffffff")
        except Exception as e:
            Messagebox.show_error(f"Failed to load HCP departments: {e}", title="Error")

    def search_hcp_departments(self, search_entry):
        """Search HCP departments based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            hcp_departments = get_all_hcp_departments(self.db_conn)
            filtered_departments = [
                department
                for department in hcp_departments
                if query.lower() in str(department).lower()
            ]
            for department in filtered_departments:
                self.tree.insert("", "end", values=department)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_hcp_department(self):
        """Open a form to add a new HCP department."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add HCP Department")
        add_window.geometry("400x350")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["HCPID", "DepartmentName"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(
                row=idx, column=0, padx=5, pady=5, sticky="e"
            )
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_hcp_department():
            """Save the HCP department to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_hcp_department_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_hcp_departments()
            except Exception as e:
                Messagebox.show_error(
                    f"Failed to add HCP department: {e}", title="Error"
                )

        save_button = tb.Button(
            form_frame, text="Save", command=save_hcp_department, bootstyle=SUCCESS
        )
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_hcp_department(self):
        """Edit selected HCP department."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit HCP Department")
        edit_window.geometry("400x350")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["DepartmentName"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(
                row=idx, column=0, padx=5, pady=5, sticky="e"
            )
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Skip HCPID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_hcp_department_record():
            """Update HCP department in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["HCPID"] = values[0]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_hcp_department(self.db_conn, values[0], data)
                edit_window.destroy()
                self.load_hcp_departments()
            except Exception as e:
                Messagebox.show_error(
                    f"Failed to update HCP department: {e}", title="Error"
                )

        save_button = tb.Button(
            form_frame,
            text="Save",
            command=update_hcp_department_record,
            bootstyle=SUCCESS,
        )
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_hcp_department(self):
        """Delete selected HCP department."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning(
                "Please select a record to delete.", title="Warning"
            )
            return

        values = self.tree.item(selected_item, "values")
        if not values:
            Messagebox.show_error(
                "Failed to retrieve the selected HCP department's details.",
                title="Error",
            )
            return

        hcp_id = values[0]
        department_name = values[1]

        confirm = Messagebox.okcancel(
            message=f"Are you sure you want to delete the department '{department_name}' for HCP ID '{hcp_id}'?",
            title="Confirm Deletion",
            alert=True,
        )
        if not confirm:
            return

        try:
            delete_hcp_department(self.db_conn, hcp_id, department_name)
            self.load_hcp_departments()
            Messagebox.show_info(
                f"Department '{department_name}' for HCP ID '{hcp_id}' deleted successfully.",
                title="Success",
            )
        except Exception as e:
            Messagebox.show_error(
                f"Failed to delete HCP department: {e}", title="Error"
            )