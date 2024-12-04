from database.db_connection import get_cursor, close_connection


def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS HealthCareProfessionals (
            HCPID CHAR(8) PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            ContactNumber CHAR(12),
            Department VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Patients (
            PatientID CHAR(8) PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            DOB DATE,
            Address VARCHAR(255),
            PhoneNumber CHAR(12),
            PrimaryHCPID CHAR(8),
            FOREIGN KEY (PrimaryHCPID) REFERENCES HealthCareProfessionals(HCPID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Medications (
            MedicationID CHAR(8) PRIMARY KEY,
            MedicationName VARCHAR(100),
            Dosage VARCHAR(50),
            Manufacturer VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Insurance (
            InsuranceID CHAR(8) PRIMARY KEY,
            InsuranceName VARCHAR(100),
            Email VARCHAR(100),
            ContactNumber CHAR(12)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Visits (
            PatientID CHAR(8),
            VisitDate DATE,
            HCPID CHAR(8),
            Reason VARCHAR(255),
            Notes TEXT,
            PRIMARY KEY (PatientID, VisitDate),
            FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
            FOREIGN KEY (HCPID) REFERENCES HealthCareProfessionals(HCPID)
        );

        """,
        """
        CREATE TABLE IF NOT EXISTS PatientInsurance (
            PatientID CHAR(8),
            InsuranceID CHAR(8),
            CoverageStartDate DATE DEFAULT NULL,
            CoverageEndDate DATE DEFAULT NULL,
            PRIMARY KEY (PatientID, InsuranceID),
            FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
            FOREIGN KEY (InsuranceID) REFERENCES Insurance(InsuranceID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS SideEffects (
            MedicationID CHAR(8),
            SideEffectDescription VARCHAR(255),
            Severity VARCHAR(20),
            PRIMARY KEY (MedicationID, SideEffectDescription),
            FOREIGN KEY (MedicationID) REFERENCES Medications(MedicationID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS HCPDepartments (
            HCPID CHAR(8),
            DepartmentName VARCHAR(100),
            PRIMARY KEY (HCPID, DepartmentName),
            FOREIGN KEY (HCPID) REFERENCES HealthCareProfessionals(HCPID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS PatientMedications (
            PatientID CHAR(8),
            MedicationID CHAR(8),
            StartDate DATE,
            EndDate DATE,
            Dosage VARCHAR(50),
            PRIMARY KEY (PatientID, MedicationID),
            FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
            FOREIGN KEY (MedicationID) REFERENCES Medications(MedicationID)
);


        """,
    ]

    cur, conn = get_cursor()

    for query in queries:
        try:
            cur.execute(query)
            print(f"Executed query: {query.strip().splitlines()[0]}")  # Debugging info
        except Exception as e:
            print(f"Error executing query: {e}")

    close_connection(conn, cur)


if __name__ == "__main__":
    create_tables()

