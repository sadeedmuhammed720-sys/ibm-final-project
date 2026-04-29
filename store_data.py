import sqlite3
import re
import os

# --- STEP 2: THE DATABASE PIPELINE ---
# This script reads the raw text logs and stores them in a structured SQLite database.
# In the Enterprise world, this process is called ETL (Extract, Transform, Load).

LOG_FILE = "agriculture_telemetry.log"
DATABASE_FILE = "agriculture.db"

def setup_database():
    """Builds the table structure in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Drop existing table to start fresh
    cursor.execute("DROP TABLE IF EXISTS telemetry_logs")
    
    # Create the 'telemetry_logs' table
    # This table stores the timestamp, device, and the actual sensor values.
    cursor.execute("""
        CREATE TABLE telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            level TEXT,
            device_id TEXT,
            moisture REAL,
            temperature REAL,
            humidity REAL,
            status_message TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database structure created successfully.")

def parse_and_store_logs():
    """Reads logs, parses using Regex, and saves to database."""
    if not os.path.exists(LOG_FILE):
        print(f"Error: {LOG_FILE} not found!")
        return

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Regex patterns
    # 1. Main log structure: [TIMESTAMP] - [LEVEL] - [DEVICE] - [MESSAGE]
    log_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+-\s+\[(\w+)\]\s+-\s+(\w+)\s+-\s+(.*)$')
    
    # 2. Metric extractors (finding numbers inside the text)
    moisture_pattern = re.compile(r'Moisture:\s+(\d+\.\d+)%')
    temp_pattern = re.compile(r'Temp:\s+(\d+\.\d+)C')
    humidity_pattern = re.compile(r'Humidity:\s+(\d+\.\d+)%')

    logs_parsed = 0
    with open(LOG_FILE, "r") as f:
        for line in f:
            match = log_pattern.match(line.strip())
            if match:
                timestamp, level, device_id, message = match.groups()
                
                # Extract numeric values if they exist
                moisture = moisture_pattern.search(message)
                temperature = temp_pattern.search(message)
                humidity = humidity_pattern.search(message)
                
                # Convert to float or None
                m_val = float(moisture.group(1)) if moisture else None
                t_val = float(temperature.group(1)) if temperature else None
                h_val = float(humidity.group(1)) if humidity else None

                # Insert into Database
                cursor.execute("""
                    INSERT INTO telemetry_logs (timestamp, level, device_id, moisture, temperature, humidity, status_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (timestamp, level, device_id, m_val, t_val, h_val, message))
                
                logs_parsed += 1

    conn.commit()
    conn.close()
    print(f"ETL Complete: Processed {logs_parsed} log entries into '{DATABASE_FILE}'.")

if __name__ == "__main__":
    setup_database()
    parse_and_store_logs()
