from database.crud_operations import fetch_data, execute_query
from database.db_connection import close_connection, get_cursor


# -------------------------
# Patients
# -------------------------

def get_all_patients(conn):
    """Retrieve all patients from the Patients table."""
    query = "SELECT * FROM Patients"
    return fetch_data(conn, query)

def add_patient_to_db(conn, data):
    """Insert a new patient into the Patients table."""
    query = """
    INSERT INTO Patients (PatientID, FirstName, LastName, DOB, Address, PhoneNumber, PrimaryHCPID)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data["PatientID"],
        data["FirstName"],
        data["LastName"],
        data["DOB"],
        data["Address"],
        data["PhoneNumber"],
        data["PrimaryHCPID"]
    )
    execute_query(conn, query, params)

def update_patient(conn, patient_id, data):
    """Update an existing patient's information."""
    query = """
    UPDATE Patients
    SET FirstName = %s, LastName = %s, DOB = %s, Address = %s, PhoneNumber = %s, PrimaryHCPID = %s
    WHERE PatientID = %s
    """
    params = (
        data["FirstName"],
        data["LastName"],
        data["DOB"],
        data["Address"],
        data["PhoneNumber"],
        data["PrimaryHCPID"],
        patient_id
    )
    execute_query(conn, query, params)

def delete_patient(conn, patient_id):
    """Delete a patient by PatientID."""
    query = "DELETE FROM Patients WHERE PatientID = %s"
    try:
        execute_query(conn, query, (patient_id,))
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")


# -------------------------
# HealthCareProfessionals
# -------------------------

def get_all_hcps(conn):
    """Retrieve all healthcare professionals from the HealthCareProfessionals table."""
    query = "SELECT * FROM HealthCareProfessionals"
    return fetch_data(conn, query)

def add_hcp_to_db(conn, data):
    """Insert a new health care professional into the HealthCareProfessionals table."""
    query = """
    INSERT INTO HealthCareProfessionals (HCPID, FirstName, LastName, ContactNumber, Department)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data["HCPID"],
        data["FirstName"],
        data["LastName"],
        data["ContactNumber"],
        data["Department"]
    )
    execute_query(conn, query, params)

def update_hcp(conn, hcp_id, data):
    """Update an existing healthcare professional's information."""
    query = """
    UPDATE HealthCareProfessionals
    SET FirstName = %s, LastName = %s, ContactNumber = %s, Department = %s
    WHERE HCPID = %s
    """
    params = (
        data["FirstName"],
        data["LastName"],
        data["ContactNumber"],
        data["Department"],
        hcp_id
    )
    execute_query(conn, query, params)

def delete_hcp(conn, hcp_id):
    """Delete a healthcare professional by HCPID."""
    query = "DELETE FROM HealthCareProfessionals WHERE HCPID = %s"
    execute_query(conn, query, (hcp_id,))


# -------------------------
# Insurance
# -------------------------

def get_all_insurance(conn):
    """Retrieve all insurance info from the Insurance table."""
    query = "SELECT * FROM Insurance"
    return fetch_data(conn, query)

def add_insurance_to_db(conn, data):
    """Insert a new insurance entry into the Insurance table."""
    query = """
    INSERT INTO Insurance (InsuranceID, InsuranceName, Email, ContactNumber)
    VALUES (%s, %s, %s, %s)
    """
    params = (
        data["InsuranceID"],
        data["InsuranceName"],
        data["Email"],
        data["ContactNumber"]
    )
    execute_query(conn, query, params)

def update_insurance(conn, insurance_id, data):
    """Update an existing insurance provider's information."""
    query = """
    UPDATE Insurance
    SET InsuranceName = %s, Email = %s, ContactNumber = %s
    WHERE InsuranceID = %s
    """
    params = (
        data["InsuranceName"],
        data["Email"],
        data["ContactNumber"],
        insurance_id
    )
    execute_query(conn, query, params)

def delete_insurance(conn, insurance_id):
    """Delete an insurance provider by InsuranceID."""
    query = "DELETE FROM Insurance WHERE InsuranceID = %s"
    execute_query(conn, query, (insurance_id,))


