import sqlite3

# Establish connection to the SQLite database
conn = sqlite3.connect('results.db')
cursor = conn.cursor()

# Create the setupResults table
setup_table_info = """
CREATE TABLE IF NOT EXISTS setupResults (
    COIL VARCHAR(10) PRIMARY KEY,          -- Foreign key referencing RESULT(COIL)
    RMRG INT CHECK (RMRG BETWEEN 32 AND 200),  -- Number between 32 and 200
    RMTHICK INT CHECK (RMTHICK BETWEEN 32 AND 52), -- Number between 32 and 52
    RMWIDTH INT CHECK (RMWIDTH BETWEEN 900 AND 2100), -- Number between 900 and 2100
    FOREIGN KEY (COIL) REFERENCES RESULT(COIL)
);
"""
cursor.execute(setup_table_info)
print("setupResults table created or already exists.")

# Insert records into setupResults
try:
    cursor.execute("""
        INSERT INTO setupResults (COIL, RMRG, RMTHICK, RMWIDTH)
        VALUES ('NA001310', 100, 40, 2000) 
    """)
    cursor.execute("""
        INSERT INTO setupResults (COIL, RMRG, RMTHICK, RMWIDTH)
        VALUES ('NA001311', 150, 45, 1500) 
    """)
    cursor.execute("""
        INSERT INTO setupResults (COIL, RMRG, RMTHICK, RMWIDTH)
        VALUES ('NA001312', 75, 38, 1600) 
    """)
    cursor.execute("""
        INSERT INTO setupResults (COIL, RMRG, RMTHICK, RMWIDTH)
        VALUES ('NA001313', 180, 50, 1528) 
    """)
    conn.commit()
    print("Records successfully inserted into setupResults.")
except sqlite3.IntegrityError as e:
    print(f"IntegrityError: {e}")
except sqlite3.Error as e:
    print(f"SQLite error: {e}")

print("\nRecords from setupResults table:")
cursor.execute("SELECT * FROM setupResults;")
setup_records = cursor.fetchall()
for record in setup_records:
    print(record)
# Close the database connection
conn.close()
print("Database connection closed.")
