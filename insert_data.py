import sys
import os
import fiftyone as fo

from utility.dataset_logger import log_dataset_event
from utility.dataset_type_detector import detect_dataset_type
from utility.dataset_metadata import add_standard_metadata
from insert.image_insert import insert_image_data
from insert.audio_insert import insert_audio_data
from insert.video_insert import insert_video_data
from insert.special_file_type_insert import insert_annotated_data

def main():
    if len(sys.argv) != 3:
        print("Usage: python insert_into_dataset.py <dataset_name> <data_dir>")
        sys.exit(1)

    dataset_name = sys.argv[1]
    data_dir = sys.argv[2]

    if not os.path.isdir(data_dir):
        print(f"Directory not found: {data_dir}")
        sys.exit(1)

    if dataset_name not in fo.list_datasets():
        print(f"Dataset '{dataset_name}' does not exist. Cannot insert data.")
        sys.exit(1)

    ds = fo.load_dataset(dataset_name)
    existing_type = ds.info.get("type")
    if not existing_type:
        print(f"Dataset '{dataset_name}' has no recorded type in metadata.")
        sys.exit(1)

    new_type = detect_dataset_type(data_dir)
    if not new_type:
        print("Could not detect type of new data. Supported: images, audio, video, COCO, YOLO, VOC")
        sys.exit(1)

    if new_type != existing_type:
        print(f"Type mismatch: dataset is '{existing_type}', new data is '{new_type}'")
        sys.exit(1)

    print(f"Adding {new_type} data to dataset '{dataset_name}'...")

    try:
        if new_type == "image":
            added_count = insert_image_data(ds, data_dir)
        elif new_type == "audio":
            added_count = insert_audio_data(ds, data_dir)
        elif new_type == "video":
            added_count = insert_video_data(ds, data_dir)
        elif new_type in ("coco", "yolo", "voc"):
            added_count = insert_annotated_data(ds, data_dir, new_type)
        else:
            print(f"Unsupported dataset type: {new_type}")
            sys.exit(1)

        ds.save()

        add_standard_metadata(ds, data_dir, new_type, extra_metadata={"last_insert_count": added_count})

        log_dataset_event(dataset_name, new_type, data_dir, added_count, update_type="insert", dataset_id=None, status="success")
        print(f"Added {added_count} samples to dataset '{dataset_name}'.")

    except Exception as e:
        log_dataset_event(dataset_name, new_type, data_dir, 0, update_type="insert", dataset_id=None, status=f"failed: {e}")
        print(f"Failed to insert data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
