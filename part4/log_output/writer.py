import time
from datetime import datetime

OUTPUT_FILE = "/shared/timestamp.txt"

while True:
    timestamp = datetime.now().isoformat()
    with open(OUTPUT_FILE, "w") as file:
        file.write(timestamp)
    print(f"Writer: Updated timestamp to {timestamp}")
    time.sleep(5)
