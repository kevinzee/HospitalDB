import ttkbootstrap as tb
from ttkbootstrap.constants import *
from gui.patients_view import PatientsView
from gui.hcps_view import HCPsView
from gui.insurance_view import InsuranceView
from gui.visits_view import VisitsView
from gui.medications_view import MedicationsView
from gui.patient_medications_view import PatientMedicationsView
from gui.patient_insurance_view import PatientInsuranceView
from gui.side_effects_view import SideEffectsView
from gui.hcp_departments_view import HCPDepartmentsView


class HospitalAppGUI:
    def __init__(self, root, db_conn):
        self.root = root
        self.db_conn = db_conn
        self.root.title("Hospital Management System")
        self.root.geometry("1200x800")
        self.setup_main_frames()

        # Initialize views
        self.patients_view = PatientsView(self.root, self.db_conn)
        self.hcps_view = HCPsView(self.root, self.db_conn)
        self.insurance_view = InsuranceView(self.root, self.db_conn)
        self.visits_view = VisitsView(self.root, self.db_conn)
        self.medications_view = MedicationsView(self.root, self.db_conn)
        self.patient_medications_view = PatientMedicationsView(self.root, self.db_conn)
        self.patient_insurance_view = PatientInsuranceView(self.root, self.db_conn)
        self.side_effects_view = SideEffectsView(self.root, self.db_conn)
        self.hcp_departments_view = HCPDepartmentsView(self.root, self.db_conn)

    def setup_main_frames(self):
        # Header
        header_frame = tb.Frame(self.root, padding=10)
        header_frame.pack(side="top", fill="x")

        header_label = tb.Label(
            header_frame,
            text="Hospital Management System",
            font=("TkDefaultFont", 24),
            anchor="center",
        )
        header_label.pack()

        # Sidebar
        sidebar_frame = tb.Frame(self.root, padding=10)
        sidebar_frame.pack(side="left", fill="y")

        # Buttons for each view
        tb.Button(
            sidebar_frame, text="Patients", command=lambda: self.patients_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Healthcare Professionals", command=lambda: self.hcps_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Insurance", command=lambda: self.insurance_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Visits", command=lambda: self.visits_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Medications", command=lambda: self.medications_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Patient Medications", command=lambda: self.patient_medications_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Patient Insurance", command=lambda: self.patient_insurance_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="Side Effects", command=lambda: self.side_effects_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        tb.Button(
            sidebar_frame, text="HCP Departments", command=lambda: self.hcp_departments_view.show(self.content_frame), bootstyle=PRIMARY
        ).pack(fill="x", pady=5)

        # Main Content Area
        self.content_frame = tb.Frame(self.root, padding=10)
        self.content_frame.pack(side="right", fill="both", expand=True)


if __name__ == "__main__":
    from database.db_connection import connect_to_db

    app = tb.Window(themename="journal")
    conn = connect_to_db()
    gui = HospitalAppGUI(app, conn)
    app.mainloop()
