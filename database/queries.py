from database.crud_operations import fetch_data
from database.db_connection import get_cursor, close_connection


def get_all_patients(conn):
    """Retrieve all patients from the Patients table."""
    query = "SELECT * FROM Patients"
    return fetch_data(conn, query)

def get_all_hcps(conn):
    """Retrieve all patients from the HCP table."""
    query = "SELECT * FROM HealthCareProfessionals"
    return fetch_data(conn, query)

def get_all_insurance(conn):
    """Retrieve all insurance info from the Insurance table."""
    query = "SELECT * FROM Insurance"
    return fetch_data(conn, query)

def get_all_patientinsurance(conn):
    """Retrieve all patient's insurance info from the PatientInsurance table."""
    query = "SELECT * FROM PatientInsurance"
    return fetch_data(conn, query)

def get_all_medications(conn):
    """Retrieve all medications from the Medications table."""
    query = "SELECT * FROM Medications"
    return fetch_data(conn, query)

def get_all_patientmedications(conn):
    """Retrieve all medications from the PatientMedications table."""
    query = "SELECT * FROM PatientMedications"
    return fetch_data(conn, query)

def get_all_departments(conn):
    """Retrieve all departments from the HCP Departments table."""
    query = "SELECT * FROM HCPDepartments"
    return fetch_data(conn, query)

def get_all_sideEffects(conn):
    """Retrieve all side effects from the SideEffects table."""
    query = "SELECT * FROM SideEffects"
    return fetch_data(conn, query)

def get_all_visits(conn):
    """Retrieve all patient visits."""
    query = "SELECT * FROM Visits"
    return fetch_data(conn, query)


def get_patients_without_visits(conn):
    """Retrieve patients who have never visited the hospital."""
    query = """
    SELECT p.PatientID, p.FirstName, p.LastName
    FROM Patients p
    WHERE NOT EXISTS (
        SELECT 1
        FROM Visits v
        WHERE v.PatientID = p.PatientID
    )
    """
    return fetch_data(conn, query)


def get_patients_by_insurance(conn, insurance_id):
    """Retrieve all patients covered by a specific insurance provider."""
    query = """
    SELECT p.PatientID, p.FirstName, p.LastName
    FROM Patients p
    WHERE p.PatientID IN (
        SELECT pi.PatientID
        FROM PatientInsurance pi
        WHERE pi.InsuranceID = ?
    )
    """
    return fetch_data(conn, query, (insurance_id,))


def get_patients_with_multiple_medications(conn):
    """Retrieve patients who are prescribed more than one medication."""
    query = """
    SELECT pm.PatientID
    FROM PatientMedications pm
    GROUP BY pm.PatientID
    HAVING COUNT(pm.MedicationID) > 1
    """
    return fetch_data(conn, query)


def get_patients_by_medication(conn, medication_name):
    """Retrieve patients taking a specific medication."""
    query = """
    SELECT p.PatientID, p.FirstName, p.LastName
    FROM Patients p
    WHERE p.PatientID IN (
        SELECT pm.PatientID
        FROM PatientMedications pm
        WHERE pm.MedicationID = (
            SELECT m.MedicationID
            FROM Medications m
            WHERE m.MedicationName = ?
        )
    )
    """
    return fetch_data(conn, query, (medication_name,))


def get_visit_count_per_patient(conn):
    """Retrieve the number of visits each patient has made."""
    query = """
    SELECT p.PatientID, p.FirstName, p.LastName,
           (SELECT COUNT(*)
            FROM Visits v
            WHERE v.PatientID = p.PatientID) VisitCount
    FROM Patients p
    """
    return fetch_data(conn, query)


def get_departments_without_patients(conn):
    """Retrieve departments with no patients assigned to their healthcare professionals."""
    query = """
    SELECT h.Department
    FROM HealthCareProfessionals h
    WHERE NOT EXISTS (
        SELECT 1
        FROM Patients p
        WHERE p.PrimaryHCPID = h.HCPID
    )
    """
    return fetch_data(conn, query)


