from database.crud_operations import insert_data
from database.db_connection import get_cursor, close_connection




def populate_healthcare_professionals(conn):
    """Insert dummy data into HealthCareProfessionals table."""
    data = [
        ("00000001", "James", "Wilson", "347-555-1122", "Cardiology"),
        ("00000002", "Laura", "Taylor", "347-555-2233", "Neurology"),
        ("00000003", "Robert", "Miller", "646-555-1212", "Orthopedics"),
        ("00000004", "Laura", "Anderson", "347-555-4455", "Emergency Medicine"),
        ("00000005", "David", "Thomas", "347-555-5566", "General Surgery"),
    ]
    query = """
    INSERT INTO HealthCareProfessionals (HCPID, FirstName, LastName, ContactNumber, Department)
    VALUES (?, ?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_patients(conn):
    """Insert dummy data into Patients table."""
    data = [
        (
            "00000001",
            "John",
            "Doe",
            "1980-05-15",
            "123 Main St, Cityville",
            "347-555-9999",
            "00000001",
        ),
        (
            "00000002",
            "Jane",
            "Smith",
            "1975-09-20",
            "456 Oak St, Townsville",
            "347-555-5678",
            "00000002",
        ),
        (
            "00000003",
            "Emily",
            "Johnson",
            "1990-12-01",
            "789 Updated Blvd, New City",
            "347-555-8765",
            "00000004",
        ),
        (
            "00000004",
            "Michael",
            "Smith",
            "1965-03-10",
            "321 Elm St, Cityville",
            "347-555-4321",
            None,
        ),
        (
            "00000005",
            "Sarah",
            "Davis",
            "2000-07-25",
            "654 Maple St, Townsville",
            "347-555-6543",
            None,
        ),
    ]
    query = """
    INSERT INTO Patients (PatientID, FirstName, LastName, DOB, Address, PhoneNumber, PrimaryHCPID)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_medications(conn):
    """Insert dummy data into Medications table."""
    data = [
        ("00000001", "Aspirin", "500mg", "PharmaCorp"),
        ("00000002", "Ibuprofen", "750mg", "HealthMeds"),
        ("00000003", "Paracetamol", "500mg", "MediCare"),
        ("00000004", "Amoxicillin", "250mg", "BioPharma"),
        ("00000005", "Ciprofloxacin", "500mg", "NewPharmaCorp"),
    ]
    query = """
    INSERT INTO Medications (MedicationID, MedicationName, Dosage, Manufacturer)
    VALUES (?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_insurance(conn):
    """Insert dummy data into Insurance table."""
    data = [
        ("00000001", "HealthPlus", "contact@healthplus.com", "917-555-6677"),
        ("00000002", "CareWell", "support@carewell.com", "212-555-7788"),
        ("00000003", "MedSecure", "info@medsecure.com", "347-555-3344"),
        ("00000004", "LifeCare", "help@lifecare.com", "917-555-9900"),
        ("00000005", "HealthPremium", "service@wellhealth.com", "646-555-1010"),
    ]
    query = """
    INSERT INTO Insurance (InsuranceID, InsuranceName, Email, ContactNumber)
    VALUES (?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_visits(conn):
    """Insert dummy data into Visits table."""
    data = [
        ('00000001', '2023-11-15', '00000001', 'Routine Check-up', 'Patient in good health. Scheduled for next visit in 6 months.'),
        ('00000002', '2023-06-20', '00000002', 'Follow-up', 'Discussed test results and adjusted medication.'),
        ('00000001', '2022-10-10', '00000003', 'Consultation', 'Referred to cardiologist for further evaluation.'),
        ('00000003', '2023-01-05', '00000004', 'Emergency Visit', 'Patient presented with severe abdominal pain. Treated and discharged.'),
        ('00000004', '2021-12-30', '00000005', 'Surgery Follow-up', 'Post-operative check-up. Healing progressing well.'),
        ('00000005', '2020-01-01', '00000001', 'Initial Visit', 'New patient intake and preliminary health assessment.'),
    ]
    query = """
    INSERT INTO Visits (PatientID, VisitDate, HCPID, Reason, Notes)
    VALUES (?, ?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_patient_insurance(conn):
    """Insert dummy data into PatientInsurance table."""
    data = [
        ('00000001', '00000001', '2023-01-01', '2024-01-01'),
        ('00000001', '00000002', '2023-02-01', '2023-12-31'),
        ('00000002', '00000003', '2023-03-01', None),
        ('00000003', '00000001', '2022-01-01', '2022-12-31'),
        ('00000003', '00000005', '2023-04-01', '2024-03-31'),
    ]
    query = """
    INSERT INTO PatientInsurance (PatientID, InsuranceID, CoverageStartDate, CoverageEndDate)
    VALUES (?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_side_effects(conn):
    """Insert dummy data into SideEffects table."""
    data = [
        ("00000001", "Nausea", "Mild"),
        ("00000001", "Headache", "Moderate"),
        ("00000001", "Dizziness", "Severe"),
        ("00000002", "Dizziness", "Mild"),
        ("00000003", "Headache", "Moderate"),
        ("00000004", "Diarrhea", "Severe"),
        ("00000005", "Rash", "Mild"),
    ]
    query = """
    INSERT INTO SideEffects (MedicationID, SideEffectDescription, Severity)
    VALUES (?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_hcp_departments(conn):
    """Insert dummy data into HCPDepartments table."""
    data = [
        ("00000001", "Cardiology"),
        ("00000002", "Neurology"),
        ("00000003", "Orthopedics"),
        ("00000004", "Pediatrics"),
        ("00000005", "General Surgery"),
        ("00000002", "General Medicine"),
        ("00000003", "Sports Medicine"),
        ("00000004", "Neonatology"),
        ("00000005", "Trauma Surgery"),
    ]
    query = """
    INSERT INTO HCPDepartments (HCPID, DepartmentName)
    VALUES (?, ?)
    """
    for record in data:
        insert_data(conn, query, record)


def populate_patient_medications(conn):
    """Insert dummy data into PatientMedications table."""
    data = [
        ('00000001', '00000001', '2023-01-01', '2023-06-01', '500mg'),
        ('00000001', '00000003', '2023-02-01', '2023-07-01', '500mg'),
        ('00000002', '00000002', '2023-03-01', '2023-08-01', '350mg'),
        ('00000002', '00000004', '2023-04-01', '2023-09-01', '250mg'),
        ('00000003', '00000005', '2023-05-01', '2023-10-01', '100mg'),
        ('00000004', '00000003', '2023-06-01', '2023-11-01', '60mg'),
        ('00000005', '00000001', '2023-07-01', '2023-12-01', '50mg'),
    ]
    query = """
    INSERT INTO PatientMedications (PatientID, MedicationID, StartDate, EndDate, Dosage)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    for record in data:
        insert_data(conn, query, record)



def populate_all_tables():
    """Populate all tables with dummy data."""
    conn = get_cursor()[1]  # Get the database connection
    try:
        # populate_healthcare_professionals(conn)
        # populate_patients(conn)
        # populate_medications(conn)
        # populate_insurance(conn)
        # populate_visits(conn)
        # populate_patient_insurance(conn)
        # populate_side_effects(conn)
        # populate_hcp_departments(conn)
        populate_patient_medications(conn)
    finally:
        close_connection(conn, None)


if __name__ == "__main__":
    populate_all_tables()
