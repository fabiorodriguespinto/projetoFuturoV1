import sqlite3
import time
import requests
from datetime import datetime
import os # For potential future use with environment variables
import yaml

# Assuming executar_retreinamento is correctly imported from elsewhere if needed,
# or defined in this file. For now, let's assume it's available.
from worker.tasks.retrain_model import executar_retreinamento

# Configuration Loading
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
DEFAULT_NN_SERVICE_URL = "http://nn_service:8001/predict_fallback_worker" # Fallback if config fails

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as stream:
            config = yaml.safe_load(stream)
        url = config.get('nn_service_url')
        if not url:
            print(f"WORKER ERROR: 'nn_service_url' not found in {CONFIG_PATH}. Using default.", flush=True)
            return DEFAULT_NN_SERVICE_URL
        print(f"WORKER: Loaded NN_SERVICE_URL: {url} from {CONFIG_PATH}", flush=True)
        return url
    except FileNotFoundError:
        print(f"WORKER ERROR: Configuration file not found at {CONFIG_PATH}. Using default.", flush=True)
        return DEFAULT_NN_SERVICE_URL
    except yaml.YAMLError as exc:
        print(f"WORKER ERROR: Error parsing YAML configuration file {CONFIG_PATH}: {exc}. Using default.", flush=True)
        return DEFAULT_NN_SERVICE_URL
    except Exception as e:
        print(f"WORKER ERROR: An unexpected error occurred while loading config: {e}. Using default.", flush=True)
        return DEFAULT_NN_SERVICE_URL

NN_SERVICE_URL = load_config()
DATABASE_PATH = "/data/app.db" # Consistent with docker-compose volume
LOOP_SLEEP_SECONDS = 60 * 5 # Run every 5 minutes, for example

def log_message(message):
    """Simple logger."""
    print(f"WORKER: {datetime.utcnow().isoformat()} - {message}", flush=True)

def init_db():
    """Initializes the database and table if they don't exist."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price REAL,
                day_of_year INT,
                created_at TEXT
            )
        """)
        conn.commit()
        log_message("Database initialized successfully.")
    except sqlite3.Error as e:
        log_message(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def get_prediction_from_nn_service(day_of_year: int):
    """Gets prediction from the NN service."""
    payload = {"day_of_year": day_of_year}
    try:
        response = requests.post(NN_SERVICE_URL, json=payload, timeout=10)
        if response.status_code == 200:
            prediction_data = response.json()
            if "prediction" in prediction_data:
                return prediction_data["prediction"]
            else:
                log_message(f"Error: 'prediction' key not found in NN service response: {prediction_data}")
                return None
        else:
            log_message(f"Error from NN service: Status {response.status_code}, Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        log_message(f"Error calling NN service: {e}")
        return None

def store_prediction(price: float, day_of_year: int):
    """Stores the prediction in the database."""
    if price is None:
        log_message("Skipping database insertion because price is None.")
        return

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO predictions (price, day_of_year, created_at) VALUES (?, ?, ?)",
            (price, day_of_year, datetime.utcnow().isoformat())
        )
        conn.commit()
        log_message(f"Successfully stored prediction: Price {price}, DayOfYear {day_of_year}")
    except sqlite3.Error as e:
        log_message(f"Error storing prediction: {e}")
    finally:
        if conn:
            conn.close()

def main_worker_loop():
    """Main loop for the worker."""
    log_message("Worker started.")
    init_db()

    while True:
        current_time = datetime.now()
        day_of_year = current_time.timetuple().tm_yday
        log_message(f"Running prediction cycle for day_of_year: {day_of_year}")

        # Get prediction from NN service
        predicted_price = get_prediction_from_nn_service(day_of_year)

        if predicted_price is not None:
            store_prediction(predicted_price, day_of_year)
        else:
            log_message("Failed to get prediction. Skipping storage for this cycle.")

        # Placeholder for the retraining logic
        # For now, we'll just log that it would run.
        log_message("Checking if retraining is needed...")
        executar_retreinamento() # This function needs to be defined or imported correctly.
                                 # Assuming it's a heavy operation, it might not run every cycle.

        log_message(f"Cycle finished. Sleeping for {LOOP_SLEEP_SECONDS} seconds.")
        time.sleep(LOOP_SLEEP_SECONDS)

if __name__ == "__main__":
    # Note: The original file had `executar_retreinamento()` called directly.
    # This is likely not intended for a continuous worker.
    # If it's a one-off task, it should be run differently.
    # For a periodic worker, the main_worker_loop should be called.
    main_worker_loop()