# -------------------------
# HCPDepartments
# -------------------------

def get_all_hcp_departments(conn):
    """Retrieve all entries from the HCPDepartments table."""
    query = "SELECT * FROM HCPDepartments"
    return fetch_data(conn, query)

def add_hcp_department_to_db(conn, data):
    """Insert a new department into the HCPDepartments table."""
    query = """
    INSERT INTO HCPDepartments (HCPID, DepartmentName)
    VALUES (%s, %s)
    """
    params = (
        data["HCPID"],
        data["DepartmentName"]
    )
    execute_query(conn, query, params)

def update_hcp_department(conn, hcp_id, department_name, data):
    """Update an existing department."""
    query = """
    UPDATE HCPDepartments
    SET DepartmentName = %s
    WHERE HCPID = %s AND DepartmentName = %s
    """
    params = (
        data["NewDepartmentName"],
        hcp_id,
        department_name
    )
    execute_query(conn, query, params)

def delete_hcp_department(conn, hcp_id, department_name):
    """Delete a department entry."""
    query = "DELETE FROM HCPDepartments WHERE HCPID = %s AND DepartmentName = %s"
    execute_query(conn, query, (hcp_id, department_name))

# -------------------------
# Visits
# -------------------------

def get_all_visits(conn):
    """Retrieve all entries from the Visits table."""
    query = "SELECT * FROM Visits"
    return fetch_data(conn, query)

def add_visit_to_db(conn, data):
    """Insert a new visit into the Visits table."""
    query = """
    INSERT INTO Visits (PatientID, VisitDate, HCPID, Reason, Notes)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data["PatientID"],
        data["VisitDate"],
        data["HCPID"],
        data["Reason"],
        data["Notes"]
    )
    execute_query(conn, query, params)


def update_visit(conn, patient_id, visit_date, data):
    """Update an existing visit's details."""
    query = """
    UPDATE Visits
    SET VisitDate = %s, HCPID = %s, Reason = %s, Notes = %s
    WHERE PatientID = %s AND VisitDate = %s
    """
    params = (
        data["VisitDate"],
        data["HCPID"],
        data["Reason"],
        data["Notes"],
        patient_id,
        visit_date
    )
    execute_query(conn, query, params)


def delete_visit(conn, patient_id, visit_date):
    """Delete a visit by PatientID and VisitDate."""
    query = "DELETE FROM Visits WHERE PatientID = %s AND VisitDate = %s"
    execute_query(conn, query, (patient_id, visit_date))


# -------------------------
# Medications
# -------------------------

def get_all_medications(conn):
    """Retrieve all medications from the Medications table."""
    query = "SELECT * FROM Medications"
    return fetch_data(conn, query)

def add_medication_to_db(conn, data):
    """Insert a new medication into the Medications table."""
    query = """
    INSERT INTO Medications (MedicationID, MedicationName, Dosage, Manufacturer)
    VALUES (%s, %s, %s, %s)
    """
    params = (
        data["MedicationID"],
        data["MedicationName"],
        data["Dosage"],
        data["Manufacturer"]
    )
    execute_query(conn, query, params)

def update_medication(conn, medication_id, data):
    """Update an existing medication's information."""
    query = """
    UPDATE Medications
    SET MedicationName = %s, Dosage = %s, Manufacturer = %s
    WHERE MedicationID = %s
    """
    params = (
        data["MedicationName"],
        data["Dosage"],
        data["Manufacturer"],
        medication_id
    )
    execute_query(conn, query, params)

def delete_medication(conn, medication_id):
    """Delete a medication by MedicationID."""
    query = "DELETE FROM Medications WHERE MedicationID = %s"
    execute_query(conn, query, (medication_id,))


# -------------------------
# PatientInsurance
# -------------------------

def get_all_patient_insurance(conn):
    """Retrieve all entries from the PatientInsurance table."""
    query = "SELECT * FROM PatientInsurance"
    return fetch_data(conn, query)

def add_patient_insurance_to_db(conn, data):
    """Insert a new entry into the PatientInsurance table."""
    query = """
    INSERT INTO PatientInsurance (PatientID, InsuranceID)
    VALUES (%s, %s)
    """
    params = (
        data["PatientID"],
        data["InsuranceID"]
    )
    execute_query(conn, query, params)

