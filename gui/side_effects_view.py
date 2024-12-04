import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from database.basic_queries import (
    get_all_side_effects,
    add_side_effect_to_db,
    update_side_effect,
    delete_side_effect,
)


class SideEffectsView:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn

    def show(self, content_frame):
        """Display the Side Effects view."""
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
            command=lambda: self.search_side_effects(search_entry),
            bootstyle=PRIMARY,
        )
        search_button.pack(side="left", padx=5)

        add_button = tb.Button(
            search_frame,
            text="Add Side Effect",
            command=self.add_side_effect,
            bootstyle=SUCCESS,
        )
        add_button.pack(side="right", padx=5)

        # Table for displaying Side Effects
        tree_frame = tb.Frame(content_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("MedicationID", "Side Effect Description", "Severity")
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
            text="Edit Side Effect",
            command=self.edit_side_effect,
            bootstyle=INFO,
        )
        edit_button.pack(side="left", padx=5)

        delete_button = tb.Button(
            actions_frame,
            text="Delete Side Effect",
            command=self.delete_side_effect,
            bootstyle=DANGER,
        )
        delete_button.pack(side="left", padx=5)

        # Load initial data
        self.load_side_effects()

    def load_side_effects(self):
        """Load side effects from the database."""
        self.tree.delete(*self.tree.get_children())
        try:
            side_effects = get_all_side_effects(self.db_conn)
            for effect in side_effects:
                self.tree.insert("", "end", values=effect)
        except Exception as e:
            Messagebox.show_error(f"Failed to load side effects: {e}", title="Error")

    def search_side_effects(self, search_entry):
        """Search side effects based on the search query."""
        query = search_entry.get().strip()
        if not query:
            Messagebox.show_warning("Please enter a search query.", title="Warning")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            side_effects = get_all_side_effects(self.db_conn)
            filtered_effects = [
                effect for effect in side_effects if query.lower() in str(effect).lower()
            ]
            for effect in filtered_effects:
                self.tree.insert("", "end", values=effect)
        except Exception as e:
            Messagebox.show_error(f"Search failed: {e}", title="Error")

    def add_side_effect(self):
        """Open a form to add a new side effect."""
        add_window = tb.Toplevel(self.root)
        add_window.title("Add Side Effect")
        add_window.geometry("400x350")
        add_window.resizable(False, False)

        form_frame = tb.Frame(add_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        # Form fields
        fields = ["MedicationID", "SideEffectDescription", "Severity"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def save_side_effect():
            """Save the side effect to the database."""
            data = {field: entries[field].get().strip() for field in fields}
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                add_side_effect_to_db(self.db_conn, data)
                add_window.destroy()
                self.load_side_effects()
            except Exception as e:
                Messagebox.show_error(f"Failed to add side effect: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=save_side_effect, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def edit_side_effect(self):
        """Edit selected side effect."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to edit.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        edit_window = tb.Toplevel(self.root)
        edit_window.title("Edit Side Effect")
        edit_window.geometry("400x350")
        edit_window.resizable(False, False)

        form_frame = tb.Frame(edit_window, padding=20)
        form_frame.pack(fill="both", expand=True)

        fields = ["SideEffectDescription", "Severity"]
        entries = {}

        for idx, field in enumerate(fields):
            tb.Label(form_frame, text=field).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = tb.Entry(form_frame)
            entry.insert(0, values[idx + 1])  # Skip MedicationID
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            entries[field] = entry

        def update_side_effect_record():
            """Update side effect in the database."""
            data = {field: entries[field].get().strip() for field in fields}
            data["MedicationID"] = values[0]
            if not all(data.values()):
                Messagebox.show_warning("All fields are required.", title="Warning")
                return

            try:
                update_side_effect(self.db_conn, values[1], data)  # Use SideEffectDescription as key
                edit_window.destroy()
                self.load_side_effects()
            except Exception as e:
                Messagebox.show_error(f"Failed to update side effect: {e}", title="Error")

        save_button = tb.Button(form_frame, text="Save", command=update_side_effect_record, bootstyle=SUCCESS)
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def delete_side_effect(self):
        """Delete selected side effect."""
        selected_item = self.tree.focus()
        if not selected_item:
            Messagebox.show_warning("Please select a record to delete.", title="Warning")
            return

        values = self.tree.item(selected_item, "values")
        try:
            delete_side_effect(self.db_conn, values[0], values[1])  # MedicationID, SideEffectDescription
            self.load_side_effects()
        except Exception as e:
            Messagebox.show_error(f"Failed to delete side effect: {e}", title="Error")
