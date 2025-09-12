import sys
import os
from datetime import datetime, timezone
import fiftyone as fo
from pymongo import MongoClient

from create.image_loader import create_image_dataset
from create.audio_loader import create_audio_dataset
from create.vide_loader import create_video_dataset
from create.specific_file_type_loader import create_annotated_dataset

MONGO_URI = os.environ.get(
    "FIFTYONE_DATABASE_URI",
    "mongodb://localhost:27017/fiftyone?authSource=admin"
)
LOG_COLLECTION = "dataset_registry"

def log_dataset_event(name, dtype, source, count, dataset_id, status="success"):
    """Insert a dataset creation log into MongoDB."""
    client = MongoClient(MONGO_URI)
    db_name = MONGO_URI.split("/")[-1].split("?")[0]  # Extract DB name from URI
    db = client[db_name]

    log_entry = {
        "dataset_name": name,
        "dataset_id": dataset_id,  # MongoDB ObjectId of the dataset
        "type": dtype,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sample_count": count,
        "status": status
    }
    db[LOG_COLLECTION].insert_one(log_entry)
    client.close()
    print(f"Logged dataset creation in MongoDB collection '{LOG_COLLECTION}'")

def detect_dataset_type(data_dir):
    """Detect dataset type based on file extensions and folder structure."""
    exts = set(ext.lower() for ext in [
        os.path.splitext(f)[1] for f in os.listdir(data_dir)
    ])

    img_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"}
    if exts & img_exts:
        return "image"

    audio_exts = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
    if exts & audio_exts:
        return "audio"

    video_exts = {".mp4", ".avi", ".mov", ".mkv"}
    if exts & video_exts:
        return "video"

    if os.path.exists(os.path.join(data_dir, "annotations.json")):
        return "coco"
    if any(f.endswith(".txt") for f in os.listdir(data_dir)) and \
       os.path.exists(os.path.join(data_dir, "images")):
        return "yolo"
    if os.path.exists(os.path.join(data_dir, "Annotations")):
        return "voc"

    return None

def add_standard_metadata(dataset, source_dir, dtype):
    """Attach standardized metadata to the dataset."""
    dataset.info = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": source_dir,
        "type": dtype
    }
    dataset.save()

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_dataset.py <dataset_name> <data_dir>")
        sys.exit(1)

    dataset_name = sys.argv[1]
    data_dir = sys.argv[2]

    if not os.path.isdir(data_dir):
        print(f"Directory not found: {data_dir}")
        sys.exit(1)

    dtype = detect_dataset_type(data_dir)
    if not dtype:
        print("Could not detect dataset type. Supported: images, audio, video, COCO, YOLO, VOC")
        sys.exit(1)

    print(f"Detected dataset type: {dtype}")

    try:
        if dtype == "image":
            ds = create_image_dataset(dataset_name, data_dir)
        elif dtype == "audio":
            ds = create_audio_dataset(dataset_name, data_dir)
        elif dtype == "video":
            ds = create_video_dataset(dataset_name, data_dir)
        elif dtype in ("coco", "yolo", "voc"):
            ds = create_annotated_dataset(dataset_name, data_dir, dtype)
        else:
            print(f"Unsupported dataset type: {dtype}")
            sys.exit(1)

        ds.persistent = True
        ds.save()

        add_standard_metadata(ds, data_dir, dtype)

        dataset_id = str(ds._doc.id)

        log_dataset_event(dataset_name, dtype, data_dir, len(ds), dataset_id, status="success")

        print(f"Dataset '{dataset_name}' created, persisted, and stored in MongoDB with metadata.")
        fo.launch_app(ds).wait()

    except Exception as e:
        log_dataset_event(dataset_name, dtype, data_dir, 0, dataset_id=None, status=f"failed: {e}")
        print(f"Dataset creation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
