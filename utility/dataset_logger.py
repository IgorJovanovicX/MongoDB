import os
from datetime import datetime, timezone
from pymongo import MongoClient

MONGO_URI = os.environ.get(
    "FIFTYONE_DATABASE_URI",
    "mongodb://localhost:27017/fiftyone?authSource=admin"
)
LOG_COLLECTION = "dataset_registry"

def log_dataset_event(name, dtype, source, count, update_type="create", dataset_id=None, status="success"):

    client = MongoClient(MONGO_URI)
    db_name = MONGO_URI.split("/")[-1].split("?")[0]
    db = client[db_name]

    log_entry = {
        "dataset_name": name,
        "update_type": update_type,
        "type": dtype,
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sample_count": count,
        "status": status
    }

    if dataset_id is not None:
        log_entry["dataset_id"] = dataset_id

    db[LOG_COLLECTION].insert_one(log_entry)
    client.close()
    print(f"Logged dataset {update_type} in MongoDB collection '{LOG_COLLECTION}'")
