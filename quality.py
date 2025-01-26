import sqlite3

# Establish connection to the SQLite database
conn = sqlite3.connect('results.db')
cursor = conn.cursor()

# Create the qualityResults table
quality_table_info = """
CREATE TABLE IF NOT EXISTS quality (
    COIL VARCHAR(10) PRIMARY KEY,                -- Primary key referencing RESULT(COIL)
    CRT INT ,       -- Number between 1 and 25
    FRT INT ,       -- Number between 1 and 25
    elongation INT , -- Number between 1 and 25
    TensileStrength INT, -- Number between 1 and 25
    FOREIGN KEY (COIL) REFERENCES RESULT(COIL)
);
"""
cursor.execute(quality_table_info)
print("quality table created or already exists.")

# Insert records into qualityResults
try:
    cursor.execute("""
        INSERT INTO quality (COIL, CRT, FRT, elongation, TensileStrength)
        VALUES ('NA001310', 20, 15, 12, 22) 
    """)
    cursor.execute("""
        INSERT INTO quality (COIL, CRT, FRT, elongation, TensileStrength)
        VALUES ('NA001311', 18, 10, 16, 25) 
    """)
    cursor.execute("""
        INSERT INTO quality (COIL, CRT, FRT, elongation, TensileStrength)
        VALUES ('NA001312', 23, 22, 20, 24) 
    """)
    cursor.execute("""
        INSERT INTO quality (COIL, CRT, FRT, elongation, TensileStrength)
        VALUES ('NA001313', 12, 19, 18, 21) 
    """)
    conn.commit()
    print("Records successfully inserted into quality.")
except sqlite3.IntegrityError as e:
    print(f"IntegrityError: {e}")
except sqlite3.Error as e:
    print(f"SQLite error: {e}")

# Close the connection
conn.close()
