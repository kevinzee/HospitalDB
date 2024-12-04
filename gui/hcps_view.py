import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from database.basic_queries import get_all_hcps, add_hcp_to_db, update_hcp, delete_hcp


class HCPsView:
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
        """Display the HCPs view."""
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
            command=lambda: self.search_hcps(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame,
            text="Add HCP",
            command=self.add_hcp,
            bootstyle=SUCCESS,
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying HCPs
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("HCPID", "First Name", "Last Name", "Contact Number", "Department")
        self.tree = tb.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")

        # Configure columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # Hide default column
        self.tree.column("HCPID", anchor="center", width=100)
        self.tree.column("First Name", anchor="w", width=150)
        self.tree.column("Last Name", anchor="w", width=150)
        self.tree.column("Contact Number", anchor="center", width=120)
        self.tree.column("Department", anchor="w", width=200)

        # Add headers
        self.tree.heading("HCPID", text="HCP ID", anchor="center")
        self.tree.heading("First Name", text="First Name", anchor="w")
        self.tree.heading("Last Name", text="Last Name", anchor="w")
        self.tree.heading("Contact Number", text="Contact Number", anchor="center")
        self.tree.heading("Department", text="Department", anchor="w")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = tb.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        actions_frame = tb.Frame(content_frame)
        actions_frame.pack(side="bottom", fill="x", pady=10)

        edit_button = tb.Button(
            actions_frame, text="Edit HCP", command=self.edit_hcp, bootstyle=INFO
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame, text="Delete HCP", command=self.delete_hcp, bootstyle=DANGER
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_hcps()

    def load_hcps(self):
        """Load HCPs from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            hcps = get_all_hcps(self.db_conn)
            for idx, hcp in enumerate(hcps):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=hcp, tags=(tag,))
            self.tree.tag_configure("evenrow", background="#f9f9f9")
            self.tree.tag_configure("oddrow", background="#ffffff")
        except Exception as e:
            Messagebox.show_error(f"Failed to load HCPs: {e}", title="Error")

    def search_hcps(self, search_entry):
        """Search HCPs based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            hcps = get_all_hcps(self.db_conn)
            filtered_hcps = [
                h for h in hcps if query.lower() in h[1].lower() or query.lower() in h[2].lower()
            ]
            for hcp in filtered_hcps:
                self.tree.insert("", "end", values=hcp)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_hcp(self):
        """Open a form to add a new healthcare professional."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Healthcare Professional")
        add_window.geometry("400x400")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["HCPID", "FirstName", "LastName", "ContactNumber", "Department"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_hcp():
            """Save the HCP to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_hcp_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_hcps()
            except Exception as e:
                Messagebox.show_error(f"Failed to add HCP: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_hcp, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_hcp(self):
        """Edit selected HCP."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Healthcare Professional")
        edit_window.geometry("400x350")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["FirstName", "LastName", "ContactNumber", "Department"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Skip HCPID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_hcp_record():
            """Update HCP in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["HCPID"] = values[0]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_hcp(self.db_conn, data["HCPID"], data)
                edit_window.destroy()
                self.load_hcps()
            except Exception as e:
                Messagebox.show_error(f"Failed to update HCP: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_hcp_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_hcp(self):
        """Delete selected healthcare professional (HCP)."""
        # Get the selected item
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        # Retrieve the HCPID from the selected row
        values = self.tree.item(selected_item, "values")
        if not values:
            Messagebox.show_error("Failed to retrieve the selected HCP's details.", title="Error")
            return

        hcp_id = values[0]  # Assuming the first column is the HCPID

        # Confirm deletion with the user
        confirm = Messagebox.okcancel(
            message=f"Are you sure you want to delete the healthcare professional with ID '{hcp_id}'?",
            title="Confirm Deletion",
            alert=True
        )
        if not confirm:
            return

        try:
            # Call the database method to delete the HCP
            delete_hcp(self.db_conn, hcp_id)
            # Remove the deleted item from the Treeview
            self.tree.delete(selected_item)
            Messagebox.show_info(f"Healthcare professional with ID '{hcp_id}' deleted successfully.", title="Success")
        except Exception as e:
            Messagebox.show_error(f"Failed to delete HCP: {e}", title="Error")
