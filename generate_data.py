import random
import time
from datetime import datetime, timedelta
import os

# --- STEP 1: THE DATA FACTORY ---
# This script generates a realistic "Enterprise Log" for an agricultural system.
# It simulates three types of devices: Soil Sensors, Weather Stations, and Irrigation Pumps.

LOG_FILE = "agriculture_telemetry.log"

def generate_enterprise_logs(num_days=7):
    print(f"Generating log data for {num_days} days...")
    
    start_date = datetime.now() - timedelta(days=num_days)
    devices = {
        "SOIL_S1": {"type": "SOIL", "moisture_range": (35, 55), "temp_range": (20, 25)},
        "SOIL_S2": {"type": "SOIL", "moisture_range": (30, 50), "temp_range": (18, 23)},
        "WEATHER_W1": {"type": "WEATHER", "temp_range": (15, 35), "humidity_range": (40, 70)},
        "PUMP_P1": {"type": "PUMP", "status": ["ACTIVE", "IDLE"]}
    }

    with open(LOG_FILE, "w") as f:
        current_time = start_date
        
        while current_time < datetime.now():
            for dev_id, config in devices.items():
                # Randomize if a log is written (simulates varied reporting intervals)
                if random.random() > 0.8:
                    continue
                
                level = "INFO"
                message = ""
                
                if config["type"] == "SOIL":
                    moisture = round(random.uniform(*config["moisture_range"]), 2)
                    temp = round(random.uniform(*config["temp_range"]), 2)
                    
                    # INJECT ANOMALY: Low Moisture
                    if random.random() < 0.05: # 5% chance of anomaly
                        moisture = round(random.uniform(5, 15), 2)
                        level = "WARNING"
                        message = f"Moisture: {moisture}%, Temp: {temp}C | Status: LOW_MOISTURE_CRITICAL"
                    else:
                        message = f"Moisture: {moisture}%, Temp: {temp}C | Status: OK"
                        
                elif config["type"] == "WEATHER":
                    temp = round(random.uniform(*config["temp_range"]), 2)
                    humidity = round(random.uniform(*config["humidity_range"]), 2)
                    
                    # INJECT ANOMALY: Heatwave
                    if random.random() < 0.03:
                        temp = round(random.uniform(42, 50), 2)
                        level = "ERROR"
                        message = f"Temp: {temp}C, Humidity: {humidity}% | Status: HEAT_WARNING"
                    else:
                        message = f"Temp: {temp}C, Humidity: {humidity}% | Status: OK"
                        
                elif config["type"] == "PUMP":
                    status = random.choice(config["status"])
                    message = f"Pump Status: {status} | Feedback: SUCCESS"

                # Write the log line
                log_line = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - [{level}] - {dev_id} - {message}\n"
                f.write(log_line)
                
            # Increment time by random minutes
            current_time += timedelta(minutes=random.randint(5, 30))

    print(f"Successfully generated {LOG_FILE}")

if __name__ == "__main__":
    generate_enterprise_logs(10) # Generate 10 days of data