def update_patient_insurance(conn, patient_id, insurance_id, data):
    """Update a patient-insurance entry."""
    query = """
    UPDATE PatientInsurance
    SET InsuranceID = %s
    WHERE PatientID = %s AND InsuranceID = %s
    """
    params = (
        data["InsuranceID"],
        patient_id,
        insurance_id
    )
    execute_query(conn, query, params)

def delete_patient_insurance(conn, patient_id, insurance_id):
    """Delete a patient-insurance entry."""
    query = "DELETE FROM PatientInsurance WHERE PatientID = %s AND InsuranceID = %s"
    execute_query(conn, query, (patient_id, insurance_id))

# -------------------------
# PatientMedications
# -------------------------

def get_all_patient_medications(conn):
    """Retrieve all entries from the PatientMedications table."""
    query = "SELECT * FROM PatientMedications"
    return fetch_data(conn, query)

def add_patient_medication_to_db(conn, data):
    """Insert a new entry into the PatientMedications table."""
    query = """
    INSERT INTO PatientMedications (PatientID, MedicationID, MedicationName, StartDate, EndDate, Dosage)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        data["PatientID"],
        data["MedicationID"],
        data["MedicationName"],
        data["StartDate"],
        data["EndDate"],
        data["Dosage"],
    )
    execute_query(conn, query, params)

def update_patient_medication(conn, patient_id, medication_id, data):
    """Update a patient-medication entry."""
    query = """
    UPDATE PatientMedications
    SET MedicationName = %s, StartDate = %s, EndDate = %s, Dosage = %s
    WHERE PatientID = %s AND MedicationID = %s
    """
    params = (
        data["MedicationName"],
        data["StartDate"],
        data["EndDate"],
        data["Dosage"],
        patient_id,
        medication_id,
    )
    execute_query(conn, query, params)

def delete_patient_medication(conn, patient_id, medication_id):
    """Delete a patient-medication entry."""
    query = "DELETE FROM PatientMedications WHERE PatientID = %s AND MedicationID = %s"
    execute_query(conn, query, (patient_id, medication_id))


# -------------------------
# SideEffects
# -------------------------

def get_all_side_effects(conn):
    """Retrieve all entries from the SideEffects table."""
    query = "SELECT * FROM SideEffects"
    return fetch_data(conn, query)

def add_side_effect_to_db(conn, data):
    """Insert a new side effect into the SideEffects table."""
    query = """
    INSERT INTO SideEffects (MedicationID, SideEffectDescription, Severity)
    VALUES (%s, %s, %s)
    """
    params = (
        data["MedicationID"],
        data["SideEffectDescription"],
        data["Severity"]
    )
    execute_query(conn, query, params)

def update_side_effect(conn, medication_id, side_effect_description, data):
    """Update a side effect entry."""
    query = """
    UPDATE SideEffects
    SET Severity = %s, SideEffectDescription = %s
    WHERE MedicationID = %s AND SideEffectDescription = %s
    """
    params = (
        data["Severity"],
        data["SideEffectDescription"],
        medication_id,
        side_effect_description
    )
    execute_query(conn, query, params)

def delete_side_effect(conn, medication_id, side_effect_description):
    """Delete a side effect entry."""
    query = "DELETE FROM SideEffects WHERE MedicationID = %s AND SideEffectDescription = %s"
    execute_query(conn, query, (medication_id, side_effect_description))


def test_basic_queries():
    """Test some basic queries for validation."""
    conn = get_cursor()[1]
    try:
        print("All Patients:")
        print(get_all_patients(conn))

        print("\nAll Visits:")
        print(get_all_visits(conn))

        print("\nAll Medications:")
        print(get_all_medications(conn))

        print("\nAll Patient Insurances:")
        print(get_all_patient_insurance(conn))

        print("\nAll Patient Medications:")
        print(get_all_patient_medications(conn))

        print("\nAll Side Effects:")
        print(get_all_side_effects(conn))
    finally:
        close_connection(conn, None)