def get_patients_over_age(conn, age):
    """Retrieve all patients over a certain age."""
    query = """
    SELECT p.PatientID, p.FirstName, p.LastName, p.DOB
    FROM Patients p
    WHERE TIMESTAMPDIFF(YEAR, p.DOB, CURDATE()) > ?
    """
    return fetch_data(conn, query, (age,))


def get_healthcare_professionals_by_department(conn, department):
    """Retrieve all healthcare professionals in a specific department."""
    query = """
    SELECT h.HCPID, h.FirstName, h.LastName, h.ContactNumber
    FROM HealthCareProfessionals h
    WHERE h.Department = ?
    """
    return fetch_data(conn, query, (department,))


def get_medications_and_side_effects(conn):
    """Retrieve all medications and their associated side effects."""
    query = """
    SELECT m.MedicationName, m.Dosage,
           (SELECT GROUP_CONCAT(CONCAT(Severity, ': ', SideEffectDescription) SEPARATOR '; ')
            FROM SideEffects s
            WHERE s.MedicationID = m.MedicationID) SideEffects
    FROM Medications m
    """
    return fetch_data(conn, query)


def get_average_visits_per_patient_by_department(conn, department):
    """Calculate the average number of visits per patient for a specific department."""
    query = """
    SELECT (SELECT COUNT(*)
            FROM Visits v
            WHERE v.PatientID IN (
                SELECT p.PatientID
                FROM Patients p
                WHERE p.PrimaryHCPID IN (
                    SELECT h.HCPID
                    FROM HealthCareProfessionals h
                    WHERE h.Department = ?
                )
            )) /
           (SELECT COUNT(*)
            FROM Patients p
            WHERE p.PrimaryHCPID IN (
                SELECT h.HCPID
                FROM HealthCareProfessionals h
                WHERE h.Department = ?
            )) AS AvgVisitsPerPatient
    """
    return fetch_data(conn, query, (department, department))


def get_patients_grouped_by_hcp(conn):
    """List patients grouped by their primary healthcare provider."""
    query = """
    SELECT h.HCPID, h.FirstName AS HCP_FirstName, h.LastName AS HCP_LastName,
           (SELECT GROUP_CONCAT(CONCAT(p.FirstName, ' ', p.LastName) SEPARATOR '; ')
            FROM Patients p
            WHERE p.PrimaryHCPID = h.HCPID) AS Patients
    FROM HealthCareProfessionals h
    """
    return fetch_data(conn, query)


# Test Queries
def test_queries():
    conn = get_cursor()[1]
    try:
        print("All Patients:")
        print(get_all_patients(conn))

        print("\nPatients Without Visits:")
        print(get_patients_without_visits(conn))

        print("\nPatients by Insurance Provider (InsuranceID: 00000001):")
        print(get_patients_by_insurance(conn, "00000001"))

        print("\nPatients with Multiple Medications:")
        print(get_patients_with_multiple_medications(conn))

        print("\nPatients Taking Aspirin:")
        print(get_patients_by_medication(conn, "Aspirin"))

        print("\nVisit Count Per Patient:")
        print(get_visit_count_per_patient(conn))

        print("\nDepartments Without Patients:")
        print(get_departments_without_patients(conn))

        print("\nPatients Over Age 65:")
        print(get_patients_over_age(conn, 65)) 

        print("\nHealthcare Professionals in Cardiology:")
        print(get_healthcare_professionals_by_department(conn, "Cardiology"))

        print("\nMedications and Their Side Effects:")
        print(get_medications_and_side_effects(conn))

        print("\nAverage Visits Per Patient in Cardiology:")
        print(get_average_visits_per_patient_by_department(conn, "Cardiology"))

        print("\nPatients Grouped by Healthcare Professional:")
        print(get_patients_grouped_by_hcp(conn))
    finally:
        close_connection(conn, None)


if __name__ == "__main__":
    test_queries()

